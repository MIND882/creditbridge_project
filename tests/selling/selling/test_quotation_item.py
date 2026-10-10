"""API tests for the Quotation Item router (selling).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.selling.quotation_item_domain.models.quotation_item import QuotationItem

from app.stock.price_list_domain.models.price_list import PriceList

from app.stock.uom_domain.models.uom import Uom



BASE = "/quotation-item"





def _seed_price_list(db, business_id) -> str:

    """One PriceList row so required FKs have a referent."""

    row = PriceList(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        enabled=False,

        price_list_name="seed value",

        currency="seed value",

        buying=False,

        selling=False,

        price_not_uom_dependent=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_uom(db, business_id) -> str:

    """One Uom row so required FKs have a referent."""

    row = Uom(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        uom_name="seed value",

        must_be_whole_number=False,

        enabled=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestQuotationItemApi:

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

        "naming_series": 'SAL-QTN-.YYYY.-',

        "quotation_to": "test-quotation_to",

        "transaction_date": "2026-01-01",

        "order_type": 'Sales',

        "company": "test-company",

        "currency": "test-currency",

        "conversion_rate": 1,

        "selling_price_list_id": _seed_price_list(db, business_id),

        "price_list_currency": "test-price_list_currency",

        "plc_conversion_rate": 1,

        "status": 'Draft',

        }

        payload["items"] = [

            {

            "item_name": "test-item_name",

            "qty": 1,

            "uom_id": _seed_uom(db, business_id),

            "conversion_factor": 1,

            "ordered_qty": 1,

            },

            {

            "item_name": "test-item_name",

            "qty": 1,

            "uom_id": _seed_uom(db, business_id),

            "conversion_factor": 1,

            "ordered_qty": 1,

            },

        ]

        response = client.post("/quotation", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = QuotationItem(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            item_name="seed value",

            qty=1,

            uom_id=uuid.uuid4(),

            conversion_factor=1,

            ordered_qty=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


