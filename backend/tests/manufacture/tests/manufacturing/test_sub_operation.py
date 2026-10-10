"""API tests for the Sub Operation router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.sub_operation_domain.models.sub_operation import SubOperation

from app.manufacturing.operation_domain.models.operation import Operation



BASE = "/sub-operation"





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





class TestSubOperationApi:

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

        }

        payload["sub_operations"] = [

            {

            "operation_id": _seed_operation(db, business_id),

            },

            {

            "operation_id": _seed_operation(db, business_id),

            },

        ]

        response = client.post("/operation", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = SubOperation(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            operation_id=uuid.uuid4(),

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


