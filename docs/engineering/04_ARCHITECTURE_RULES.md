# CreditBridge Architecture Rules

Architecture Flow

Business Screen

↓

Business Component

↓

Shared Pattern

↓

Composite

↓

Primitive

↓

Token

Dependency always goes downward.

Never upward.

---

Business Logic

Only

features/

---

Shared UI

Only

shared/design-system

---

API

Only

api/

or

features/**/api

---

State

Only

store/

or

feature store

---

Utilities

Only

shared/utils

---

Never

Business imports Business.

Shared imports Business.

Token imports Component.

Component imports Feature.
