"""

Validators shared by the tax-template doctypes.



Ported from ``erpnext/accounts/services/taxes.py``, whose helpers both the Sales

and the Purchase Taxes and Charges Template call through

``valdiate_taxes_and_charges_template``. Keeping them in one module means the two

templates cannot drift apart on what a valid tax row is.



The row types differ (``SalesTaxesAndCharges`` vs ``PurchaseTaxesAndCharges``),

so these take the fields they need rather than a concrete model. ``getattr`` is

used where a field exists on one row type and not the other -- ``category`` is

purchase-only, which is exactly how upstream's ``tax.get("category")`` behaves.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.cost_center_domain.models.cost_center import CostCenter

from app.accounts.tax_enums import ChargeType

from app.core.errors import DomainValidationError



__all__ = [

    "validate_taxes_and_charges",

    "validate_account_head",

    "validate_cost_center",

    "validate_inclusive_tax",

]





def validate_taxes_and_charges(

    idx: int, charge_type: Optional[ChargeType], row_id: Optional[str]

) -> None:

    """

    Port of ``validate_taxes_and_charges``.



    ``row_id`` only means something for the "previous row" charge types, and

    even then it must point *backwards* -- a row cannot depend on one that has

    not been computed yet.

    """

    if charge_type in (

        ChargeType.ACTUAL,

        ChargeType.ON_NET_TOTAL,

        ChargeType.ON_PAID_AMOUNT,

    ) and row_id:

        raise DomainValidationError(

            "Can refer row only if the charge type is 'On Previous Row Amount' "

            "or 'Previous Row Total'",

            code="tax_row_id_not_allowed",

        )



    if charge_type in (ChargeType.ON_PREVIOUS_ROW_AMOUNT, ChargeType.ON_PREVIOUS_ROW_TOTAL):

        if idx == 1:

            raise DomainValidationError(

                "Cannot select charge type as 'On Previous Row Amount' or "

                "'On Previous Row Total' for first row",

                code="tax_previous_row_on_first_row",

            )

        if not row_id:

            raise DomainValidationError(

                f"Please specify a valid Row ID for row {idx}",

                code="tax_missing_row_id",

            )

        try:

            referred = int(row_id)

        except (TypeError, ValueError):

            raise DomainValidationError(

                f"Please specify a valid Row ID for row {idx}",

                code="tax_missing_row_id",

            ) from None

        if referred >= idx:

            raise DomainValidationError(

                "Cannot refer row number greater than or equal to current row number "

                "for this Charge type",

                code="tax_row_id_forward_reference",

            )





def validate_account_head(

    db: Session,

    business_id: uuid.UUID,

    idx: int,

    account_id: Optional[uuid.UUID],

    context: str = "",

) -> Account:

    """

    Port of ``validate_account_head``.



    Upstream's first check is that the account belongs to the same company;

    tenancy makes that structural here, so what remains is the group rule.

    """

    if account_id is None:

        raise DomainValidationError(

            f"Row {idx}: Account Head is mandatory", code="tax_account_head_mandatory"

        )



    account = db.get(Account, account_id)

    if account is None or account.business_id != business_id:

        raise DomainValidationError(

            f"Row {idx}: The {context} Account {account_id} does not belong to this company",

            code="tax_account_head_not_found",

        )

    if account.is_group:

        raise DomainValidationError(

            f"You selected the account group {account.name} as {context} Account in "

            f"row {idx}. Please select a single account.",

            code="tax_account_head_is_group",

        )

    return account





def validate_cost_center(

    db: Session,

    business_id: uuid.UUID,

    idx: int,

    cost_center_id: Optional[uuid.UUID],

) -> None:

    """

    Port of ``validate_cost_center``.



    The upstream body only checks that the cost centre belongs to the same

    company, which tenancy already guarantees. The lookup is still performed so

    a dangling id is caught rather than silently accepted.

    """

    if cost_center_id is None:

        return



    cost_center = db.get(CostCenter, cost_center_id)

    if cost_center is None or cost_center.business_id != business_id:

        raise DomainValidationError(

            f"Row {idx}: Cost Center {cost_center_id} does not belong to this company",

            code="tax_cost_center_not_found",

        )





def validate_inclusive_tax(

    idx: int,

    charge_type: Optional[ChargeType],

    included_in_print_rate: bool,

    row_id: Optional[str],

    category: Optional[str],

    taxes: Sequence[object],

) -> None:

    """

    Port of ``validate_inclusive_tax``.



    A tax folded into the printed price has to be consistent with the rows it

    derives from: an 'Actual' charge has no rate to fold in, and a

    "previous row" charge inherits the inclusiveness of the rows it references.

    """

    if not included_in_print_rate:

        return



    if charge_type is ChargeType.ACTUAL:

        raise DomainValidationError(

            f"Charge of type 'Actual' in row {idx} cannot be included in Item Rate "

            f"or Paid Amount",

            code="tax_inclusive_actual_not_allowed",

        )



    def _previous_row_error(row_range: str) -> None:

        raise DomainValidationError(

            f"To include tax in row {idx} in Item rate, taxes in rows {row_range} "

            f"must also be included",

            code="tax_inclusive_previous_rows",

        )



    if charge_type is ChargeType.ON_PREVIOUS_ROW_AMOUNT:

        try:

            referred = int(row_id)  # type: ignore[arg-type]

        except (TypeError, ValueError):

            return  # validate_taxes_and_charges already rejects a bad row_id

        if referred - 1 >= len(taxes):

            return

        if not bool(getattr(taxes[referred - 1], "included_in_print_rate", False)):

            _previous_row_error(str(row_id))



    elif charge_type is ChargeType.ON_PREVIOUS_ROW_TOTAL:

        try:

            referred = int(row_id)  # type: ignore[arg-type]

        except (TypeError, ValueError):

            return

        if not all(

            bool(getattr(t, "included_in_print_rate", False)) for t in taxes[: referred - 1]

        ):

            _previous_row_error(f"1 - {row_id}")



    elif category == "Valuation":

        raise DomainValidationError(

            "Valuation type charges can not be marked as Inclusive",

            code="tax_inclusive_valuation_not_allowed",

        )
