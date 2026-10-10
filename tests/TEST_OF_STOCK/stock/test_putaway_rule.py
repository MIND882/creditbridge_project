"""API tests for the Putaway Rule router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.putaway_rule_domain.models.putaway_rule import PutawayRule

from app.stock.item_domain.models.item import Item

from app.stock.warehouse_domain.models.warehouse import Warehouse



BASE = "/putaway-rule"





def _seed_item(db, business_id) -> str:

    """One Item row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = Item(

        business_id=business_id,

        name=_seed_name,

        item_code=_seed_name,

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



def _seed_warehouse(db, business_id) -> str:

    """One Warehouse row so required FKs have a referent."""

    row = Warehouse(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        warehouse_name="seed value",

        is_group=False,

        company="seed value",

        disabled=False,

        is_rejected_warehouse=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "item_code_id": _seed_item(db, business_id),

        "warehouse_id": _seed_warehouse(db, business_id),

        "capacity": 1,

        "company": "test-company",

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestPutawayRuleApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"]



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

        payload.pop("capacity", None)

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        row = PutawayRule(

            business_id=other_business_id,

            name="other-tenant",

            item_code_id=uuid.uuid4(),

            warehouse_id=uuid.uuid4(),

            capacity=1,

            company="seed value",

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_update_changes_field(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        response = client.patch(f'{BASE}/{row["id"]}', json={"item_name": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["item_name"] == "updated"



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


