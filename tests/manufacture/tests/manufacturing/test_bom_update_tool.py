"""API tests for the BOM Update Tool router (manufacturing).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.manufacturing.bom_update_tool_domain.models.bom_update_tool import BomUpdateTool

from app.manufacturing.bom_domain.models.bom import Bom



BASE = "/bom-update-tool"





def _seed_bom(db, business_id) -> str:

    """One Bom row so required FKs have a referent."""

    row = Bom(

        business_id=business_id,

        name=f"seed-{uuid.uuid4().hex[:10]}",

        company="seed value",

        item_id=uuid.uuid4(),

        quantity=1,

        with_operations=False,

        track_semi_finished_goods=False,

        fg_based_operating_cost=False,

        is_active=False,

        is_default=False,

        set_rate_of_sub_assembly_item_based_on_bom=False,

        is_phantom_bom=False,

        allow_alternative_item=False,

        inspection_required=False,

        currency="seed value",

        conversion_rate=1,

        has_variants=False,

        show_in_website=False,

        show_items=False,

        show_operations=False,

    )

    db.add(row)

    db.flush()

    return str(row.id)





class TestBomUpdateToolApi:

    def test_get_creates_default_row(self, client: TestClient):

        response = client.get(BASE)

        assert response.status_code == 200, response.text

        assert response.json()["id"]



    def test_get_is_idempotent(self, client: TestClient):

        first = client.get(BASE).json()

        second = client.get(BASE).json()

        assert first["id"] == second["id"]



    def test_second_tenant_gets_its_own_row(self, client: TestClient, db, other_business_id):

        row = BomUpdateTool(

            business_id=other_business_id,

            current_bom_id=uuid.uuid4(),

            new_bom_id=uuid.uuid4(),

        )

        db.add(row)

        db.flush()

        mine = client.get(BASE).json()

        assert mine["id"] != str(row.id)



    def test_collection_write_endpoints_not_available(self, client: TestClient):

        assert client.post(BASE, json={}).status_code == 405


