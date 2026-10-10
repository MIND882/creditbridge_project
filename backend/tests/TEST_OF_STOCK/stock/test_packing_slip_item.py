"""API tests for the Packing Slip Item router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.packing_slip_item_domain.models.packing_slip_item import PackingSlipItem

from app.stock.delivery_note_domain.models.delivery_note import DeliveryNote

from app.stock.item_domain.models.item import Item



BASE = "/packing-slip-item"





def _seed_delivery_note(db, business_id) -> str:

    """One DeliveryNote row so required FKs have a referent."""

    row = DeliveryNote(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        naming_series='MAT-DN-.YYYY.-',

        customer="seed value",

        company="seed value",

        posting_date=dt.date(2026, 1, 1),

        posting_time=dt.time(0, 0),

        set_posting_time=False,

        is_return=False,

        issue_credit_note=False,

        currency="seed value",

        conversion_rate=1,

        selling_price_list_id=uuid.uuid4(),

        price_list_currency="seed value",

        plc_conversion_rate=1,

        ignore_pricing_rule=False,

        print_without_amount=False,

        group_same_items=False,

        status='Draft',

        is_internal_customer=False,

        disable_rounded_total=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_item(db, business_id) -> str:

    """One Item row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = Item(

        business_id=business_id,

        name=_seed_name,

        item_code=_seed_name,

        item_group_id=uuid.uuid4(),

        stock_uom_id=uuid.uuid4(),

        disabled=False,

        allow_alternative_item=False,

        is_stock_item=False,

        include_item_in_manufacturing=False,

        is_fixed_asset=False,

        has_batch_no=False,

        create_new_batch=False,

        has_expiry_date=False,

        retain_sample=False,

        has_serial_no=False,

        has_variants=False,

        is_purchase_item=False,

        is_customer_provided_item=False,

        delivered_by_supplier=False,

        is_sales_item=False,

        enable_deferred_revenue=False,

        enable_deferred_expense=False,

        inspection_required_before_purchase=False,

        inspection_required_before_delivery=False,

        is_sub_contracted_item=False,

        auto_create_assets=False,

        grant_commission=False,

        is_grouped_asset=False,

        allow_negative_stock=False,

        restrict_to_companies=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestPackingSlipItemApi:

    def test_empty_list_envelope(self, client: TestClient):

        body = client.get(BASE).json()

        assert body["total"] == 0

        assert body["items"] == []



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_write_endpoints_not_available(self, client: TestClient):

        assert client.post(BASE, json={}).status_code == 405

        assert client.delete(f"{BASE}/{uuid.uuid4()}").status_code == 405



    def test_rows_are_written_through_the_parent(self, client: TestClient, db, business_id):

        payload = {

        "delivery_note_id": _seed_delivery_note(db, business_id),

        "naming_series": 'MAT-PAC-.YYYY.-',

        "from_case_no": 1,

        }

        payload["items"] = [

            {

            "item_code_id": _seed_item(db, business_id),

            "qty": 1,

            },

            {

            "item_code_id": _seed_item(db, business_id),

            "qty": 1,

            },

        ]

        response = client.post("/packing-slip", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = PackingSlipItem(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            item_code_id=uuid.uuid4(),

            qty=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


