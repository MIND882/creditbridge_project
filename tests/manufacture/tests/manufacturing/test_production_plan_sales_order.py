"""API tests for the Production Plan Sales Order router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.production_plan_sales_order_domain.models.production_plan_sales_order import ProductionPlanSalesOrder

from app.selling.sales_order_domain.models.sales_order import SalesOrder

from app.stock.material_request_domain.models.material_request import MaterialRequest



BASE = "/production-plan-sales-order"





def _seed_sales_order(db, business_id) -> str:

    """One SalesOrder row so required FKs have a referent."""

    row = SalesOrder(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        company="seed value",

        naming_series='SAL-ORD-.YYYY.-',

        customer_id=uuid.uuid4(),

        order_type='Sales',

        transaction_date=dt.date(2026, 1, 1),

        skip_delivery_note=False,

        has_unit_price_items=False,

        is_subcontracted=False,

        currency="seed value",

        conversion_rate=1,

        selling_price_list_id=uuid.uuid4(),

        price_list_currency="seed value",

        plc_conversion_rate=1,

        ignore_pricing_rule=False,

        reserve_stock=False,

        disable_rounded_total=False,

        ignore_default_payment_terms_template=False,

        status='Draft',

        group_same_items=False,

        is_internal_customer=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_material_request(db, business_id) -> str:

    """One MaterialRequest row so required FKs have a referent."""

    row = MaterialRequest(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        naming_series='MAT-MR-.YYYY.-',

        material_request_type='Purchase',

        company="seed value",

        transaction_date=dt.date(2026, 1, 1),

        auto_created_via_reorder=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestProductionPlanSalesOrderApi:

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

        "naming_series": 'MPS.YY.-.######',

        "company": "test-company",

        "posting_date": "2026-01-01",

        "from_date": "2026-01-01",

        }

        payload["sales_orders"] = [

            {

            "sales_order_id": _seed_sales_order(db, business_id),

            },

            {

            "sales_order_id": _seed_sales_order(db, business_id),

            },

        ]

        response = client.post("/master-production-schedule", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = ProductionPlanSalesOrder(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            sales_order_id=uuid.uuid4(),

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


