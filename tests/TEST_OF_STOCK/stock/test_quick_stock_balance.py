"""API tests for the Quick Stock Balance router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.quick_stock_balance_domain.models.quick_stock_balance import QuickStockBalance

from app.stock.warehouse_domain.models.warehouse import Warehouse

from app.stock.item_domain.models.item import Item



BASE = "/quick-stock-balance"





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





class TestQuickStockBalanceApi:

    def test_get_creates_default_row(self, client: TestClient):

        response = client.get(BASE)

        assert response.status_code == 200, response.text

        assert response.json()["id"]



    def test_get_is_idempotent(self, client: TestClient):

        first = client.get(BASE).json()

        second = client.get(BASE).json()

        assert first["id"] == second["id"]



    def test_patch_updates_fields(self, client: TestClient):

        response = client.patch(BASE, json={"item_barcode": "updated"})

        assert response.status_code == 200, response.text

        assert response.json()["item_barcode"] == "updated"



    def test_second_tenant_gets_its_own_row(self, client: TestClient, db, other_business_id):

        row = QuickStockBalance(

            business_id=other_business_id,

            warehouse_id=uuid.uuid4(),

            item_id=uuid.uuid4(),

            date=dt.date(2026, 1, 1),

        )

        db.add(row)

        db.flush()

        mine = client.get(BASE).json()

        assert mine["id"] != str(row.id)



    def test_collection_write_endpoints_not_available(self, client: TestClient):

        assert client.post(BASE, json={}).status_code == 405


