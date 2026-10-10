"""

Fixtures for the stock module tests.



Mirrors the root ``conftest.py`` conventions (in-memory SQLite over a

StaticPool, tenancy pinned to a fixed business id, FK-ordered table

creation) but scoped to the stock routers. The table set is derived from the

FK graph over every ``app.accounts.*`` / ``app.stock.*`` model, so a new

domain is picked up the moment its model is imported -- no hand-maintained

creation list to break.

"""



import os

import shutil

import sys

import tempfile

import uuid



# must precede every app.* import

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")

os.environ.setdefault("REDIS_URL", "redis://localhost:6379")

os.environ.setdefault("ENCRYPTION_KEY", "0123456789abcdef0123456789abcdef")

os.environ["DATABASE_URL"] = "sqlite:///:memory:"



sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))



import pytest  # noqa: E402

from fastapi import FastAPI  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402

from sqlalchemy import Column, Table, Uuid, create_engine  # noqa: E402

from sqlalchemy.orm import sessionmaker  # noqa: E402

from sqlalchemy.pool import StaticPool  # noqa: E402



from app.core.tenancy import get_current_business_uuid, get_db  # noqa: E402

from app.db.session import Base  # noqa: E402



from app.stock.batch_domain.api.batch import router as batch_router  # noqa: E402

from app.stock.bin_domain.api.bin import router as bin_router  # noqa: E402

from app.stock.brand_domain.api.brand import router as brand_router  # noqa: E402

from app.stock.company_restriction_domain.api.company_restriction import router as company_restriction_router  # noqa: E402

from app.stock.customs_tariff_number_domain.api.customs_tariff_number import router as customs_tariff_number_router  # noqa: E402

from app.stock.delivery_note_domain.api.delivery_note import router as delivery_note_router  # noqa: E402

from app.stock.delivery_note_item_domain.api.delivery_note_item import router as delivery_note_item_router  # noqa: E402

from app.stock.delivery_settings_domain.api.delivery_settings import router as delivery_settings_router  # noqa: E402

from app.stock.delivery_stop_domain.api.delivery_stop import router as delivery_stop_router  # noqa: E402

from app.stock.delivery_trip_domain.api.delivery_trip import router as delivery_trip_router  # noqa: E402

from app.stock.inventory_dimension_domain.api.inventory_dimension import router as inventory_dimension_router  # noqa: E402

from app.stock.item_domain.api.item import router as item_router  # noqa: E402

from app.stock.item_alternative_domain.api.item_alternative import router as item_alternative_router  # noqa: E402

from app.stock.item_attribute_domain.api.item_attribute import router as item_attribute_router  # noqa: E402

from app.stock.item_attribute_value_domain.api.item_attribute_value import router as item_attribute_value_router  # noqa: E402

from app.stock.item_barcode_domain.api.item_barcode import router as item_barcode_router  # noqa: E402

from app.stock.item_customer_detail_domain.api.item_customer_detail import router as item_customer_detail_router  # noqa: E402

from app.stock.item_default_domain.api.item_default import router as item_default_router  # noqa: E402

from app.stock.item_group_domain.api.item_group import router as item_group_router  # noqa: E402

from app.stock.item_lead_time_domain.api.item_lead_time import router as item_lead_time_router  # noqa: E402

from app.stock.item_manufacturer_domain.api.item_manufacturer import router as item_manufacturer_router  # noqa: E402

from app.stock.item_price_domain.api.item_price import router as item_price_router  # noqa: E402

from app.stock.item_quality_inspection_parameter_domain.api.item_quality_inspection_parameter import router as item_quality_inspection_parameter_router  # noqa: E402

from app.stock.item_reorder_domain.api.item_reorder import router as item_reorder_router  # noqa: E402

from app.stock.item_standard_cost_domain.api.item_standard_cost import router as item_standard_cost_router  # noqa: E402

from app.stock.item_supplier_domain.api.item_supplier import router as item_supplier_router  # noqa: E402

from app.stock.item_tax_domain.api.item_tax import router as item_tax_router  # noqa: E402

from app.stock.item_variant_domain.api.item_variant import router as item_variant_router  # noqa: E402

from app.stock.item_variant_attribute_domain.api.item_variant_attribute import router as item_variant_attribute_router  # noqa: E402

from app.stock.item_variant_settings_domain.api.item_variant_settings import router as item_variant_settings_router  # noqa: E402

from app.stock.item_website_specification_domain.api.item_website_specification import router as item_website_specification_router  # noqa: E402

from app.stock.landed_cost_item_domain.api.landed_cost_item import router as landed_cost_item_router  # noqa: E402

from app.stock.landed_cost_purchase_receipt_domain.api.landed_cost_purchase_receipt import router as landed_cost_purchase_receipt_router  # noqa: E402

from app.stock.landed_cost_taxes_and_charges_domain.api.landed_cost_taxes_and_charges import router as landed_cost_taxes_and_charges_router  # noqa: E402

from app.stock.landed_cost_vendor_invoice_domain.api.landed_cost_vendor_invoice import router as landed_cost_vendor_invoice_router  # noqa: E402

from app.stock.landed_cost_voucher_domain.api.landed_cost_voucher import router as landed_cost_voucher_router  # noqa: E402

from app.stock.manufacturer_domain.api.manufacturer import router as manufacturer_router  # noqa: E402

from app.stock.material_request_domain.api.material_request import router as material_request_router  # noqa: E402

from app.stock.material_request_item_domain.api.material_request_item import router as material_request_item_router  # noqa: E402

from app.stock.packed_item_domain.api.packed_item import router as packed_item_router  # noqa: E402

from app.stock.packing_slip_domain.api.packing_slip import router as packing_slip_router  # noqa: E402

from app.stock.packing_slip_item_domain.api.packing_slip_item import router as packing_slip_item_router  # noqa: E402

from app.stock.pick_list_domain.api.pick_list import router as pick_list_router  # noqa: E402

from app.stock.pick_list_item_domain.api.pick_list_item import router as pick_list_item_router  # noqa: E402

from app.stock.price_list_domain.api.price_list import router as price_list_router  # noqa: E402

from app.stock.price_list_country_domain.api.price_list_country import router as price_list_country_router  # noqa: E402

from app.stock.purchase_receipt_domain.api.purchase_receipt import router as purchase_receipt_router  # noqa: E402

from app.stock.purchase_receipt_item_domain.api.purchase_receipt_item import router as purchase_receipt_item_router  # noqa: E402

from app.stock.putaway_rule_domain.api.putaway_rule import router as putaway_rule_router  # noqa: E402

from app.stock.quality_inspection_domain.api.quality_inspection import router as quality_inspection_router  # noqa: E402

from app.stock.quality_inspection_parameter_domain.api.quality_inspection_parameter import router as quality_inspection_parameter_router  # noqa: E402

from app.stock.quality_inspection_parameter_group_domain.api.quality_inspection_parameter_group import router as quality_inspection_parameter_group_router  # noqa: E402

from app.stock.quality_inspection_reading_domain.api.quality_inspection_reading import router as quality_inspection_reading_router  # noqa: E402

from app.stock.quality_inspection_template_domain.api.quality_inspection_template import router as quality_inspection_template_router  # noqa: E402

from app.stock.quick_stock_balance_domain.api.quick_stock_balance import router as quick_stock_balance_router  # noqa: E402

from app.stock.repost_item_valuation_domain.api.repost_item_valuation import router as repost_item_valuation_router  # noqa: E402

from app.stock.serial_and_batch_bundle_domain.api.serial_and_batch_bundle import router as serial_and_batch_bundle_router  # noqa: E402

from app.stock.serial_and_batch_entry_domain.api.serial_and_batch_entry import router as serial_and_batch_entry_router  # noqa: E402

from app.stock.serial_no_domain.api.serial_no import router as serial_no_router  # noqa: E402

from app.stock.shipment_domain.api.shipment import router as shipment_router  # noqa: E402

from app.stock.shipment_delivery_note_domain.api.shipment_delivery_note import router as shipment_delivery_note_router  # noqa: E402

from app.stock.shipment_parcel_domain.api.shipment_parcel import router as shipment_parcel_router  # noqa: E402

from app.stock.shipment_parcel_template_domain.api.shipment_parcel_template import router as shipment_parcel_template_router  # noqa: E402

from app.stock.stock_closing_balance_domain.api.stock_closing_balance import router as stock_closing_balance_router  # noqa: E402

from app.stock.stock_closing_entry_domain.api.stock_closing_entry import router as stock_closing_entry_router  # noqa: E402

from app.stock.stock_entry_domain.api.stock_entry import router as stock_entry_router  # noqa: E402

from app.stock.stock_entry_detail_domain.api.stock_entry_detail import router as stock_entry_detail_router  # noqa: E402

from app.stock.stock_entry_type_domain.api.stock_entry_type import router as stock_entry_type_router  # noqa: E402

from app.stock.stock_ledger_entry_domain.api.stock_ledger_entry import router as stock_ledger_entry_router  # noqa: E402

from app.stock.stock_reconciliation_domain.api.stock_reconciliation import router as stock_reconciliation_router  # noqa: E402

from app.stock.stock_reconciliation_item_domain.api.stock_reconciliation_item import router as stock_reconciliation_item_router  # noqa: E402

from app.stock.stock_reposting_settings_domain.api.stock_reposting_settings import router as stock_reposting_settings_router  # noqa: E402

from app.stock.stock_reservation_entry_domain.api.stock_reservation_entry import router as stock_reservation_entry_router  # noqa: E402

from app.stock.stock_settings_domain.api.stock_settings import router as stock_settings_router  # noqa: E402

from app.stock.uom_domain.api.uom import router as uom_router  # noqa: E402

from app.stock.uom_category_domain.api.uom_category import router as uom_category_router  # noqa: E402

from app.stock.uom_conversion_detail_domain.api.uom_conversion_detail import router as uom_conversion_detail_router  # noqa: E402

from app.stock.variant_field_domain.api.variant_field import router as variant_field_router  # noqa: E402

from app.stock.warehouse_domain.api.warehouse import router as warehouse_router  # noqa: E402

from app.stock.warehouse_type_domain.api.warehouse_type import router as warehouse_type_router  # noqa: E402



#: A fixed tenant so tests can assert on isolation against a second value.

BUSINESS_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")

OTHER_BUSINESS_ID = uuid.UUID("22222222-2222-4222-8222-222222222222")





#: Schema file built once per session; every test gets a fresh copy of it.

_SCHEMA_DIR = tempfile.mkdtemp(prefix="creditbridge-stock-tests-")

_SCHEMA_FILE = os.path.join(_SCHEMA_DIR, "schema.db")





def _build_schema(path: str) -> None:

    """Create every converted table once, in FK order, into ``path``.



    ``businesses`` is a minimal id-only table because TenantModel's

    ``business_id`` is a FK to it; it MUST be declared against the same

    MetaData that owns the stock tables, or the FK cannot be resolved at DDL

    compile time.



    Only ``app.accounts.*`` and ``app.stock.*`` tables are created: the rest of

    Base.metadata holds pre-existing CreditBridge models that use Postgres-only

    types (JSONB), which SQLite cannot render.



    ``use_alter`` FKs are emitted as separate ALTER statements, so they are NOT

    part of CREATE TABLE and must not constrain the creation order -- ERPNext

    has genuine mutual links (delivery_note <-> purchase_receipt) that would

    otherwise make the graph unorderable.

    """

    eng = create_engine(f"sqlite:///{path}")

    if "businesses" not in Base.metadata.tables:

        Table("businesses", Base.metadata, Column("id", Uuid, primary_key=True))

    Base.metadata.tables["businesses"].create(eng, checkfirst=True)



    converted_tables = {

        m.class_.__tablename__

        for m in Base.registry.mappers

        if m.class_.__module__.startswith(("app.accounts.", "app.stock."))

    }

    pending = {

        t: ({fk.column.table.name

             for fk in Base.metadata.tables[t].foreign_keys

             if not fk.constraint.use_alter}

            & converted_tables) - {t}

        for t in converted_tables

    }

    ordered: list[str] = []

    while pending:

        ready = sorted(t for t, d in pending.items() if not (d - set(ordered)))

        if not ready:  # pragma: no cover - would mean a genuine FK cycle

            raise RuntimeError(f"unorderable converted tables: {sorted(pending)}")

        ordered.extend(ready)

        for t in ready:

            del pending[t]



    for name in ordered:

        Base.metadata.tables[name].create(eng)

    eng.dispose()





@pytest.fixture(scope="session")

def _schema_file():

    """Build the schema once; every test then copies it (milliseconds)."""

    if not os.path.exists(_SCHEMA_FILE):

        _build_schema(_SCHEMA_FILE)

    return _SCHEMA_FILE





@pytest.fixture()

def engine(_schema_file, tmp_path):

    """A fresh database per test, copied from the session-wide schema file.



    Building ~380 tables per test cost ~1s each; copying an empty file costs a

    fraction of a millisecond, so the file-per-test pattern keeps isolation

    (every test starts from an empty database, so committed rows never leak

    between tests) without the per-test DDL.

    """

    path = os.path.join(str(tmp_path), "test.db")

    shutil.copyfile(_schema_file, path)

    # One shared connection for the whole test: the ``db`` fixture and the app

    # dependency therefore talk to the same SQLite connection, which removes

    # the reader/writer deadlock ("database is locked") that a second

    # connection would introduce. Same reasoning as the in-memory suites.

    eng = create_engine(

        f"sqlite:///{path}",

        connect_args={"check_same_thread": False},

        poolclass=StaticPool,

    )

    yield eng

    eng.dispose()





@pytest.fixture()

def db(engine):

    """A Session bound to the in-memory database."""

    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    session = TestingSession()

    try:

        yield session

    finally:

        session.close()





@pytest.fixture()

def business_id() -> uuid.UUID:

    return BUSINESS_ID





@pytest.fixture()

def other_business_id() -> uuid.UUID:

    return OTHER_BUSINESS_ID





@pytest.fixture()

def app(engine):

    """A FastAPI app with the stock routers and overridden tenancy."""

    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)



    application = FastAPI()

    application.include_router(batch_router, prefix="/batch")

    application.include_router(bin_router, prefix="/bin")

    application.include_router(brand_router, prefix="/brand")

    application.include_router(company_restriction_router, prefix="/company-restriction")

    application.include_router(customs_tariff_number_router, prefix="/customs-tariff-number")

    application.include_router(delivery_note_router, prefix="/delivery-note")

    application.include_router(delivery_note_item_router, prefix="/delivery-note-item")

    application.include_router(delivery_settings_router, prefix="/delivery-settings")

    application.include_router(delivery_stop_router, prefix="/delivery-stop")

    application.include_router(delivery_trip_router, prefix="/delivery-trip")

    application.include_router(inventory_dimension_router, prefix="/inventory-dimension")

    application.include_router(item_router, prefix="/item")

    application.include_router(item_alternative_router, prefix="/item-alternative")

    application.include_router(item_attribute_router, prefix="/item-attribute")

    application.include_router(item_attribute_value_router, prefix="/item-attribute-value")

    application.include_router(item_barcode_router, prefix="/item-barcode")

    application.include_router(item_customer_detail_router, prefix="/item-customer-detail")

    application.include_router(item_default_router, prefix="/item-default")

    application.include_router(item_group_router, prefix="/item-group")

    application.include_router(item_lead_time_router, prefix="/item-lead-time")

    application.include_router(item_manufacturer_router, prefix="/item-manufacturer")

    application.include_router(item_price_router, prefix="/item-price")

    application.include_router(item_quality_inspection_parameter_router, prefix="/item-quality-inspection-parameter")

    application.include_router(item_reorder_router, prefix="/item-reorder")

    application.include_router(item_standard_cost_router, prefix="/item-standard-cost")

    application.include_router(item_supplier_router, prefix="/item-supplier")

    application.include_router(item_tax_router, prefix="/item-tax")

    application.include_router(item_variant_router, prefix="/item-variant")

    application.include_router(item_variant_attribute_router, prefix="/item-variant-attribute")

    application.include_router(item_variant_settings_router, prefix="/item-variant-settings")

    application.include_router(item_website_specification_router, prefix="/item-website-specification")

    application.include_router(landed_cost_item_router, prefix="/landed-cost-item")

    application.include_router(landed_cost_purchase_receipt_router, prefix="/landed-cost-purchase-receipt")

    application.include_router(landed_cost_taxes_and_charges_router, prefix="/landed-cost-taxes-and-charges")

    application.include_router(landed_cost_vendor_invoice_router, prefix="/landed-cost-vendor-invoice")

    application.include_router(landed_cost_voucher_router, prefix="/landed-cost-voucher")

    application.include_router(manufacturer_router, prefix="/manufacturer")

    application.include_router(material_request_router, prefix="/material-request")

    application.include_router(material_request_item_router, prefix="/material-request-item")

    application.include_router(packed_item_router, prefix="/packed-item")

    application.include_router(packing_slip_router, prefix="/packing-slip")

    application.include_router(packing_slip_item_router, prefix="/packing-slip-item")

    application.include_router(pick_list_router, prefix="/pick-list")

    application.include_router(pick_list_item_router, prefix="/pick-list-item")

    application.include_router(price_list_router, prefix="/price-list")

    application.include_router(price_list_country_router, prefix="/price-list-country")

    application.include_router(purchase_receipt_router, prefix="/purchase-receipt")

    application.include_router(purchase_receipt_item_router, prefix="/purchase-receipt-item")

    application.include_router(putaway_rule_router, prefix="/putaway-rule")

    application.include_router(quality_inspection_router, prefix="/quality-inspection")

    application.include_router(quality_inspection_parameter_router, prefix="/quality-inspection-parameter")

    application.include_router(quality_inspection_parameter_group_router, prefix="/quality-inspection-parameter-group")

    application.include_router(quality_inspection_reading_router, prefix="/quality-inspection-reading")

    application.include_router(quality_inspection_template_router, prefix="/quality-inspection-template")

    application.include_router(quick_stock_balance_router, prefix="/quick-stock-balance")

    application.include_router(repost_item_valuation_router, prefix="/repost-item-valuation")

    application.include_router(serial_and_batch_bundle_router, prefix="/serial-and-batch-bundle")

    application.include_router(serial_and_batch_entry_router, prefix="/serial-and-batch-entry")

    application.include_router(serial_no_router, prefix="/serial-no")

    application.include_router(shipment_router, prefix="/shipment")

    application.include_router(shipment_delivery_note_router, prefix="/shipment-delivery-note")

    application.include_router(shipment_parcel_router, prefix="/shipment-parcel")

    application.include_router(shipment_parcel_template_router, prefix="/shipment-parcel-template")

    application.include_router(stock_closing_balance_router, prefix="/stock-closing-balance")

    application.include_router(stock_closing_entry_router, prefix="/stock-closing-entry")

    application.include_router(stock_entry_router, prefix="/stock-entry")

    application.include_router(stock_entry_detail_router, prefix="/stock-entry-detail")

    application.include_router(stock_entry_type_router, prefix="/stock-entry-type")

    application.include_router(stock_ledger_entry_router, prefix="/stock-ledger-entry")

    application.include_router(stock_reconciliation_router, prefix="/stock-reconciliation")

    application.include_router(stock_reconciliation_item_router, prefix="/stock-reconciliation-item")

    application.include_router(stock_reposting_settings_router, prefix="/stock-reposting-settings")

    application.include_router(stock_reservation_entry_router, prefix="/stock-reservation-entry")

    application.include_router(stock_settings_router, prefix="/stock-settings")

    application.include_router(uom_router, prefix="/uom")

    application.include_router(uom_category_router, prefix="/uom-category")

    application.include_router(uom_conversion_detail_router, prefix="/uom-conversion-detail")

    application.include_router(variant_field_router, prefix="/variant-field")

    application.include_router(warehouse_router, prefix="/warehouse")

    application.include_router(warehouse_type_router, prefix="/warehouse-type")



    def override_get_db():

        session = TestingSession()

        try:

            yield session

        finally:

            session.close()



    application.dependency_overrides[get_db] = override_get_db

    application.dependency_overrides[get_current_business_uuid] = lambda: BUSINESS_ID

    return application





@pytest.fixture()

def client(app) -> TestClient:

    return TestClient(app)
