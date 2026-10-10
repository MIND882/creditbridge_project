import csv, json, sys, collections
from app.main import app

meta = json.load(open(sys.argv[1]))
spec = app.openapi()
S = spec["components"]["schemas"]

def deref(p):
    while isinstance(p, dict) and "$ref" in p:
        p = S[p["$ref"].split("/")[-1]]
    return p

def unwrap(p):
    p = deref(p)
    for key in ("anyOf", "oneOf", "allOf"):
        if key in p:
            opts = [deref(b) for b in p[key] if deref(b).get("type") != "null"]
            if opts:
                return unwrap(opts[0])
    return p

def kind(p):
    p = unwrap(p)
    if "enum" in p: return "enum"
    t, f = p.get("type"), p.get("format")
    if f == "uuid": return "uuid"
    if f in ("date", "date-time", "time"): return "date"
    if t == "boolean": return "bool"
    if t in ("integer", "number"): return "num"
    if t == "string": return "str"
    return str(t)

WANT = {"check": {"bool"}, "currency": {"num"}, "number": {"num"},
        "date": {"date"}, "time": {"date", "str"}, "select": {"enum"},
        "text": {"str"}, "textarea": {"str"}, "link": {"uuid", "str"}}

def create_schema(prefix):
    for p in (prefix, prefix + "/"):
        op = spec["paths"].get(p, {}).get("post")
        if op:
            s = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
            if s:
                return unwrap(s)
    return None

rows, no_post = [], []
for d in meta:
    sch = create_schema(d["backend"]["api_prefix"])
    if sch is None:
        no_post.append(d["name"]); continue
    props, req = sch.get("properties", {}), set(sch.get("required", []))
    mf = {f["name"]: f for f in d["fields"]}
    for n, f in mf.items():
        if n == "name":
            continue
        if n not in props:
            rows.append((d["name"], n, "NOT_IN_API", f["type"])); continue
        got = kind(props[n])
        if got not in WANT.get(f["type"], {"str"}):
            rows.append((d["name"], n, "TYPE", f"meta={f['type']} api={got}"))
        if f["type"] == "select" and got == "enum":
            vals = {str(v) for v in unwrap(props[n])["enum"]}
            opts = set(f.get("options", []))
            if vals - opts: rows.append((d["name"], n, "ENUM_MISSING_IN_META", sorted(vals - opts)))
            if opts - vals: rows.append((d["name"], n, "ENUM_NOT_IN_API", sorted(opts - vals)))
        if n in req and not f.get("required"):
            rows.append((d["name"], n, "API_REQUIRED_META_OPTIONAL", ""))
        if f.get("required") and n not in req:
            rows.append((d["name"], n, "META_REQUIRED_API_OPTIONAL", ""))
    for n in props:
        if n not in mf and n in req:
            rows.append((d["name"], n, "API_REQUIRED_NOT_IN_META", ""))

print(collections.Counter(d["type"] for d in meta))
print("no POST (read-only/child):", len(no_post))
for code, n in collections.Counter(r[2] for r in rows).most_common():
    print(f"{code:30} {n}")
with open("metadata_vs_api.csv", "w", newline="") as fh:
    csv.writer(fh).writerows([("domain", "field", "issue", "detail"), *rows])