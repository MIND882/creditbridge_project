"""API tests for the Production Plan Item Reference router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.production_plan_item_reference_domain.models.production_plan_item_reference import ProductionPlanItemReference

from app.stock.item_domain.models.item import Item

from app.manufacturing.bom_domain.models.bom import Bom

from app.stock.uom_domain.models.uom import Uom

from app.stock.warehouse_domain.models.warehouse import Warehouse



BASE = "/production-plan-item-reference"





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



def _seed_bom(db, business_id) -> str:

    """One Bom row so required FKs have a referent."""

    row = Bom(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        company="seed value",

        item_id=uuid.uuid4(),

        quantity=1,

        with_operations=False,

        track_semi_finished_goods=False,

        fg_based_operating_cost=False,

        is_active=False,

        is_default=False,

        set_rate_of_sub_assembly_item_based_on_bom=False,

        is_phantom_bom=False,

        allow_alternative_item=False,

        inspection_required=False,

        currency="seed value",

        conversion_rate=1,

        has_variants=False,

        show_in_website=False,

        show_items=False,

        show_operations=False,

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



def _seed_warehouse(db, business_id) -> str:

    """One Warehouse row so required FKs have a referent."""

    row = Warehouse(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        warehouse_name="seed value",

        is_group=False,

        company="seed value",

        disabled=False,

        is_rejected_warehouse=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestProductionPlanItemReferenceApi:

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

        "naming_series": 'MFG-PP-.YYYY.-',

        "company": "test-company",

        "posting_date": "2026-01-01",

        }

        payload["prod_plan_references"] = [

            {

            },

            {

            },

        ]

        response = client.post("/production-plan", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = ProductionPlanItemReference(

            business_id=other_business_id,

            name="other-child",

            idx=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


