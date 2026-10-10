"""

Enums shared by the tax-template doctypes.



ERPNext repeats the same ``charge_type`` Select across Sales Taxes and Charges,

Purchase Taxes and Charges and Advance Taxes and Charges. One enum here keeps the

three models from drifting apart.

"""



from __future__ import annotations



import enum



__all__ = ["ChargeType", "PurchaseTaxCategory", "AddDeductTax", "TaxRuleType"]





class ChargeType(str, enum.Enum):

    """How a tax row computes its amount. Shared by all three tax child tables."""



    ACTUAL = "Actual"

    ON_NET_TOTAL = "On Net Total"

    ON_PREVIOUS_ROW_AMOUNT = "On Previous Row Amount"

    ON_PREVIOUS_ROW_TOTAL = "On Previous Row Total"

    ON_PAID_AMOUNT = "On Paid Amount"





class PurchaseTaxCategory(str, enum.Enum):

    """Purchase-only: whether the charge is capitalised into stock valuation."""



    VALUATION_AND_TOTAL = "Valuation and Total"

    VALUATION = "Valuation"

    TOTAL = "Total"





class AddDeductTax(str, enum.Enum):

    ADD = "Add"

    DEDUCT = "Deduct"





class TaxRuleType(str, enum.Enum):

    SALES = "Sales"

    PURCHASE = "Purchase"
