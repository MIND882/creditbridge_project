"""API tests for the Item Attribute Value router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.item_attribute_value_domain.models.item_attribute_value import ItemAttributeValue

BASE = "/item-attribute-value"







class TestItemAttributeValueApi:

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

        "attribute_name": "test-attribute_name",

        }

        payload["item_attribute_values"] = [

            {

            "attribute_value": "test-attribute_value",

            "abbr": "test-abbr",

            },

            {

            "attribute_value": "test-attribute_value",

            "abbr": "test-abbr",

            },

        ]

        response = client.post("/item-attribute", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = ItemAttributeValue(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            attribute_value="seed value",

            abbr="seed value",

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


