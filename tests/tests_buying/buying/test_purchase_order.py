"""API tests for the Purchase Order router (buying).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.buying.purchase_order_domain.models.purchase_order import PurchaseOrder

from app.buying.supplier_domain.models.supplier import Supplier

from app.stock.item_domain.models.item import Item

from app.stock.uom_domain.models.uom import Uom



BASE = "/purchase-order"





def _seed_supplier(db, business_id) -> str:

    """One Supplier row so required FKs have a referent."""

    row = Supplier(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        supplier_name="seed value",

        is_transporter=False,

        is_internal_supplier=False,

        supplier_type='Company',

        disabled=False,

        warn_rfqs=False,

        warn_pos=False,

        prevent_rfqs=False,

        prevent_pos=False,

        on_hold=False,

        is_frozen=False,

        allow_purchase_invoice_creation_without_purchase_order=False,

        allow_purchase_invoice_creation_without_purchase_receipt=False,

        restrict_to_companies=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_item(db, business_id) -> str:

    """One Item row so required FKs have a referent."""

    row = Item(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        item_code="seed value",

        item_group_id=uuid.uuid4(),

        stock_uom_id=uuid.uuid4(),

        disabled=False,

        allow_alternative_item=False,

        is_stock_item=False,

        include_item_in_manufacturing=False,

        is_fixed_asset=False,

        has_batch_no=False,

        create_new_batch=False,

        has_expiry_date=False,

        retain_sample=False,

        has_serial_no=False,

        has_variants=False,

        is_purchase_item=False,

        is_customer_provided_item=False,

        delivered_by_supplier=False,

        is_sales_item=False,

        enable_deferred_revenue=False,

        enable_deferred_expense=False,

        inspection_required_before_purchase=False,

        inspection_required_before_delivery=False,

        is_sub_contracted_item=False,

        auto_create_assets=False,

        grant_commission=False,

        is_grouped_asset=False,

        allow_negative_stock=False,

        restrict_to_companies=False,

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





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "naming_series": 'PUR-ORD-.YYYY.-',

        "supplier_id": _seed_supplier(db, business_id),

        "company": "test-company",

        "transaction_date": "2026-01-01",

        "currency": "test-currency",

        "conversion_rate": 1,

        "status": 'Draft',

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestPurchaseOrderApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"]

        assert row["docstatus"] == 0



    def test_children_round_trip_idx_ordered(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id, items=[

            {

            "item_code_id": _seed_item(db, business_id),

            "item_name": "test-item_name",

            "schedule_date": "2026-01-01",

            "qty": 1,

            "stock_uom_id": _seed_uom(db, business_id),

            "uom_id": _seed_uom(db, business_id),

            "conversion_factor": 1,

            "base_rate": 1,

            "base_amount": 1,

            },

            {

            "item_code_id": _seed_item(db, business_id),

            "item_name": "test-item_name",

            "schedule_date": "2026-01-01",

            "qty": 1,

            "stock_uom_id": _seed_uom(db, business_id),

            "uom_id": _seed_uom(db, business_id),

            "conversion_factor": 1,

            "base_rate": 1,

            "base_amount": 1,

            },

        ])

        assert [x["idx"] for x in row["items"]] == [1, 2]

        client.patch(f'{BASE}/{row["id"]}', json={"items": []})

        body = client.get(f'{BASE}/{row["id"]}').json()

        assert body["items"] == []



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

        payload.pop("naming_series", None)

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        row = PurchaseOrder(

            business_id=other_business_id,

            name="other-tenant",

            naming_series='PUR-ORD-.YYYY.-',

            supplier_id=uuid.uuid4(),

            company="seed value",

            transaction_date=dt.date(2026, 1, 1),

            currency="seed value",

            conversion_rate=1,

            status='Draft',

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_update_changes_field(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.patch(f'{BASE}/{row["id"]}', json={"title": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["title"] == "updated"



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


