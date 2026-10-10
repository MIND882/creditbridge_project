"""API tests for the Purchase Receipt Item Supplied router (buying).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.buying.purchase_receipt_item_supplied_domain.models.purchase_receipt_item_supplied import PurchaseReceiptItemSupplied

BASE = "/purchase-receipt-item-supplied"







class TestPurchaseReceiptItemSuppliedApi:

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



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = PurchaseReceiptItemSupplied(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            consumed_qty=1,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


