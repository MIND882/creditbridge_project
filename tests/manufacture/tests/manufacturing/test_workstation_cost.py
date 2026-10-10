"""API tests for the Workstation Cost router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.workstation_cost_domain.models.workstation_cost import WorkstationCost

from app.manufacturing.workstation_operating_component_domain.models.workstation_operating_component import WorkstationOperatingComponent



BASE = "/workstation-cost"





def _seed_workstation_operating_component(db, business_id) -> str:

    """One WorkstationOperatingComponent row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = WorkstationOperatingComponent(

        business_id=business_id,

        name=_seed_name,

        component_name=_seed_name,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestWorkstationCostApi:

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

        "production_capacity": 1,

        "workstation_name": "test-workstation_name",

        }

        payload["workstation_costs"] = [

            {

            "operating_component_id": _seed_workstation_operating_component(db, business_id),

            "operating_cost": 1,

            },

            {

            "operating_component_id": _seed_workstation_operating_component(db, business_id),

            "operating_cost": 1,

            },

        ]

        response = client.post("/workstation", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = WorkstationCost(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            operating_component_id=uuid.uuid4(),

            operating_cost=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


