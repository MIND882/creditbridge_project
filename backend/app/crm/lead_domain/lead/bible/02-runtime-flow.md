# 02 - RUNTIME FLOW
# PURPOSE

THIS DOCUMENT EXPLAINS EXACTLY HOW A LEAD REQUEST TRAVELS THROUGH THE CREDITBRIDGE BACKEND

IT IS NOT A DESIGN DOCUMENT.

IT IS THE EXECUTION LIFECYCLE OF A REQUEST.

EVERY REQUEST (CREATE , UPDATE, DELETE, LIST GET QUALIFY, ASSIGN, ETC.) FLLLOW THIS SAME ARCHITECTURE

-----

# COMPLETE RUNTIME FLOW

```text
User
    │
    ▼
Frontend (Lead Form)
    │
    ▼
API Client
    │
    ▼
HTTP Request
    │
    ▼
FastAPI Router
    │
    ▼
Dependency Injection
    │
    ├── Database Session
    ├── Business UUID
    ├── Actor UUID
    └── LeadService
    │
    ▼
Request Schema Validation
    │
    ▼
LeadService
    │
    ▼
LeadRepository
    │
    ▼
Lead SQLAlchemy Model
    │
    ▼
PostgreSQL Database
    │
    ▼
Lead SQLAlchemy Model
    │
    ▼
LeadRepository
    │
    ▼
LeadService
    │
    ▼
Response Schema
    │
    ▼
FastAPI Router
    │
    ▼
HTTP Response
    │
    ▼
Frontend
    │
    ▼
UI Update
```
---

# Step 1 — User

The runtime starts when an authenticated MSME user performs an action.

Examples

- Create Lead
- Open Lead
- Update Lead
- Delete Lead
- View Pipeline

The user never communicates directly with the backend database.

---

# Step 2 — Frontend

The Lead UI collects information.

Example

• Name

• Company

• Phone

• Email

• PAN

• GSTIN

• Source

The frontend only collects data.

No business rules are executed here.

---

# Step 3 — API Client

The frontend calls the API Client.

Example

POST /crm/leads

Responsibilities

• Build HTTP request

• Attach JWT token

• Send JSON

It does not know how Leads are created.

---

# Step 4 — FastAPI Router

The Router is the HTTP entry point.

Responsibilities

• Receive request

• Match endpoint

• Resolve dependencies

• Call LeadService

• Convert Service exceptions into HTTP responses

Router never contains

❌ SQL

❌ Business Rules

❌ AI

❌ Validation Logic

---

# Step 5 — Dependency Injection

Before execution starts FastAPI creates required objects.

Current dependencies

Database Session

Provides SQLAlchemy Session.

Business UUID

Resolved from authenticated JWT.

Actor UUID

Currently returns None.

Reserved for future staff authentication.

LeadService

Shared service instance.

---

# Step 6 — Request Schema

Incoming JSON is converted into a Pydantic Schema.

Examples

LeadCreate

LeadUpdate

LeadQualifyRequest

LeadMarkDuplicateRequest

Responsibilities

• Required fields

• Data types

• Enum validation

• Format validation

If validation fails

The request stops immediately.

LeadService is never executed.

---

# Step 7 — LeadService

LeadService is the Business Brain.

This is where business workflow begins.

Responsibilities

• Execute business rules

• Coordinate repositories

• Manage transactions

• Generate Lead Name

• Check duplicate Lead (future)

• Record activities

• Trigger AI pipeline

• Commit or Rollback

LeadService never writes SQL.

It communicates only through repositories.

---

# Step 8 — LeadRepository

Repository is responsible only for database access.

Responsibilities

• INSERT

• UPDATE

• SELECT

• Soft Delete

• Restore

• Assign Owner

• Change Status

• Pagination

Repository contains

NO

❌ Business Rules

❌ AI

❌ Validation

❌ HTTP

❌ Commit()

Repository only performs

• add()

• flush()

• refresh()

• select()

Service decides whether to Commit or Rollback.

---

# Step 9 — SQLAlchemy Model

Repository converts business objects into SQLAlchemy models.

Example

Lead()

The model represents

• Table

• Columns

• Relationships

• Indexes

• Constraints

The model never contains business workflow.

---

# Step 10 — PostgreSQL

Database permanently stores the Lead.

Database only persists data.

It does not know

• Why Lead exists

• Why Status changed

• Why Activity was created

It only stores rows.

---

# Step 11 — Repository Response

Repository converts database results into Python objects.

Returns

Lead Model

or

List[Lead]

Repository never returns HTTP responses.

---

# Step 12 — LeadService Response

LeadService receives the database objects.

If required it

• Creates activities

• Updates counters

• Triggers AI

• Commits transaction

Finally returns the Lead object.

---

# Step 13 — Response Schema

Before leaving the backend

Lead

↓

LeadResponse

Only fields defined in the Response Schema are exposed.

Internal database fields remain hidden.

---

# Step 14 — FastAPI Router

Router serializes LeadResponse into JSON.

Adds

HTTP Status

Headers

Content-Type

Returns response.

---

# Step 15 — Frontend

The frontend receives JSON.

Updates

• Lead Table

• Lead Detail

• Timeline

• Statistics

The user finally sees the updated UI.

---

# Transaction Boundary

Only the Service Layer controls transactions.

```text
LeadService

↓

Repository A

↓

Repository B

↓

Repository C

↓

Commit
```

If any repository fails

Everything rolls back.

Repository never commits.

---

# Layer Responsibility

| Layer | Responsibility |
|--------|----------------|
| Frontend | Collect user input |
| API Client | Send HTTP request |
| Router | HTTP communication |
| Dependency Injection | Create required objects |
| Request Schema | Validate request |
| LeadService | Execute business workflow |
| Repository | Database communication |
| Model | Database mapping |
| PostgreSQL | Data persistence |
| Response Schema | Safe API response |
| Frontend | Render UI |

---

# Runtime Principle

Every layer owns one responsibility only.

Frontend

↓

Collect Data

Router

↓

HTTP

Schema

↓

Validation

Service

↓

Business

Repository

↓

Persistence

Model

↓

Mapping

Database

↓

Storage

Response Schema

↓

Serialization

Frontend

↓

Rendering

No layer performs another layer's responsibility.