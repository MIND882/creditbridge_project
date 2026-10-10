"""API tests for the Supplier Scorecard Period router (buying).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.buying.supplier_scorecard_period_domain.models.supplier_scorecard_period import SupplierScorecardPeriod

from app.buying.supplier_domain.models.supplier import Supplier

from app.buying.supplier_scorecard_domain.models.supplier_scorecard import SupplierScorecard

from app.buying.supplier_scorecard_variable_domain.models.supplier_scorecard_variable import SupplierScorecardVariable



BASE = "/supplier-scorecard-period"





def _seed_supplier(db, business_id) -> str:

    """One Supplier row so required FKs have a referent."""

    row = Supplier(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        supplier_name="seed value",

        is_transporter=False,

        is_internal_supplier=False,

        supplier_type='Company',

        disabled=False,

        warn_rfqs=False,

        warn_pos=False,

        prevent_rfqs=False,

        prevent_pos=False,

        on_hold=False,

        is_frozen=False,

        allow_purchase_invoice_creation_without_purchase_order=False,

        allow_purchase_invoice_creation_without_purchase_receipt=False,

        restrict_to_companies=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_supplier_scorecard(db, business_id) -> str:

    """One SupplierScorecard row so required FKs have a referent."""

    _seed_ref = uuid.uuid4()

    row = SupplierScorecard(

        business_id=business_id,

        name=str(_seed_ref),

        supplier_id=_seed_ref,

        period='Per Week',

        weighting_function="seed value",

        warn_rfqs=False,

        warn_pos=False,

        prevent_rfqs=False,

        prevent_pos=False,

        notify_supplier=False,

        notify_employee=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_supplier_scorecard_variable(db, business_id) -> str:

    """One SupplierScorecardVariable row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = SupplierScorecardVariable(

        business_id=business_id,

        name=_seed_name,

        variable_label=_seed_name,

        is_custom=False,

        param_name="seed value",

        path="seed value",

    )

    db.add(row)

    db.flush()

    return str(row.id)





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "supplier_id": _seed_supplier(db, business_id),

        "naming_series": 'PU-SSP-.YYYY.-',

        "start_date": "2026-01-01",

        "end_date": "2026-01-01",

        "scorecard_id": _seed_supplier_scorecard(db, business_id),

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestSupplierScorecardPeriodApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"]



    def test_children_round_trip_idx_ordered(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id, variables=[

            {

            "variable_label_id": _seed_supplier_scorecard_variable(db, business_id),

            },

            {

            "variable_label_id": _seed_supplier_scorecard_variable(db, business_id),

            },

        ])

        assert [x["idx"] for x in row["variables"]] == [1, 2]

        client.patch(f'{BASE}/{row["id"]}', json={"variables": []})

        body = client.get(f'{BASE}/{row["id"]}').json()

        assert body["variables"] == []



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

        row = SupplierScorecardPeriod(

            business_id=other_business_id,

            name="other-tenant",

            supplier_id=uuid.uuid4(),

            naming_series='PU-SSP-.YYYY.-',

            start_date=dt.date(2026, 1, 1),

            end_date=dt.date(2026, 1, 1),

            scorecard_id=uuid.uuid4(),

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_update_changes_field(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.patch(f'{BASE}/{row["id"]}', json={"total_score": 2})

        assert response.status_code == 200, response.text

        assert float(response.json()["total_score"]) == float(2)



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


