# CreditBridge CRM
# Frontend Layer

---

# Purpose

Frontend is the User Interface of CreditBridge.

Its responsibility is to allow a human being to interact with the CreditBridge system.

The Frontend NEVER contains business rules.

It only collects user input, displays data returned by the backend, validates obvious client-side mistakes, and communicates with the Backend API.

Frontend is the first software layer after the User.

---

# Why does Frontend exist?

Without a Frontend, a business owner would have to call backend APIs manually.

Example

POST /v1/leads

with JSON

which is impossible for most users.

Frontend converts human interaction into structured requests that the backend understands.

---

# Responsibilities

The Frontend is responsible for:

• Rendering pages
• Collecting user input
• Client-side validation
• Calling Backend APIs
• Showing loading states
• Showing success messages
• Showing backend errors
• Displaying returned data
• Managing local UI state

The Frontend is NOT responsible for:

✗ Business Logic

✗ Database

✗ Authentication Rules

✗ Authorization Rules

✗ Lead Scoring

✗ AI

✗ SQL

✗ Workflow Decisions

Those belong to the Backend.

---

# Lead Module Frontend Architecture

Lead Module

│

├── LeadList.tsx

├── LeadHeader.tsx

├── LeadToolbar.tsx

├── LeadTable.tsx

├── LeadPagination.tsx

├── CreateLeadDrawer.tsx

├── EditLeadDrawer.tsx

├── LeadForm.tsx

├── useLeads.ts

├── leadApi.ts

├── lead.schema.ts

└── lead.types.ts

Each file has one responsibility.

---

# Runtime Flow

User

↓

Clicks "New Lead"

↓

LeadHeader

↓

CreateLeadDrawer opens

↓

LeadForm renders

↓

User fills the form

↓

Frontend Validation

↓

useCreateLead()

↓

leadApi.createLead()

↓

Axios Client

↓

POST /v1/leads

↓

Backend

↓

Response

↓

Drawer closes

↓

Lead List refetches

↓

UI updates automatically

---

# File Responsibilities

## LeadList.tsx

Purpose

The entry page of the Lead module.

Responsibilities

• Renders the Lead screen

• Maintains page state

• Maintains filters

• Maintains pagination

• Opens drawers

• Calls React Hooks

It NEVER calls Axios directly.

It NEVER contains business logic.

---

## useLeads.ts

Purpose

Acts as the Frontend Service Layer.

Responsibilities

• Fetch Leads

• Fetch One Lead

• Create Lead

• Update Lead

• Delete Lead

• Loading State

• Error State

• Refetch

This file NEVER knows endpoint URLs.

It simply calls leadApi.ts.

---

## leadApi.ts

Purpose

HTTP Client for the Lead module.

Responsibilities

Convert frontend function calls into HTTP requests.

Example

createLead()

↓

POST /v1/leads

getLeads()

↓

GET /v1/leads

updateLead()

↓

PUT /v1/leads/{id}

deleteLead()

↓

DELETE /v1/leads/{id}

It contains NO React code.

It contains NO business logic.

---

## CreateLeadDrawer.tsx

Purpose

Creates the User Experience for creating a Lead.

Responsibilities

Open Drawer

↓

Render LeadForm

↓

Submit Form

↓

Close Drawer after success

↓

Trigger refetch

No API URLs exist here.

No backend knowledge exists here.

---

## LeadForm.tsx

Purpose

Collect structured Lead information.

Responsibilities

Display fields

Collect input

Display validation errors

Call onSubmit()

LeadForm does NOT know

• Axios

• Backend

• Database

• SQL

It is a reusable form component only. :contentReference[oaicite:0]{index=0}

---

## lead.schema.ts

Purpose

Frontend Validation Layer.

Responsibilities

Validate user input before making API requests.

Example

Email format

PAN length

GSTIN length

Required fields

Revenue ≥ 0

Transform

Form Values

↓

API Payload

↓

Backend

It mirrors backend validation rather than inventing new business rules. :contentReference[oaicite:1]{index=1}

---

## lead.types.ts

Purpose

Type Contract between Frontend and Backend.

Responsibilities

Defines

LeadResponse

LeadCreatePayload

LeadUpdatePayload

LeadListResponse

Enums

No React

No Axios

No Validation

Only TypeScript contracts.

---

# Complete Frontend Runtime

User

↓

LeadList

↓

CreateLeadDrawer

↓

LeadForm

↓

lead.schema.ts

↓

useLeads.ts

↓

leadApi.ts

↓

Axios Client

↓

Backend API

↓

Axios Response

↓

useLeads updates state

↓

LeadList re-renders

↓

User sees updated UI

---

# Design Principle

Frontend exists to translate

Human Intent

↓

Structured HTTP Request

↓

Backend

and translate

Backend Response

↓

Visual Information

↓

Human Understanding

It should never become the source of business truth.

The Backend is always the Source of Truth.
