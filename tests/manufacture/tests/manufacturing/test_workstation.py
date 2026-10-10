"""API tests for the Workstation router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.workstation_domain.models.workstation import Workstation

from app.manufacturing.workstation_operating_component_domain.models.workstation_operating_component import WorkstationOperatingComponent



BASE = "/workstation"





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





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "production_capacity": 1,

        "workstation_name": "test-workstation_name",

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestWorkstationApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"] == "test-workstation_name"



    def test_children_round_trip_idx_ordered(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id, workstation_costs=[

            {

            "operating_component_id": _seed_workstation_operating_component(db, business_id),

            "operating_cost": 1,

            },

            {

            "operating_component_id": _seed_workstation_operating_component(db, business_id),

            "operating_cost": 1,

            },

        ])

        assert [x["idx"] for x in row["workstation_costs"]] == [1, 2]

        client.patch(f'{BASE}/{row["id"]}', json={"workstation_costs": []})

        body = client.get(f'{BASE}/{row["id"]}').json()

        assert body["workstation_costs"] == []



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

        payload.pop("production_capacity", None)

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        _other_name = "other-workstation_name"

        row = Workstation(

            business_id=other_business_id,

            name=_other_name,

            workstation_name=_other_name,

            production_capacity=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_update_changes_field(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.patch(f'{BASE}/{row["id"]}', json={"workstation_name": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["workstation_name"] == "updated"



    def test_delete_returns_204_then_404(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert client.delete(f"{BASE}/{row['id']}").status_code == 204

        assert client.get(f"{BASE}/{row['id']}").status_code == 404



    def test_list_envelope_and_pagination(self, client: TestClient, db, business_id):

        _create(client, db, business_id, **{"workstation_name": "row-1"})

        _create(client, db, business_id, **{"workstation_name": "row-2"})

        assert client.get(BASE).json()["total"] == 2

        page = client.get(BASE, params={"limit": 1}).json()

        assert page["limit"] == 1

        assert len(page["items"]) == 1

        assert page["has_more"] is True

        assert page["total"] == 2


