"""API tests for the Shipment Parcel router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.shipment_parcel_domain.models.shipment_parcel import ShipmentParcel

from app.stock.delivery_note_domain.models.delivery_note import DeliveryNote



BASE = "/shipment-parcel"





def _seed_delivery_note(db, business_id) -> str:

    """One DeliveryNote row so required FKs have a referent."""

    row = DeliveryNote(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        naming_series='MAT-DN-.YYYY.-',

        customer="seed value",

        company="seed value",

        posting_date=dt.date(2026, 1, 1),

        posting_time=dt.time(0, 0),

        set_posting_time=False,

        is_return=False,

        issue_credit_note=False,

        currency="seed value",

        conversion_rate=1,

        selling_price_list_id=uuid.uuid4(),

        price_list_currency="seed value",

        plc_conversion_rate=1,

        ignore_pricing_rule=False,

        print_without_amount=False,

        group_same_items=False,

        status='Draft',

        is_internal_customer=False,

        disable_rounded_total=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestShipmentParcelApi:

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

        "pickup_address_name": "test-pickup_address_name",

        "delivery_address_name": "test-delivery_address_name",

        "value_of_goods": 1,

        "pickup_date": "2026-01-01",

        "pickup_from": "00:00:00",

        "pickup_to": "00:00:00",

        "description_of_content": "test-description_of_content",

        }

        payload["shipment_parcel"] = [

            {

            "weight": 1,

            "count": 1,

            },

            {

            "weight": 1,

            "count": 1,

            },

        ]

        response = client.post("/shipment", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = ShipmentParcel(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            weight=1,

            count=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


