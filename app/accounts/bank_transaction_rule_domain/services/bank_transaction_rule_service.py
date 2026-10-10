"""

Business logic for Bank Transaction Rule -- port of

``erpnext/accounts/doctype/bank_transaction_rule/bank_transaction_rule.py``.



Upstream hook -> here

-------------------

``autoname: field:rule_name``  uniqueness in :meth:`_assert_name_free`

``before_insert``              priority auto-assign in :meth:`create`

``validate``                   :meth:`_validate`

``validate_amount_formula``    :func:`validate_amount_formula`

``evaluate_rule``              :meth:`evaluate_rule`

``on_trash``                   :meth:`_clear_matched_transactions`

``after_delete``               :meth:`_renumber_priorities`



The ``company`` field collapses to ``business_id``, so upstream's "Account

company does not match with the rule company" check is satisfied

structurally: every account query is already scoped to the tenant, so a

foreign company's account cannot be referenced at all.



``frappe.safe_eval`` is replaced by :func:`_safe_eval`, a small AST evaluator

that admits only the operators upstream's token regex allows. ``eval`` is never

called on rule input.

"""



from __future__ import annotations



import ast

import re

import uuid

from decimal import Decimal

from typing import Optional, Union



from sqlalchemy.orm import Session



from app.accounts.bank_transaction_rule_accounts_domain.models.bank_transaction_rule_accounts import (

    BankTransactionRuleAccount,

)

from app.accounts.bank_transaction_rule_description_conditions_domain.models.bank_transaction_rule_description_conditions import (

    BankTransactionRuleDescriptionCondition,

)

from app.accounts.bank_transaction_rule_domain.models.bank_transaction_rule import (

    BankTransactionRule,

    RuleBankEntryType,

    RuleClassifyAs,

    RuleTransactionType,

)

from app.accounts.bank_transaction_rule_domain.repositories.bank_transaction_rule_repository import (

    BankTransactionRuleRepository,

)

from app.accounts.bank_transaction_rule_domain.schemas.bank_transaction_rule import (

    BankTransactionRuleCreate,

    BankTransactionRuleUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankTransactionRuleService", "validate_amount_formula", "InvalidFormulaError"]



# Upstream module-level constants, reproduced verbatim.

PLAIN_NUMBER_PATTERN = re.compile(r"^-?\d+(\.\d+)?$")

ALLOWED_FORMULA_TOKEN = re.compile(r"\s+|transaction_amount|\d+(?:\.\d+)?|[+\-*/%^()]")

PYTHON_ONLY_OPERATORS = ("**", "//")



#: Operators the token regex admits. ``^`` is exponent in expr-eval syntax and

#: is translated to ``**`` before evaluation.

_BINOPS = {

    ast.Add: lambda a, b: a + b,

    ast.Sub: lambda a, b: a - b,

    ast.Mult: lambda a, b: a * b,

    ast.Div: lambda a, b: a / b,

    ast.Mod: lambda a, b: a % b,

    ast.Pow: lambda a, b: a ** b,

}





class InvalidFormulaError(DomainValidationError):

    """A debit/credit formula that is not a plain number or an allowed expression."""



    def __init__(self, formula: str) -> None:

        super().__init__(

            f"Invalid debit/credit formula: {formula}", code="bank_transaction_rule_bad_formula"

        )

        self.formula = formula





def _is_expr_eval_formula(formula: str) -> bool:

    """

    Port of ``_is_expr_eval_formula``: the string must consist entirely of

    allowed tokens and have balanced parentheses.

    """

    position = 0

    while position < len(formula):

        match = ALLOWED_FORMULA_TOKEN.match(formula, position)

        if not match:

            return False

        position = match.end()

    return formula.count("(") == formula.count(")")





def _safe_eval(expression: str, transaction_amount: float = 1) -> Union[int, float]:

    """

    Evaluate an arithmetic expression with ``transaction_amount`` bound.



    Replaces ``frappe.safe_eval``. Only literals, the single allowed name,

    unary +/- and the binary operators in ``_BINOPS`` are admitted; anything

    else raises. Division by zero is allowed to raise and is caught by the

    caller as an invalid formula, matching upstream's blanket ``except``.

    """

    tree = ast.parse(expression, mode="eval")



    def walk(node: ast.AST) -> Union[int, float]:

        if isinstance(node, ast.Expression):

            return walk(node.body)

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):

                return node.value

            raise ValueError(f"literal not allowed: {node.value!r}")

        if isinstance(node, ast.Name):

            if node.id == "transaction_amount":

                return transaction_amount

            raise ValueError(f"name not allowed: {node.id}")

        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.USub):

                return -walk(node.operand)

            if isinstance(node.op, ast.UAdd):

                return +walk(node.operand)

            raise ValueError("unary operator not allowed")

        if isinstance(node, ast.BinOp):

            fn = _BINOPS.get(type(node.op))

            if fn is None:

                raise ValueError("binary operator not allowed")

            return fn(walk(node.left), walk(node.right))

        raise ValueError(f"node not allowed: {type(node).__name__}")



    return walk(tree)





def validate_amount_formula(formula: Optional[str]) -> None:

    """

    Port of ``validate_amount_formula``.



    A blank formula is fine (that side of the entry is simply unused). A plain

    number passes outright. Otherwise the string must not use Python-only

    operators, must tokenise cleanly, and must evaluate to a number.

    """

    stripped = (formula or "").strip()

    # Blank means "this side of the entry is unused". Upstream checks only

    # `not formula`, so a whitespace-only string falls through and fails inside

    # safe_eval; treating it as blank here makes the function total. The API

    # cannot reach this case anyway, because input schemas strip whitespace.

    if not stripped:

        return



    if PLAIN_NUMBER_PATTERN.match(stripped):

        return



    if any(operator in stripped for operator in PYTHON_ONLY_OPERATORS):

        raise InvalidFormulaError(formula)



    if not _is_expr_eval_formula(stripped):

        raise InvalidFormulaError(formula)



    # expr-eval uses ^ for exponentiation; translate for the smoke-test only.

    python_formula = stripped.replace("^", "**")



    try:

        result = _safe_eval(python_formula, transaction_amount=1)

    except Exception as exc:

        raise InvalidFormulaError(formula) from exc



    if not isinstance(result, (int, float)) or isinstance(result, bool):

        raise InvalidFormulaError(formula)





class BankTransactionRuleService:

    def __init__(self, repository: Optional[BankTransactionRuleRepository] = None) -> None:

        self.repository = repository or BankTransactionRuleRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID

    ) -> BankTransactionRule:

        row = self.repository.get_by_id(db, business_id, rule_id)

        if row is None:

            raise NotFoundError("Bank Transaction Rule", rule_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _assert_name_free(

        self,

        db: Session,

        business_id: uuid.UUID,

        rule_name: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, rule_name, exclude_id=exclude_id)

        if existing is not None:

            raise ConflictError(

                f"Bank Transaction Rule '{rule_name}' already exists",

                code="bank_transaction_rule_duplicate",

            )



    @staticmethod

    def _validate_amount_range(row: BankTransactionRule) -> None:

        if row.min_amount is not None and row.max_amount is not None:

            if row.min_amount > row.max_amount:

                raise DomainValidationError(

                    "Min amount cannot be greater than max amount.",

                    code="bank_transaction_rule_min_above_max",

                )



    @staticmethod

    def _validate_payment_entry(row: BankTransactionRule) -> None:

        if row.classify_as is not RuleClassifyAs.PAYMENT_ENTRY:

            return

        if not row.party_type:

            raise DomainValidationError(

                "Party type is required to create a payment entry.",

                code="bank_transaction_rule_party_type_mandatory",

            )

        if not row.party:

            raise DomainValidationError(

                "Party is required to create a payment entry.",

                code="bank_transaction_rule_party_mandatory",

            )

        if row.account_id is None:

            raise DomainValidationError(

                "Party account is required to create a payment entry.",

                code="bank_transaction_rule_account_mandatory",

            )



    @staticmethod

    def _validate_bank_entry(row: BankTransactionRule) -> None:

        if row.classify_as is not RuleClassifyAs.BANK_ENTRY:

            return



        multiple = row.bank_entry_type is RuleBankEntryType.MULTIPLE_ACCOUNTS

        if not multiple:

            # Unset counts as Single Account, matching upstream's `or`.

            if row.account_id is None:

                raise DomainValidationError(

                    "Please add an account for the Bank Entry rule.",

                    code="bank_transaction_rule_bank_entry_account_mandatory",

                )

            return



        if not row.accounts:

            raise DomainValidationError(

                "Please configure accounts for the Bank Entry rule.",

                code="bank_transaction_rule_bank_entry_accounts_mandatory",

            )



        last_index = len(row.accounts) - 1

        for index, account in enumerate(row.accounts):

            if index == last_index:

                # The balancing row's amount is computed from the others.

                if account.debit or account.credit:

                    raise DomainValidationError(

                        "The last account row must not have any debit or credit amounts set.",

                        code="bank_transaction_rule_last_row_has_amount",

                    )

                continue

            if account.debit:

                validate_amount_formula(account.debit)

            if account.credit:

                validate_amount_formula(account.credit)



    @staticmethod

    def _validate_regex(row: BankTransactionRule) -> None:

        for condition in row.description_rules:

            if condition.check == "Regex":

                try:

                    re.compile(condition.value or "")

                except re.error as exc:

                    raise DomainValidationError(

                        "Invalid regex pattern.", code="bank_transaction_rule_bad_regex"

                    ) from exc



    def _validate(self, row: BankTransactionRule) -> None:

        self._validate_amount_range(row)

        self._validate_payment_entry(row)

        self._validate_bank_entry(row)

        self._validate_regex(row)



    # ── helpers ported from the delete hooks ─────────────────────────────────

    def _clear_matched_transactions(

        self, db: Session, business_id: uuid.UUID, rule: BankTransactionRule

    ) -> None:

        """Port of ``on_trash``: drop the rule reference from matched transactions."""

        from app.accounts.bank_transaction_domain.repositories.bank_transaction_repository import (

            BankTransactionRepository,

        )



        for transaction in BankTransactionRepository().list_matching_rule(

            db, business_id, rule.id

        ):

            transaction.matched_transaction_rule_id = None

            transaction.is_rule_evaluated = False



    def _renumber_priorities(self, db: Session, business_id: uuid.UUID) -> None:

        """Port of ``after_delete``: close the gap left by the deleted rule."""

        for position, rule in enumerate(

            self.repository.list_by_priority(db, business_id), start=1

        ):

            if rule.priority != position:

                rule.priority = position



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID) -> BankTransactionRule:

        return self._get_or_404(db, business_id, rule_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankTransactionRule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankTransactionRule].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_children(

        self,

        business_id: uuid.UUID,

        row: BankTransactionRule,

        description_rules: Optional[list[dict]],

        accounts: Optional[list[dict]],

    ) -> None:

        if description_rules is not None:

            row.description_rules.clear()

            for idx, item in enumerate(description_rules, start=1):

                row.description_rules.append(

                    BankTransactionRuleDescriptionCondition(

                        business_id=business_id,

                        idx=idx,

                        check=item["check"],

                        value=item["value"],

                    )

                )

        if accounts is not None:

            row.accounts.clear()

            for idx, item in enumerate(accounts, start=1):

                row.accounts.append(

                    BankTransactionRuleAccount(

                        business_id=business_id,

                        idx=idx,

                        account_id=item.get("account_id"),

                        party_type=item.get("party_type"),

                        party=item.get("party"),

                        debit=item.get("debit"),

                        credit=item.get("credit"),

                        user_remark=item.get("user_remark"),

                    )

                )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankTransactionRuleCreate

    ) -> BankTransactionRule:

        self._assert_name_free(db, business_id, payload.rule_name)



        row = BankTransactionRule(

            business_id=business_id,

            name=payload.rule_name,

            rule_name=payload.rule_name,

            transaction_type=payload.transaction_type,

            min_amount=payload.min_amount,

            max_amount=payload.max_amount,

            rule_description=payload.rule_description,

            classify_as=payload.classify_as,

            bank_entry_type=payload.bank_entry_type,

            account_id=payload.account_id,

            party_type=payload.party_type,

            party=payload.party,

            # `before_insert`: take the next free slot when not given.

            priority=payload.priority

            or (self.repository.highest_priority(db, business_id) + 1),

        )

        self._replace_children(

            business_id,

            row,

            [d.model_dump() for d in payload.description_rules],

            [a.model_dump() for a in payload.accounts],

        )



        try:

            self._validate(row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        rule_id: uuid.UUID,

        payload: BankTransactionRuleUpdate,

    ) -> BankTransactionRule:

        row = self._get_or_404(db, business_id, rule_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            if "rule_name" in changes:

                self._assert_name_free(db, business_id, changes["rule_name"], exclude_id=row.id)

                row.rule_name = changes["rule_name"]

                row.name = changes["rule_name"]



            for field_name in (

                "transaction_type", "min_amount", "max_amount", "rule_description",

                "classify_as", "bank_entry_type", "account_id", "party_type", "party",

            ):

                if field_name in changes:

                    setattr(row, field_name, changes[field_name])



            self._replace_children(

                business_id, row, changes.get("description_rules"), changes.get("accounts")

            )

            self._validate(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, rule_id)



        try:

            self._clear_matched_transactions(db, business_id, row)

            self.repository.delete(db, row)

            self._renumber_priorities(db, business_id)

        except Exception:

            db.rollback()

            raise



        db.commit()



    # ── rule matching ────────────────────────────────────────────────────────

    @staticmethod

    def evaluate_rule(rule: BankTransactionRule, transaction: object) -> bool:

        """

        Port of ``evaluate_rule``.



        Returns True on the *first* matching description condition. The company

        check is dropped: it compared ``self.company`` to the transaction's

        company, and both now collapse to the same ``business_id``.

        """

        withdrawal = Decimal(str(transaction.withdrawal or 0))  # type: ignore[attr-defined]

        deposit = Decimal(str(transaction.deposit or 0))  # type: ignore[attr-defined]



        if rule.transaction_type is RuleTransactionType.WITHDRAWAL and withdrawal == 0:

            return False

        if rule.transaction_type is RuleTransactionType.DEPOSIT and deposit == 0:

            return False



        amount = withdrawal or deposit



        if rule.min_amount is not None and amount < rule.min_amount:

            return False

        if rule.max_amount is not None and amount > rule.max_amount:

            return False



        description = (getattr(transaction, "description", None) or "").lower()

        for condition in rule.description_rules:

            value = (condition.value or "").lower()



            if condition.check == "Contains" and value in description:

                return True

            if condition.check == "Starts With" and description.startswith(value):

                return True

            if condition.check == "Ends With" and description.endswith(value):

                return True

            if condition.check == "Regex":

                try:

                    if re.search(value, description):

                        return True

                except re.error:

                    # An invalid pattern is rejected at save time; if one is

                    # here anyway it must not abort the whole evaluation run.

                    continue



        return False



    def find_matching_rule(

        self, db: Session, business_id: uuid.UUID, transaction: object

    ) -> Optional[BankTransactionRule]:

        """

        First matching rule in ``priority`` order.



        This is what the upstream scheduler's ``run_rule_evaluation`` does per

        transaction; exposed here so a caller can classify on demand.

        """

        for rule in self.repository.list_by_priority(db, business_id):

            if self.evaluate_rule(rule, transaction):

                return rule

        return None
