"""API tests for the Sales Order Item router (selling).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.selling.sales_order_item_domain.models.sales_order_item import SalesOrderItem

from app.selling.customer_domain.models.customer import Customer

from app.stock.price_list_domain.models.price_list import PriceList

from app.stock.item_domain.models.item import Item

from app.stock.uom_domain.models.uom import Uom



BASE = "/sales-order-item"





def _seed_customer(db, business_id) -> str:

    """One Customer row so required FKs have a referent."""

    row = Customer(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        customer_name="seed value",

        customer_type='Company',

        is_internal_customer=False,

        restrict_to_companies=False,

        so_required=False,

        dn_required=False,

        disabled=False,

        is_frozen=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_price_list(db, business_id) -> str:

    """One PriceList row so required FKs have a referent."""

    row = PriceList(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        enabled=False,

        price_list_name="seed value",

        currency="seed value",

        buying=False,

        selling=False,

        price_not_uom_dependent=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_item(db, business_id) -> str:

    """One Item row so required FKs have a referent."""

    row = Item(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        item_code="seed value",

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



def _seed_uom(db, business_id) -> str:

    """One Uom row so required FKs have a referent."""

    row = Uom(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        uom_name="seed value",

        must_be_whole_number=False,

        enabled=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestSalesOrderItemApi:

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

        "company": "test-company",

        "naming_series": 'SAL-ORD-.YYYY.-',

        "customer_id": _seed_customer(db, business_id),

        "order_type": 'Sales',

        "transaction_date": "2026-01-01",

        "currency": "test-currency",

        "conversion_rate": 1,

        "selling_price_list_id": _seed_price_list(db, business_id),

        "price_list_currency": "test-price_list_currency",

        "plc_conversion_rate": 1,

        "status": 'Draft',

        }

        payload["items"] = [

            {

            "item_code_id": _seed_item(db, business_id),

            "item_name": "test-item_name",

            "qty": 1,

            "uom_id": _seed_uom(db, business_id),

            "conversion_factor": 1,

            },

            {

            "item_code_id": _seed_item(db, business_id),

            "item_name": "test-item_name",

            "qty": 1,

            "uom_id": _seed_uom(db, business_id),

            "conversion_factor": 1,

            },

        ]

        response = client.post("/sales-order", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = SalesOrderItem(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            item_code_id=uuid.uuid4(),

            item_name="seed value",

            qty=1,

            uom_id=uuid.uuid4(),

            conversion_factor=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


