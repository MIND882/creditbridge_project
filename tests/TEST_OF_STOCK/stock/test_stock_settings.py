"""API tests for the Stock Settings router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.stock_settings_domain.models.stock_settings import StockSettings

BASE = "/stock-settings"







class TestStockSettingsApi:

    def test_get_creates_default_row(self, client: TestClient):

        response = client.get(BASE)

        assert response.status_code == 200, response.text

        assert response.json()["id"]



    def test_get_is_idempotent(self, client: TestClient):

        first = client.get(BASE).json()

        second = client.get(BASE).json()

        assert first["id"] == second["id"]



    def test_patch_updates_fields(self, client: TestClient):

        response = client.patch(BASE, json={"naming_series_prefix": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["naming_series_prefix"] == "updated"



    def test_second_tenant_gets_its_own_row(self, client: TestClient, db, other_business_id):

        row = StockSettings(

            business_id=other_business_id,

        )

        db.add(row)

        db.flush()

        mine = client.get(BASE).json()

        assert mine["id"] != str(row.id)



    def test_collection_write_endpoints_not_available(self, client: TestClient):

        assert client.post(BASE, json={}).status_code == 405


