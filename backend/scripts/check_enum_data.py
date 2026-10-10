import pkgutil, importlib, app
from sqlalchemy import Enum as SAEnum, text, inspect
from app.core.base_model import Base
from app.db.session import engine

for m in pkgutil.walk_packages(app.__path__, "app."):
    if ".models." in m.name:
        try:
            importlib.import_module(m.name)
        except Exception as e:
            print("IMPORT FAIL", m.name, e)

MODULES = ("app.accounts", "app.buying", "app.selling", "app.customers", "app.crm")
insp = inspect(engine)
have = set(insp.get_table_names())
fixes, unknown, skipped = [], [], []
with engine.connect() as c:
    for mapper in Base.registry.mappers:
        if not mapper.class_.__module__.startswith(MODULES):
            continue
        t = mapper.local_table
        if t.name not in have:
            continue
        dbcols = {x["name"] for x in insp.get_columns(t.name)}
        for col in t.columns:
            ty = col.type
            if not (isinstance(ty, SAEnum) and ty.enum_class and not ty.native_enum):
                continue
            if col.name not in dbcols:
                skipped.append(f"{t.name}.{col.name}")
                continue
            values = {m.value for m in ty.enum_class}
            names = {m.name: m.value for m in ty.enum_class}
            rows = c.execute(text(
                f'SELECT DISTINCT "{col.name}" FROM "{t.name}" WHERE "{col.name}" IS NOT NULL'
            )).scalars().all()
            for r in rows:
                if r in values:
                    continue
                if r in names:
                    fixes.append(f"UPDATE \"{t.name}\" SET \"{col.name}\" = '{names[r]}' WHERE \"{col.name}\" = '{r}';")
                else:
                    unknown.append(f"{t.name}.{col.name}: {r!r}")
print("-- FIXES");   print("\n".join(sorted(set(fixes))))
print("-- UNKNOWN"); print("\n".join(unknown))
print("-- SKIPPED"); print("\n".join(skipped))
