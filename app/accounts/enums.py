"""

Enums shared across the accounts domain.



Values are copied verbatim from the ``options`` strings in the ERPNext doctype

JSON (``erpnext/accounts/doctype/account/account.json`` and

``.../account_category/account_category.json``) so a migrated chart of accounts

loads without value remapping. Note ERPNext prefixes every optional Select with

a leading empty line -- that empty value is represented here by ``None`` in the

model rather than by an empty-string member.

"""



from __future__ import annotations



from enum import Enum



__all__ = [

    "RootType",

    "ReportType",

    "BalanceMustBe",

    "FreezeAccount",

    "AccountType",

    "ROOT_TYPE_TO_REPORT_TYPE",

]





class RootType(str, Enum):

    """Account.json -> ``root_type`` Select."""



    ASSET = "Asset"

    LIABILITY = "Liability"

    INCOME = "Income"

    EXPENSE = "Expense"

    EQUITY = "Equity"





class ReportType(str, Enum):

    """Account.json -> ``report_type`` Select."""



    BALANCE_SHEET = "Balance Sheet"

    PROFIT_AND_LOSS = "Profit and Loss"





class BalanceMustBe(str, Enum):

    """Account.json -> ``balance_must_be`` Select."""



    DEBIT = "Debit"

    CREDIT = "Credit"





class FreezeAccount(str, Enum):

    """Account.json -> ``freeze_account`` Select (``No``/``Yes``)."""



    NO = "No"

    YES = "Yes"





class AccountType(str, Enum):

    """

    Account.json -> ``account_type`` Select.



    Taken from the generated ``DF.Literal[...]`` list in

    ``erpnext/accounts/doctype/account/account.py``, which is the authoritative

    superset of what the JSON ``options`` string is truncated to in the UI.

    """



    ACCUMULATED_DEPRECIATION = "Accumulated Depreciation"

    ASSET_RECEIVED_BUT_NOT_BILLED = "Asset Received But Not Billed"

    BANK = "Bank"

    CASH = "Cash"

    CHARGEABLE = "Chargeable"

    CAPITAL_WORK_IN_PROGRESS = "Capital Work in Progress"

    COST_OF_GOODS_SOLD = "Cost of Goods Sold"

    CURRENT_ASSET = "Current Asset"

    CURRENT_LIABILITY = "Current Liability"

    DEPRECIATION = "Depreciation"

    DIRECT_EXPENSE = "Direct Expense"

    DIRECT_INCOME = "Direct Income"

    EQUITY = "Equity"

    EXPENSE_ACCOUNT = "Expense Account"

    EXPENSES_INCLUDED_IN_ASSET_VALUATION = "Expenses Included In Asset Valuation"

    EXPENSES_INCLUDED_IN_VALUATION = "Expenses Included In Valuation"

    FIXED_ASSET = "Fixed Asset"

    INCOME_ACCOUNT = "Income Account"

    INDIRECT_EXPENSE = "Indirect Expense"

    INDIRECT_INCOME = "Indirect Income"

    LIABILITY = "Liability"

    PAYABLE = "Payable"

    RECEIVABLE = "Receivable"

    ROUND_OFF = "Round Off"

    ROUND_OFF_FOR_OPENING = "Round Off for Opening"

    STOCK = "Stock"

    STOCK_ADJUSTMENT = "Stock Adjustment"

    STOCK_RECEIVED_BUT_NOT_BILLED = "Stock Received But Not Billed"

    STOCK_DELIVERED_BUT_NOT_BILLED = "Stock Delivered But Not Billed"

    SERVICE_RECEIVED_BUT_NOT_BILLED = "Service Received But Not Billed"

    TAX = "Tax"

    TEMPORARY = "Temporary"





#: Port of the ternary in ``Account.set_root_and_report_type``:

#:     "Balance Sheet" if root_type in ("Asset", "Liability", "Equity") else "Profit and Loss"

ROOT_TYPE_TO_REPORT_TYPE: dict[RootType, ReportType] = {

    RootType.ASSET: ReportType.BALANCE_SHEET,

    RootType.LIABILITY: ReportType.BALANCE_SHEET,

    RootType.EQUITY: ReportType.BALANCE_SHEET,

    RootType.INCOME: ReportType.PROFIT_AND_LOSS,

    RootType.EXPENSE: ReportType.PROFIT_AND_LOSS,

}





#: Account types that may only appear on a parent (never on a child of a parent

#: carrying the same type). Ported from ``validate_parent_child_account_type``.

PARENT_ONLY_ACCOUNT_TYPES: frozenset[AccountType] = frozenset(

    {

        AccountType.DIRECT_INCOME,

        AccountType.INDIRECT_INCOME,

        AccountType.CURRENT_ASSET,

        AccountType.CURRENT_LIABILITY,

        AccountType.DIRECT_EXPENSE,

        AccountType.INDIRECT_EXPENSE,

    }

)



#: Account types whose change away is only a warning once GL entries exist

#: (``validate_receivable_payable_account_type``).

RECEIVABLE_PAYABLE_TYPES: frozenset[AccountType] = frozenset(

    {AccountType.RECEIVABLE, AccountType.PAYABLE}

)
