"""API tests for the Quality Inspection Template router (stock).



Runs through ``TestClient``: schema validation, the tenancy dependency,

and the ``DomainValidationError`` code -> HTTP mapping.

"""



import datetime as dt

import uuid



from fastapi.testclient import TestClient



from app.stock.quality_inspection_template_domain.models.quality_inspection_template import QualityInspectionTemplate

from app.stock.quality_inspection_parameter_domain.models.quality_inspection_parameter import QualityInspectionParameter



BASE = "/quality-inspection-template"





def _seed_quality_inspection_parameter(db, business_id) -> str:

    """One QualityInspectionParameter row so required FKs have a referent."""

    _seed_name = f"seed-{uuid.uuid4().hex[:10]}"

    row = QualityInspectionParameter(

        business_id=business_id,

        name=_seed_name,

        parameter=_seed_name,

    )

    db.add(row)

    db.flush()

    return str(row.id)





def _payload(db, business_id, **overrides) -> dict:

    payload = {

        "quality_inspection_template_name": "test-quality_inspection_template_name",

    }

    payload.update(overrides)

    return payload





def _create(client: TestClient, db, business_id, **overrides) -> dict:

    response = client.post(BASE, json=_payload(db, business_id, **overrides))

    assert response.status_code == 201, response.text

    return response.json()





class TestQualityInspectionTemplateApi:

    def test_create_returns_201_and_defaults(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert row["id"]

        assert row["name"] == "test-quality_inspection_template_name"



    def test_children_round_trip_idx_ordered(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id, item_quality_inspection_parameter=[

            {

            "specification_id": _seed_quality_inspection_parameter(db, business_id),

            },

            {

            "specification_id": _seed_quality_inspection_parameter(db, business_id),

            },

        ])

        assert [x["idx"] for x in row["item_quality_inspection_parameter"]] == [1, 2]

        client.patch(f'{BASE}/{row["id"]}', json={"item_quality_inspection_parameter": []})

        body = client.get(f'{BASE}/{row["id"]}').json()

        assert body["item_quality_inspection_parameter"] == []



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

        payload.pop("quality_inspection_template_name", None)

        response = client.post(BASE, json=payload)

        assert response.status_code == 422



    def test_get_missing_returns_404(self, client: TestClient):

        response = client.get(f"{BASE}/{uuid.uuid4()}")

        assert response.status_code == 404



    def test_other_tenants_row_is_invisible(self, client: TestClient, db, business_id, other_business_id):

        _other_name = "other-quality_inspection_template_name"

        row = QualityInspectionTemplate(

            business_id=other_business_id,

            name=_other_name,

            quality_inspection_template_name=_other_name,

        )

        db.add(row)

        db.flush()

        assert client.get(f"{BASE}/{row.id}").status_code == 404



    def test_delete_returns_204_then_404(self, client: TestClient, db, business_id):

        row = _create(client, db, business_id)

        assert client.delete(f"{BASE}/{row['id']}").status_code == 204

        assert client.get(f"{BASE}/{row['id']}").status_code == 404



    def test_list_envelope_and_pagination(self, client: TestClient, db, business_id):

        _create(client, db, business_id, **{"quality_inspection_template_name": "row-1"})

        _create(client, db, business_id, **{"quality_inspection_template_name": "row-2"})

        assert client.get(BASE).json()["total"] == 2

        page = client.get(BASE, params={"limit": 1}).json()

        assert page["limit"] == 1

        assert len(page["items"]) == 1

        assert page["has_more"] is True

        assert page["total"] == 2


