"""

Fixtures for the manufacturing module tests.



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



from app.manufacturing.blanket_order_domain.api.blanket_order import router as blanket_order_router  # noqa: E402

from app.manufacturing.blanket_order_item_domain.api.blanket_order_item import router as blanket_order_item_router  # noqa: E402

from app.manufacturing.bom_domain.api.bom import router as bom_router  # noqa: E402

from app.manufacturing.bom_creator_domain.api.bom_creator import router as bom_creator_router  # noqa: E402

from app.manufacturing.bom_creator_item_domain.api.bom_creator_item import router as bom_creator_item_router  # noqa: E402

from app.manufacturing.bom_explosion_item_domain.api.bom_explosion_item import router as bom_explosion_item_router  # noqa: E402

from app.manufacturing.bom_item_domain.api.bom_item import router as bom_item_router  # noqa: E402

from app.manufacturing.bom_operation_domain.api.bom_operation import router as bom_operation_router  # noqa: E402

from app.manufacturing.bom_secondary_item_domain.api.bom_secondary_item import router as bom_secondary_item_router  # noqa: E402

from app.manufacturing.bom_update_batch_domain.api.bom_update_batch import router as bom_update_batch_router  # noqa: E402

from app.manufacturing.bom_update_log_domain.api.bom_update_log import router as bom_update_log_router  # noqa: E402

from app.manufacturing.bom_update_tool_domain.api.bom_update_tool import router as bom_update_tool_router  # noqa: E402

from app.manufacturing.bom_website_item_domain.api.bom_website_item import router as bom_website_item_router  # noqa: E402

from app.manufacturing.bom_website_operation_domain.api.bom_website_operation import router as bom_website_operation_router  # noqa: E402

from app.manufacturing.downtime_entry_domain.api.downtime_entry import router as downtime_entry_router  # noqa: E402

from app.manufacturing.job_card_domain.api.job_card import router as job_card_router  # noqa: E402

from app.manufacturing.job_card_item_domain.api.job_card_item import router as job_card_item_router  # noqa: E402

from app.manufacturing.job_card_operation_domain.api.job_card_operation import router as job_card_operation_router  # noqa: E402

from app.manufacturing.job_card_scheduled_time_domain.api.job_card_scheduled_time import router as job_card_scheduled_time_router  # noqa: E402

from app.manufacturing.job_card_secondary_item_domain.api.job_card_secondary_item import router as job_card_secondary_item_router  # noqa: E402

from app.manufacturing.job_card_time_log_domain.api.job_card_time_log import router as job_card_time_log_router  # noqa: E402

from app.manufacturing.manufacturing_settings_domain.api.manufacturing_settings import router as manufacturing_settings_router  # noqa: E402

from app.manufacturing.master_production_schedule_domain.api.master_production_schedule import router as master_production_schedule_router  # noqa: E402

from app.manufacturing.master_production_schedule_item_domain.api.master_production_schedule_item import router as master_production_schedule_item_router  # noqa: E402

from app.manufacturing.material_request_plan_item_domain.api.material_request_plan_item import router as material_request_plan_item_router  # noqa: E402

from app.manufacturing.operation_domain.api.operation import router as operation_router  # noqa: E402

from app.manufacturing.plant_floor_domain.api.plant_floor import router as plant_floor_router  # noqa: E402

from app.manufacturing.production_plan_domain.api.production_plan import router as production_plan_router  # noqa: E402

from app.manufacturing.production_plan_item_domain.api.production_plan_item import router as production_plan_item_router  # noqa: E402

from app.manufacturing.production_plan_item_reference_domain.api.production_plan_item_reference import router as production_plan_item_reference_router  # noqa: E402

from app.manufacturing.production_plan_material_request_domain.api.production_plan_material_request import router as production_plan_material_request_router  # noqa: E402

from app.manufacturing.production_plan_material_request_warehouse_domain.api.production_plan_material_request_warehouse import router as production_plan_material_request_warehouse_router  # noqa: E402

from app.manufacturing.production_plan_sales_order_domain.api.production_plan_sales_order import router as production_plan_sales_order_router  # noqa: E402

from app.manufacturing.production_plan_sub_assembly_item_domain.api.production_plan_sub_assembly_item import router as production_plan_sub_assembly_item_router  # noqa: E402

from app.manufacturing.routing_domain.api.routing import router as routing_router  # noqa: E402

from app.manufacturing.sales_forecast_domain.api.sales_forecast import router as sales_forecast_router  # noqa: E402

from app.manufacturing.sales_forecast_item_domain.api.sales_forecast_item import router as sales_forecast_item_router  # noqa: E402

from app.manufacturing.sub_operation_domain.api.sub_operation import router as sub_operation_router  # noqa: E402

from app.manufacturing.work_order_domain.api.work_order import router as work_order_router  # noqa: E402

from app.manufacturing.work_order_additional_item_domain.api.work_order_additional_item import router as work_order_additional_item_router  # noqa: E402

from app.manufacturing.work_order_item_domain.api.work_order_item import router as work_order_item_router  # noqa: E402

from app.manufacturing.work_order_operation_domain.api.work_order_operation import router as work_order_operation_router  # noqa: E402

from app.manufacturing.workstation_domain.api.workstation import router as workstation_router  # noqa: E402

from app.manufacturing.workstation_cost_domain.api.workstation_cost import router as workstation_cost_router  # noqa: E402

from app.manufacturing.workstation_operating_component_domain.api.workstation_operating_component import router as workstation_operating_component_router  # noqa: E402

from app.manufacturing.workstation_operating_component_account_domain.api.workstation_operating_component_account import router as workstation_operating_component_account_router  # noqa: E402

from app.manufacturing.workstation_type_domain.api.workstation_type import router as workstation_type_router  # noqa: E402

from app.manufacturing.workstation_working_hour_domain.api.workstation_working_hour import router as workstation_working_hour_router  # noqa: E402



#: A fixed tenant so tests can assert on isolation against a second value.

BUSINESS_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")

OTHER_BUSINESS_ID = uuid.UUID("22222222-2222-4222-8222-222222222222")





#: Schema file built once per session; every test gets a fresh copy of it.

_SCHEMA_DIR = tempfile.mkdtemp(prefix="creditbridge-manufacturing-tests-")

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

        if m.class_.__module__.startswith(('app.accounts.', 'app.stock.', 'app.buying.', 'app.selling.', 'app.manufacturing.'))

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

    """A FastAPI app with the manufacturing routers and overridden tenancy."""

    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)



    application = FastAPI()

    application.include_router(blanket_order_router, prefix="/blanket-order")

    application.include_router(blanket_order_item_router, prefix="/blanket-order-item")

    application.include_router(bom_router, prefix="/bom")

    application.include_router(bom_creator_router, prefix="/bom-creator")

    application.include_router(bom_creator_item_router, prefix="/bom-creator-item")

    application.include_router(bom_explosion_item_router, prefix="/bom-explosion-item")

    application.include_router(bom_item_router, prefix="/bom-item")

    application.include_router(bom_operation_router, prefix="/bom-operation")

    application.include_router(bom_secondary_item_router, prefix="/bom-secondary-item")

    application.include_router(bom_update_batch_router, prefix="/bom-update-batch")

    application.include_router(bom_update_log_router, prefix="/bom-update-log")

    application.include_router(bom_update_tool_router, prefix="/bom-update-tool")

    application.include_router(bom_website_item_router, prefix="/bom-website-item")

    application.include_router(bom_website_operation_router, prefix="/bom-website-operation")

    application.include_router(downtime_entry_router, prefix="/downtime-entry")

    application.include_router(job_card_router, prefix="/job-card")

    application.include_router(job_card_item_router, prefix="/job-card-item")

    application.include_router(job_card_operation_router, prefix="/job-card-operation")

    application.include_router(job_card_scheduled_time_router, prefix="/job-card-scheduled-time")

    application.include_router(job_card_secondary_item_router, prefix="/job-card-secondary-item")

    application.include_router(job_card_time_log_router, prefix="/job-card-time-log")

    application.include_router(manufacturing_settings_router, prefix="/manufacturing-settings")

    application.include_router(master_production_schedule_router, prefix="/master-production-schedule")

    application.include_router(master_production_schedule_item_router, prefix="/master-production-schedule-item")

    application.include_router(material_request_plan_item_router, prefix="/material-request-plan-item")

    application.include_router(operation_router, prefix="/operation")

    application.include_router(plant_floor_router, prefix="/plant-floor")

    application.include_router(production_plan_router, prefix="/production-plan")

    application.include_router(production_plan_item_router, prefix="/production-plan-item")

    application.include_router(production_plan_item_reference_router, prefix="/production-plan-item-reference")

    application.include_router(production_plan_material_request_router, prefix="/production-plan-material-request")

    application.include_router(production_plan_material_request_warehouse_router, prefix="/production-plan-material-request-warehouse")

    application.include_router(production_plan_sales_order_router, prefix="/production-plan-sales-order")

    application.include_router(production_plan_sub_assembly_item_router, prefix="/production-plan-sub-assembly-item")

    application.include_router(routing_router, prefix="/routing")

    application.include_router(sales_forecast_router, prefix="/sales-forecast")

    application.include_router(sales_forecast_item_router, prefix="/sales-forecast-item")

    application.include_router(sub_operation_router, prefix="/sub-operation")

    application.include_router(work_order_router, prefix="/work-order")

    application.include_router(work_order_additional_item_router, prefix="/work-order-additional-item")

    application.include_router(work_order_item_router, prefix="/work-order-item")

    application.include_router(work_order_operation_router, prefix="/work-order-operation")

    application.include_router(workstation_router, prefix="/workstation")

    application.include_router(workstation_cost_router, prefix="/workstation-cost")

    application.include_router(workstation_operating_component_router, prefix="/workstation-operating-component")

    application.include_router(workstation_operating_component_account_router, prefix="/workstation-operating-component-account")

    application.include_router(workstation_type_router, prefix="/workstation-type")

    application.include_router(workstation_working_hour_router, prefix="/workstation-working-hour")



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
