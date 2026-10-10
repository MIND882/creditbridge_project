"""API tests for the Item router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.item_domain.models.item import Item

from app.stock.item_group_domain.models.item_group import ItemGroup

from app.stock.uom_domain.models.uom import Uom

from app.stock.warehouse_domain.models.warehouse import Warehouse

from app.stock.item_attribute_domain.models.item_attribute import ItemAttribute

from app.accounts.item_tax_template_domain.models.item_tax_template import ItemTaxTemplate



BASE = "/item"





def _seed_item_group(db, business_id) -> str:

    """One ItemGroup row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = ItemGroup(

        business_id=business_id,

        name=_seed_name,

        item_group_name=_seed_name,

        is_group=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_uom(db, business_id) -> str:

    """One Uom row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = Uom(

        business_id=business_id,

        name=_seed_name,

        uom_name=_seed_name,

        must_be_whole_number=False,

        enabled=False,

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



def _seed_item_attribute(db, business_id) -> str:

    """One ItemAttribute row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = ItemAttribute(

        business_id=business_id,

        name=_seed_name,

        attribute_name=_seed_name,

        numeric_values=False,

        disabled=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)



def _seed_item_tax_template(db, business_id) -> str:

    """One ItemTaxTemplate row so required FKs have a referent."""

    row = ItemTaxTemplate(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        title="seed value",

        disabled=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "item_code": "test-item_code",

        "item_group_id": _seed_item_group(db, business_id),

        "stock_uom_id": _seed_uom(db, business_id),

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestItemApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"] == "test-item_code"



    def test_children_round_trip_idx_ordered(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id, barcodes=[

            {

            "barcode": "test-barcode",

            },

            {

            "barcode": "test-barcode",

            },

        ])

        assert [x["idx"] for x in row["barcodes"]] == [1, 2]

        client.patch(f'{BASE}/{row["id"]}', json={"barcodes": []})

        body = client.get(f'{BASE}/{row["id"]}').json()

        assert body["barcodes"] == []



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

        payload.pop("item_code", None)

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        _other_name = "other-item_code"

        row = Item(

            business_id=other_business_id,

            name=_other_name,

            item_code=_other_name,

            item_group_id=uuid.uuid4(),

            stock_uom_id=uuid.uuid4(),

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

        _create(client, db, business_id, **{"item_code": "row-1"})

        _create(client, db, business_id, **{"item_code": "row-2"})

        assert client.get(BASE).json()["total"] == 2

        page = client.get(BASE, params={"limit": 1}).json()

        assert page["limit"] == 1

        assert len(page["items"]) == 1

        assert page["has_more"] is True

        assert page["total"] == 2


