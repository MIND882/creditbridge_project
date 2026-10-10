"""

Fixtures for the selling module tests.



Mirrors the root ``conftest.py`` conventions (in-memory SQLite over a

StaticPool, tenancy pinned to a fixed business id, FK-ordered table

creation) but scoped to the stock routers. The table set is derived from the

FK graph over every converted model of the generated modules, so a new

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



from app.selling.customer_domain.api.customer import router as customer_router  # noqa: E402

from app.selling.customer_credit_limit_domain.api.customer_credit_limit import router as customer_credit_limit_router  # noqa: E402

from app.selling.delivery_schedule_item_domain.api.delivery_schedule_item import router as delivery_schedule_item_router  # noqa: E402

from app.selling.industry_type_domain.api.industry_type import router as industry_type_router  # noqa: E402

from app.selling.installation_note_domain.api.installation_note import router as installation_note_router  # noqa: E402

from app.selling.installation_note_item_domain.api.installation_note_item import router as installation_note_item_router  # noqa: E402

from app.selling.party_specific_item_domain.api.party_specific_item import router as party_specific_item_router  # noqa: E402

from app.selling.product_bundle_domain.api.product_bundle import router as product_bundle_router  # noqa: E402

from app.selling.product_bundle_item_domain.api.product_bundle_item import router as product_bundle_item_router  # noqa: E402

from app.selling.proforma_invoice_domain.api.proforma_invoice import router as proforma_invoice_router  # noqa: E402

from app.selling.proforma_invoice_item_domain.api.proforma_invoice_item import router as proforma_invoice_item_router  # noqa: E402

from app.selling.quotation_domain.api.quotation import router as quotation_router  # noqa: E402

from app.selling.quotation_item_domain.api.quotation_item import router as quotation_item_router  # noqa: E402

from app.selling.sales_order_domain.api.sales_order import router as sales_order_router  # noqa: E402

from app.selling.sales_order_item_domain.api.sales_order_item import router as sales_order_item_router  # noqa: E402

from app.selling.sales_partner_type_domain.api.sales_partner_type import router as sales_partner_type_router  # noqa: E402

from app.selling.sales_team_domain.api.sales_team import router as sales_team_router  # noqa: E402

from app.selling.selling_settings_domain.api.selling_settings import router as selling_settings_router  # noqa: E402

from app.selling.sms_center_domain.api.sms_center import router as sms_center_router  # noqa: E402

from app.selling.supplier_number_at_customer_domain.api.supplier_number_at_customer import router as supplier_number_at_customer_router  # noqa: E402



#: A fixed tenant so tests can assert on isolation against a second value.

BUSINESS_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")

OTHER_BUSINESS_ID = uuid.UUID("22222222-2222-4222-8222-222222222222")





#: Schema file built once per session; every test gets a fresh copy of it.

_SCHEMA_DIR = tempfile.mkdtemp(prefix="creditbridge-selling-tests-")

_SCHEMA_FILE = os.path.join(_SCHEMA_DIR, "schema.db")





def _build_schema(path: str) -> None:

    """Create every converted table once, in FK order, into ``path``.



    ``businesses`` is a minimal id-only table because TenantModel's

    ``business_id`` is a FK to it; it MUST be declared against the same

    MetaData that owns the stock tables, or the FK cannot be resolved at DDL

    compile time.



    Only the converted tables of the generated modules are created: the rest of

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

        if m.class_.__module__.startswith(('app.accounts.', 'app.stock.', 'app.buying.', 'app.selling.'))

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

    """A FastAPI app with the selling routers and overridden tenancy."""

    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)



    application = FastAPI()

    application.include_router(customer_router, prefix="/customer")

    application.include_router(customer_credit_limit_router, prefix="/customer-credit-limit")

    application.include_router(delivery_schedule_item_router, prefix="/delivery-schedule-item")

    application.include_router(industry_type_router, prefix="/industry-type")

    application.include_router(installation_note_router, prefix="/installation-note")

    application.include_router(installation_note_item_router, prefix="/installation-note-item")

    application.include_router(party_specific_item_router, prefix="/party-specific-item")

    application.include_router(product_bundle_router, prefix="/product-bundle")

    application.include_router(product_bundle_item_router, prefix="/product-bundle-item")

    application.include_router(proforma_invoice_router, prefix="/proforma-invoice")

    application.include_router(proforma_invoice_item_router, prefix="/proforma-invoice-item")

    application.include_router(quotation_router, prefix="/quotation")

    application.include_router(quotation_item_router, prefix="/quotation-item")

    application.include_router(sales_order_router, prefix="/sales-order")

    application.include_router(sales_order_item_router, prefix="/sales-order-item")

    application.include_router(sales_partner_type_router, prefix="/sales-partner-type")

    application.include_router(sales_team_router, prefix="/sales-team")

    application.include_router(selling_settings_router, prefix="/selling-settings")

    application.include_router(sms_center_router, prefix="/sms-center")

    application.include_router(supplier_number_at_customer_router, prefix="/supplier-number-at-customer")



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
