"""Business logic for Shipment -- port of

``erpnext/stock/doctype/shipment/shipment.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 4 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.shipment_domain.models.shipment import Shipment

from app.stock.shipment_domain.repositories.shipment_repository import (

    ShipmentRepository,

)

from app.stock.shipment_domain.schemas.shipment import (

    ShipmentCreate,

    ShipmentUpdate,

)

from app.stock.shipment_parcel_domain.models.shipment_parcel import ShipmentParcel

from app.stock.shipment_delivery_note_domain.models.shipment_delivery_note import ShipmentDeliveryNote

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["ShipmentService"]





class ShipmentService:

    def __init__(self, repository: Optional[ShipmentRepository] = None) -> None:

        self.repository = repository or ShipmentRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Shipment:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipment", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Shipment

    ) -> None:

        """

        Upstream has 4 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Shipment:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Shipment]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Shipment].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``SHIPMENT-.#####``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(Shipment).where(

                    Shipment.business_id == business_id

                )

            )

            or 0

        )

        return f"SHIPMENT-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ShipmentCreate

    ) -> Shipment:

        row = Shipment(

            business_id=business_id,

            name=self.next_name(db, business_id),

            pickup_from_type=payload.pickup_from_type,

            pickup_company=payload.pickup_company,

            pickup_customer=payload.pickup_customer,

            pickup_supplier=payload.pickup_supplier,

            pickup=payload.pickup,

            pickup_address_name=payload.pickup_address_name,

            pickup_address=payload.pickup_address,

            pickup_contact_name=payload.pickup_contact_name,

            pickup_contact_email=payload.pickup_contact_email,

            pickup_contact=payload.pickup_contact,

            delivery_to_type=payload.delivery_to_type,

            delivery_company=payload.delivery_company,

            delivery_customer=payload.delivery_customer,

            delivery_supplier=payload.delivery_supplier,

            delivery_to=payload.delivery_to,

            delivery_address_name=payload.delivery_address_name,

            delivery_address=payload.delivery_address,

            delivery_contact_name=payload.delivery_contact_name,

            delivery_contact_email=payload.delivery_contact_email,

            delivery_contact=payload.delivery_contact,

            parcel_template_id=payload.parcel_template_id,

            pallets=payload.pallets,

            value_of_goods=payload.value_of_goods,

            pickup_date=payload.pickup_date,

            pickup_from=payload.pickup_from,

            pickup_to=payload.pickup_to,

            shipment_type=payload.shipment_type,

            pickup_type=payload.pickup_type,

            description_of_content=payload.description_of_content,

            service_provider=payload.service_provider,

            shipment_id=payload.shipment_id,

            shipment_amount=payload.shipment_amount,

            status=payload.status,

            tracking_url=payload.tracking_url,

            carrier=payload.carrier,

            carrier_service=payload.carrier_service,

            awb_number=payload.awb_number,

            tracking_status=payload.tracking_status,

            tracking_status_info=payload.tracking_status_info,

            amended_from_id=payload.amended_from_id,

            incoterm=payload.incoterm,

            pickup_contact_person=payload.pickup_contact_person,

            total_weight=payload.total_weight,

        )

        self._replace_shipment_parcel(business_id, row, [x.model_dump() for x in payload.shipment_parcel])

        self._replace_shipment_delivery_note(business_id, row, [x.model_dump() for x in payload.shipment_delivery_note])



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        row_id: uuid.UUID,

        payload: ShipmentUpdate,

    ) -> Shipment:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "shipment_parcel":

                    self._replace_shipment_parcel(business_id, row, value or [])

                    continue

                if field_name == "shipment_delivery_note":

                    self._replace_shipment_delivery_note(business_id, row, value or [])

                    continue

                setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Shipment:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Shipment")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Shipment:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Shipment")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_shipment_parcel(

        self, business_id: uuid.UUID, row: Shipment, shipment_parcel: list[dict]

    ) -> None:

        row.shipment_parcel.clear()

        for idx, entry in enumerate(shipment_parcel, start=1):

            row.shipment_parcel.append(

                ShipmentParcel(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_shipment_delivery_note(

        self, business_id: uuid.UUID, row: Shipment, shipment_delivery_note: list[dict]

    ) -> None:

        row.shipment_delivery_note.clear()

        for idx, entry in enumerate(shipment_delivery_note, start=1):

            row.shipment_delivery_note.append(

                ShipmentDeliveryNote(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
