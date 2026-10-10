"""API tests for the Work Order Additional Item router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem

from app.stock.item_domain.models.item import Item

from app.manufacturing.bom_domain.models.bom import Bom

from app.manufacturing.operation_domain.models.operation import Operation



BASE = "/work-order-additional-item"





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



def _seed_operation(db, business_id) -> str:

    """One Operation row so required FKs have a referent."""

    row = Operation(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        is_corrective_operation=False,

        create_job_card_based_on_batch_size=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestWorkOrderAdditionalItemApi:

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

        "naming_series": 'MFG-WO-.YYYY.-',

        "production_item_id": _seed_item(db, business_id),

        "bom_no_id": _seed_bom(db, business_id),

        "qty": 1,

        "planned_start_date": "2026-01-01T00:00:00",

        "status": 'Draft',

        }

        payload["non_stock_items"] = [

            {

            },

            {

            },

        ]

        response = client.post("/work-order", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = WorkOrderAdditionalItem(

            business_id=other_business_id,

            name="other-child",

            idx=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


