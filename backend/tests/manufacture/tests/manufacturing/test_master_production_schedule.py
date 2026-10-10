"""API tests for the Master Production Schedule router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.master_production_schedule_domain.models.master_production_schedule import MasterProductionSchedule

from app.selling.sales_order_domain.models.sales_order import SalesOrder

from app.stock.material_request_domain.models.material_request import MaterialRequest



BASE = "/master-production-schedule"





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





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "naming_series": 'MPS.YY.-.######',

        "company": "test-company",

        "posting_date": "2026-01-01",

        "from_date": "2026-01-01",

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestMasterProductionScheduleApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"]



    def test_children_round_trip_idx_ordered(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id, sales_orders=[

            {

            "sales_order_id": _seed_sales_order(db, business_id),

            },

            {

            "sales_order_id": _seed_sales_order(db, business_id),

            },

        ])

        assert [x["idx"] for x in row["sales_orders"]] == [1, 2]

        client.patch(f'{BASE}/{row["id"]}', json={"sales_orders": []})

        body = client.get(f'{BASE}/{row["id"]}').json()

        assert body["sales_orders"] == []



    def test_input_schema_rejects_business_id(self, client: TestClient, db, business_id):

        payload = _payload(db, business_id)

        payload["business_id"] = str(uuid.uuid4())  # tenancy comes from the token

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_unknown_field_rejected_by_schema(self, client: TestClient, db, business_id):

        payload = _payload(db, business_id)

        payload["definitely_not_a_field"] = "x"

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_required_field_missing_is_422(self, client: TestClient, db, business_id):

        payload = _payload(db, business_id)

        payload.pop("naming_series", None)

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        row = MasterProductionSchedule(

            business_id=other_business_id,

            name="other-tenant",

            naming_series='MPS.YY.-.######',

            company="seed value",

            posting_date=dt.date(2026, 1, 1),

            from_date=dt.date(2026, 1, 1),

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_update_changes_field(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.patch(f'{BASE}/{row["id"]}', json={"to_date": "2026-06-30"})

        assert response.status_code == 200, response.text

        assert response.json()["to_date"] == "2026-06-30"



    def test_delete_returns_204_then_404(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert client.delete(f"{BASE}/{row['id']}").status_code == 204

        assert client.get(f"{BASE}/{row['id']}").status_code == 404



    def test_list_envelope_and_pagination(self, client: TestClient, db, business_id):

        _create(client, db, business_id)

        _create(client, db, business_id)

        assert client.get(BASE).json()["total"] == 2

        page = client.get(BASE, params={"limit": 1}).json()

        assert page["limit"] == 1

        assert len(page["items"]) == 1

        assert page["has_more"] is True

        assert page["total"] == 2


