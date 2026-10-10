"""API tests for the Job Card Operation router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.job_card_operation_domain.models.job_card_operation import JobCardOperation

from app.manufacturing.work_order_domain.models.work_order import WorkOrder

from app.manufacturing.operation_domain.models.operation import Operation

from app.manufacturing.workstation_domain.models.workstation import Workstation

from app.stock.item_domain.models.item import Item



BASE = "/job-card-operation"





def _seed_work_order(db, business_id) -> str:

    """One WorkOrder row so required FKs have a referent."""

    row = WorkOrder(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        company="seed value",

        naming_series='MFG-WO-.YYYY.-',

        production_item_id=uuid.uuid4(),

        bom_no_id=uuid.uuid4(),

        qty=1,

        reserve_stock=False,

        allow_alternative_item=False,

        use_multi_level_bom=False,

        skip_transfer=False,

        from_wip_warehouse=False,

        update_consumed_material_cost_in_project=False,

        planned_start_date=dt.datetime(2026, 1, 1),

        has_serial_no=False,

        has_batch_no=False,

        status='Draft',

        track_semi_finished_goods=False,

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



def _seed_workstation(db, business_id) -> str:

    """One Workstation row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = Workstation(

        business_id=business_id,

        name=_seed_name,

        workstation_name=_seed_name,

        disabled=False,

        production_capacity="seed value",

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





class TestJobCardOperationApi:

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

        "work_order_id": _seed_work_order(db, business_id),

        "company": "test-company",

        "naming_series": 'PO-JOB.#####',

        "operation_id": _seed_operation(db, business_id),

        "workstation_id": _seed_workstation(db, business_id),

        }

        payload["sub_operations"] = [

            {

            },

            {

            },

        ]

        response = client.post("/job-card", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = JobCardOperation(

            business_id=other_business_id,

            name="other-child",

            idx=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


