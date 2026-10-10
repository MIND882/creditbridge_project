"""API tests for the Supplier Scorecard Scoring Variable router (buying).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.buying.supplier_scorecard_scoring_variable_domain.models.supplier_scorecard_scoring_variable import SupplierScorecardScoringVariable

from app.buying.supplier_domain.models.supplier import Supplier

from app.buying.supplier_scorecard_domain.models.supplier_scorecard import SupplierScorecard

from app.buying.supplier_scorecard_variable_domain.models.supplier_scorecard_variable import SupplierScorecardVariable



BASE = "/supplier-scorecard-scoring-variable"





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





class TestSupplierScorecardScoringVariableApi:

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

        "supplier_id": _seed_supplier(db, business_id),

        "naming_series": 'PU-SSP-.YYYY.-',

        "start_date": "2026-01-01",

        "end_date": "2026-01-01",

        "scorecard_id": _seed_supplier_scorecard(db, business_id),

        }

        payload["variables"] = [

            {

            "variable_label_id": _seed_supplier_scorecard_variable(db, business_id),

            },

            {

            "variable_label_id": _seed_supplier_scorecard_variable(db, business_id),

            },

        ]

        response = client.post("/supplier-scorecard-period", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = SupplierScorecardScoringVariable(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            variable_label_id=uuid.uuid4(),

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


