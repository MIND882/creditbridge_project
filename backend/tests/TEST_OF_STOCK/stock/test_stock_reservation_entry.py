"""API tests for the Stock Reservation Entry router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.stock_reservation_entry_domain.models.stock_reservation_entry import StockReservationEntry

BASE = "/stock-reservation-entry"







def _payload(db, business_id, **overrides) -> dict:

    payload = {

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestStockReservationEntryApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"]

        assert row["docstatus"] == 0



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



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        row = StockReservationEntry(

            business_id=other_business_id,

            name="other-tenant",

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_update_changes_field(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.patch(f'{BASE}/{row["id"]}', json={"voucher_detail_no": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["voucher_detail_no"] == "updated"



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



    def test_submit_moves_draft_to_submitted(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.post(f"{BASE}/{row['id']}/submit")

        assert response.status_code == 200, response.text

        assert response.json()["docstatus"] == 1



    def test_submit_twice_is_rejected(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        client.post(f"{BASE}/{row['id']}/submit")

        response = client.post(f"{BASE}/{row['id']}/submit")

        assert response.status_code == 400

        assert response.json()["detail"]["code"] == "docstatus_not_draft"



    def test_cancel_requires_submitted(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.post(f"{BASE}/{row['id']}/cancel")

        assert response.status_code == 400

        assert response.json()["detail"]["code"] == "docstatus_not_submitted"



    def test_cancel_submitted_moves_to_cancelled(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        client.post(f"{BASE}/{row['id']}/submit")

        response = client.post(f"{BASE}/{row['id']}/cancel")

        assert response.status_code == 200, response.text

        assert response.json()["docstatus"] == 2



    def test_cancelled_rows_hidden_from_list_by_default(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        client.post(f"{BASE}/{row['id']}/submit")

        client.post(f"{BASE}/{row['id']}/cancel")

        assert client.get(BASE).json()["total"] == 0

        body = client.get(BASE, params={"include_cancelled": "true"}).json()

        assert body["total"] == 1


