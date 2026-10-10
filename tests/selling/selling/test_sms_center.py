"""API tests for the SMS Center router (selling).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.selling.sms_center_domain.models.sms_center import SmsCenter

BASE = "/sms-center"







class TestSmsCenterApi:

    def test_get_creates_default_row(self, client: TestClient):

        response = client.get(BASE)

        assert response.status_code == 200, response.text

        assert response.json()["id"]



    def test_get_is_idempotent(self, client: TestClient):

        first = client.get(BASE).json()

        second = client.get(BASE).json()

        assert first["id"] == second["id"]



    def test_patch_updates_fields(self, client: TestClient):

        response = client.patch(BASE, json={"receiver_list": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["receiver_list"] == "updated"



    def test_second_tenant_gets_its_own_row(self, client: TestClient, db, other_business_id):

        row = SmsCenter(

            business_id=other_business_id,

            message="seed value",

        )

        db.add(row)

        db.flush()

        mine = client.get(BASE).json()

        assert mine["id"] != str(row.id)



    def test_collection_write_endpoints_not_available(self, client: TestClient):

        assert client.post(BASE, json={}).status_code == 405


