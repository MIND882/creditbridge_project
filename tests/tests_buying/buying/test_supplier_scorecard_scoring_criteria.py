"""API tests for the Supplier Scorecard Scoring Criteria router (buying).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.buying.supplier_scorecard_scoring_criteria_domain.models.supplier_scorecard_scoring_criteria import SupplierScorecardScoringCriteria

from app.buying.supplier_scorecard_criteria_domain.models.supplier_scorecard_criteria import SupplierScorecardCriteria



BASE = "/supplier-scorecard-scoring-criteria"





def _seed_supplier_scorecard_criteria(db, business_id) -> str:

    """One SupplierScorecardCriteria row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = SupplierScorecardCriteria(

        business_id=business_id,

        name=_seed_name,

        criteria_name=_seed_name,

        max_score=1,

        formula="seed value",

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestSupplierScorecardScoringCriteriaApi:

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

        "period": 'Per Week',

        "weighting_function": "test-weighting_function",

        }

        payload["criteria"] = [

            {

            "criteria_name_id": _seed_supplier_scorecard_criteria(db, business_id),

            "weight": 1,

            },

            {

            "criteria_name_id": _seed_supplier_scorecard_criteria(db, business_id),

            "weight": 1,

            },

        ]

        response = client.post("/supplier-scorecard", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = SupplierScorecardScoringCriteria(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            criteria_name_id=uuid.uuid4(),

            weight=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


