import re, pathlib

root = pathlib.Path("app")
pattern = re.compile(r"(SAEnum\([^)]*?native_enum=False[^)]*?)(\))", re.S)

for f in root.rglob("models/*.py"):
    s = f.read_text()
    if "native_enum=False" not in s:
        continue
    new = pattern.sub(
        lambda m: m.group(1) + ", values_callable=lambda e: [m.value for m in e]" + m.group(2)
        if "values_callable" not in m.group(1) else m.group(0),
        s,
    )
    if new != s:
        f.write_text(new)
        print("fixed", f)