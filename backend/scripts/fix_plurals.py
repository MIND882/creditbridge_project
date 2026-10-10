import re, pathlib

MAP = {"entrys": "entries", "settingss": "settings", "categorys": "categories",
       "countrys": "countries", "taxs": "taxes", "batchs": "batches",
       "chargess": "charges"}
pat = re.compile(r'(["\'])([a-z_]*?)(' + "|".join(MAP) + r')(\.[a-z_]+)?\1')

for f in pathlib.Path("app").rglob("*.py"):
    if "/migrations/" in str(f):
        continue
    s = f.read_text()
    new = pat.sub(lambda m: f'{m.group(1)}{m.group(2)}{MAP[m.group(3)]}{m.group(4) or ""}{m.group(1)}', s)
    if new != s:
        f.write_text(new)
        print("fixed", f)