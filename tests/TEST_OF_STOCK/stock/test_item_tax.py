"""API tests for the Item Tax router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.item_tax_domain.models.item_tax import ItemTax

from app.stock.item_group_domain.models.item_group import ItemGroup

from app.stock.uom_domain.models.uom import Uom

from app.stock.warehouse_domain.models.warehouse import Warehouse

from app.stock.item_attribute_domain.models.item_attribute import ItemAttribute

from app.accounts.item_tax_template_domain.models.item_tax_template import ItemTaxTemplate



BASE = "/item-tax"





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





class TestItemTaxApi:

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

        "item_code": "test-item_code",

        "item_group_id": _seed_item_group(db, business_id),

        "stock_uom_id": _seed_uom(db, business_id),

        }

        payload["taxes"] = [

            {

            "item_tax_template_id": _seed_item_tax_template(db, business_id),

            },

            {

            "item_tax_template_id": _seed_item_tax_template(db, business_id),

            },

        ]

        response = client.post("/item", json=payload)

        assert response.status_code == 201, response.text

        parent_id = response.json()["id"]

        body = client.get(BASE, params={"parent_id": parent_id}).json()

        assert body["total"] == 2

        assert [x["idx"] for x in body["items"]] == [1, 2]



    def test_other_tenants_child_is_invisible(self, client: TestClient, db, other_business_id):

        row = ItemTax(

            business_id=other_business_id,

            name="other-child",

            idx=1,

            item_tax_template_id=uuid.uuid4(),

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404


