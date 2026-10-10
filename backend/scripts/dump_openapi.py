import json
from app.main import app
with open("openapi_schema.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)
print("Schema saved to openapi_schema.json")
