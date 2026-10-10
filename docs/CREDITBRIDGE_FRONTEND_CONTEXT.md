

# CreditBridge — ERP Frontend & Accounting Progress

## 1. Hum kya bana rahe hain

CreditBridge ko ERP-style architecture mein build kar rahe hain.

Basic flow:

```text
SIDEBAR
   ↓
MODULE
   ↓
MODULE DASHBOARD
   ↓
FREQUENTLY USED
   ↓
OTHER / VIEW ALL
   ↓
ALL DOMAINS
   ↓
DOMAIN
   ↓
LIST
   ↓
NEW / DETAIL / EDIT
```

Accounting ka flow:

```text
Accounting
   ↓
Accounting Dashboard
   ↓
Frequently Used
   ├── Payment Entry
   ├── Sales Invoice
   ├── Purchase Invoice
   ├── Journal Entry
   ├── Accounts Receivable
   └── Accounts Payable
   ↓
Other Accounting Domains
   ↓
All Accounting Domains
```

Hum dashboard par saare backend DocTypes nahi dikhayenge. User ko pehle commonly used kaam dikhega. Baaki domains `Other → View All` se milenge. 

---

# 2. Frontend structure

Current frontend structure:

```text
frontend/src/
│
├── app/
│   ├── accounting/
│   │   ├── page.tsx
│   │   ├── other/
│   │   │   └── page.tsx
│   │   └── payment-entry/
│   │       └── page.tsx
│   │
│   ├── favicon.ico
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
│
├── components/
│   └── navigation/
│       └── sidebar.tsx
│
├── config/
│   └── modules.ts
│
├── types/
│   └── module.ts
│
└── features/
    └── accounting/
        └── payment-entry/
            └── api/
                └── payment-entry.ts
```

Payment Entry API layer bhi frontend mein alag rakha gaya hai. 

---

# 3. Sidebar / Modules

Sidebar mein ERP modules hain:

```text
Home
Accounting
Buying
Selling
Stock
Assets
HR
Payroll
Manufacturing
CRM
Quality
Projects
Support
```

Accounting:

```text
/accounting
```

par jaata hai.

---

# 4. Accounting Dashboard

File:

```text
frontend/src/app/accounting/page.tsx
```

Dashboard mein:

```text
Frequently Used
```

ke andar:

```text
Payment Entry
Sales Invoice
Purchase Invoice
Journal Entry
Accounts Receivable
Accounts Payable
```

hain.

Payment Entry:

```text
/accounting/payment-entry
```

par jaata hai. 

Neeche:

```text
Other Accounting Domains
                    [View All →]
```

hai.

`View All`:

```text
/accounting/other
```

par jaata hai. 

---

# 5. Other Accounting Domains

File:

```text
frontend/src/app/accounting/other/page.tsx
```

Categories:

```text
Accounting Masters
Payments
Tax Masters
Cost Center and Budgeting
Multi Currency
Banking
Subscription Management
Share Management
```

Example:

```text
Payments
├── Payment Entry
├── Journal Entry
├── Journal Entry Template
├── Terms and Conditions
└── Mode of Payment
```

Ye page Accounting ka "all domains" layer hai. 

---

# 6. ERP navigation pattern

Ye pattern ab important architecture hai:

```text
MODULE
   ↓
MODULE DASHBOARD
   ↓
FREQUENTLY USED
   ↓
OTHER
   ↓
ALL DOMAINS
   ↓
DOMAIN
   ↓
LIST
   ↓
NEW / DETAIL / EDIT
```

Payment Entry example:

```text
Accounting
   ↓
Payment Entry
   ↓
Payment Entry List
   ↓
+ New Payment Entry
   ↓
New Payment Entry Form
```

Ye overall ERP navigation pattern pehle lock kiya gaya tha. 

---

# 7. Payment Entry — first real domain

Ab hum **Payment Entry** ko first proper end-to-end domain bana rahe hain.

Current list page:

```text
frontend/src/app/accounting/payment-entry/page.tsx
```

Next form:

```text
frontend/src/app/accounting/payment-entry/new/page.tsx
```

Route:

```text
/accounting/payment-entry/new
```

---

# 8. Sabse important rule: Backend is Source of Truth

Hum frontend fields guess nahi karenge.

Actual process:

```text
BACKEND MODEL
      ↓
SCHEMA
      ↓
SERVICE
      ↓
REPOSITORY
      ↓
API
      ↓
FRONTEND UI
```

Matlab:

```text
Backend batayega:
"What is Payment Entry?"

Frontend banayega:
"Isko user ko kaise dikhana hai?"
```

Backend ke actual fields, validation, relationships, child tables aur lifecycle ko follow karna hai.

---

# 9. PaymentEntry backend

Main model:

```text
backend/app/accounts/payment_entry_domain/models/payment_entry.py
```

Class:

```python
class PaymentEntry(SubmittableModel, TenantModel):
```

Payment types:

```text
Receive
Pay
Internal Transfer
```

Backend enum:

```python
class PaymentType(str, enum.Enum):
    RECEIVE = "Receive"
    PAY = "Pay"
    INTERNAL_TRANSFER = "Internal Transfer"
```

---

# 10. Actual Payment Entry fields

## Payment

```text
payment_type
posting_date
paid_from_id
paid_to_id
paid_amount
received_amount
```

## Currency

```text
source_exchange_rate
target_exchange_rate
paid_from_account_currency
paid_to_account_currency
```

## Party

```text
party_type
party
party_name
```

## Accounting

```text
cost_center_id
mode_of_payment
```

## Banking

```text
bank_account_id
party_bank_account_id
```

## Reference

```text
reference_no
reference_date
```

## Additional

```text
project
remarks
title
is_opening
apply_tds
```

## Identity

```text
name
naming_series
```

`name` backend generate karta hai.

Naming series:

```text
ACC-PAY-.YYYY.-
```

Repository generated name ko:

```text
ACC-PAY-<year>-<#####>
```

format mein banata hai.

---

# 11. Create form mein kya hoga

`PaymentEntryCreate` ke according main form:

```text
Payment Type
Posting Date

Paid From
Paid To

Paid Amount
Received Amount

Party Type
Party
Party Name

Mode of Payment
Bank Account
Party Bank Account
Cost Center

Reference No
Reference Date
Project

Source Exchange Rate
Target Exchange Rate

Title
Remarks

Is Opening
Apply TDS

References[]
Deductions[]
```

---

# 12. Derived fields — input nahi hain

Backend khud calculate karta hai:

```text
unallocated_amount
total_allocated_amount
total_deduction_amount
difference_amount
status
docstatus
```

Example calculation:

```text
allocated
    = sum(reference.allocated_amount)

deductions
    = sum(deduction.amount)

total_allocated_amount
    = allocated

total_deduction_amount
    = deductions

unallocated_amount
    = paid_amount
      - allocated
      - deductions
```

Isliye:

```text
unallocated_amount
total_allocated_amount
total_deduction_amount
```

**editable input nahi honge.**

Ye read-only/calculated information ho sakti hai.

Backend service mein ye totals child rows se calculate hote hain. 

---

# 13. Payment Entry ke child tables

Payment Entry ke andar:

```text
PaymentEntry
│
├── references[]
│
└── deductions[]
```

Backend mein separate domains:

```text
payment_entry_reference_domain
payment_entry_deduction_domain
```

hain.

Service references aur deductions ko child rows ke roop mein replace/create karti hai. 

---

# 14. References[]

Reference rows mein backend fields hain:

```text
reference_doctype
reference_name
due_date
bill_no
total_amount
outstanding_amount
allocated_amount
exchange_rate
payment_term
exchange_gain_loss
account_id
account_type
payment_type
payment_request
```

Backend duplicate references ko reject karta hai.

Allocated amount ko outstanding amount se bhi validate karta hai.

Internal Transfer ke liye allocated amount validation skip hoti hai. 

---

# 15. Deductions[]

Deduction rows:

```text
account_id
cost_center_id
amount
description
is_exchange_gain_loss
```

Deductions ka total backend calculate karta hai.

---

# 16. Payment Entry API

Current backend router:

```text
backend/app/accounts/payment_entry_domain/api/payment_entry.py
```

Backend `main.py` mein current registration:

```text
/v1/payment-entries
```

Operations:

```text
POST   /v1/payment-entries
GET    /v1/payment-entries
GET    /v1/payment-entries/{entry_id}
PATCH  /v1/payment-entries/{entry_id}
DELETE /v1/payment-entries/{entry_id}

POST   /v1/payment-entries/{entry_id}/submit
POST   /v1/payment-entries/{entry_id}/cancel
```

Child routers:

```text
/v1/payment-entry-deductions
/v1/payment-entry-references
```

---

# 17. Payment Entry List

Current frontend list page:

```text
frontend/src/app/accounting/payment-entry/page.tsx
```

UI:

```text
← Accounting

Payment Entry
Record money received, paid, or transferred internally

                    [+ New Payment Entry]
```

Filters:

```text
[ Search name, party or reference... ]
[ Payment Type ]
[ Status ]
[ Search ]
```

Table:

```text
ID
Type
Party
Posting Date
Amount
Status
```

Frontend backend se list load karta hai aur:

```text
loading
error
empty
data
```

states handle karta hai. 

---

# 18. Pagination

Frontend list mein:

```text
offset
limit
total
```

ka concept already hai.

Current limit:

```text
20
```

Backend bhi pagination support karta hai.

---

# 19. Search

Backend search support karta hai:

```text
name
party
party_name
reference_no
```

Frontend search input se query bhejta hai.

---

# 20. Payment Entry lifecycle

Payment Entry ek submittable document hai.

Lifecycle:

```text
Draft
   ↓
Submit
   ↓
Submitted
   ↓
Cancel
   ↓
Cancelled
```

Backend status:

```text
docstatus = draft
    → Draft

docstatus = submitted
    → Submitted

docstatus = cancelled
    → Cancelled
```

---

# 21. UI actions lifecycle ke according

### Draft

```text
[ Save ]
[ Submit ]
[ Delete ]
```

### Submitted

```text
[ Cancel ]
```

### Cancelled

```text
Read-only
```

Frontend ko fake status change nahi karna hai.

Actual backend endpoint call karna hai.

---

# 22. Submit ka matlab sirf status change nahi hai

Submit karne par backend GL entries post karta hai.

Concept:

```text
Paid From
    ↓
money leaves account

Paid To
    ↓
money arrives in account
```

Backend balanced GL entries create karta hai.

Cost center aur party information bhi GL posting mein carry hoti hai. 

Therefore:

```text
Submit
```

is a real accounting operation.

Sirf frontend mein:

```text
status = "Submitted"
```

karna enough nahi hai.

---

# 23. Cancel ka matlab bhi real operation hai

Submitted Payment Entry cancel hone par related GL entries reverse/cancel hoti hain.

Flow:

```text
Submitted
    ↓
Cancel
    ↓
GL reversal
```

Isliye frontend ko actual:

```text
POST /v1/payment-entries/{entry_id}/cancel
```

call karna hoga.

---

# 24. Backend validation

Backend important validations karta hai.

Mandatory:

```text
Paid Amount
Received Amount
Source Exchange Rate
Target Exchange Rate
```

Currency rule:

```text
If paid-from currency
==
paid-to currency

Received Amount
must not be greater than
Paid Amount
```

Duplicate references allowed nahi hain.

Allocated amount outstanding amount se exceed nahi kar sakta where applicable.

Posting date active Fiscal Year mein honi chahiye. 

---

# 25. Related IDs ko simple text nahi banana

Fields:

```text
paid_from_id
paid_to_id
cost_center_id
bank_account_id
party_bank_account_id
```

IDs/relationships hain.

Eventually UI mein:

```text
Paid From
[ Select Account ▼ ]

Paid To
[ Select Account ▼ ]

Cost Center
[ Select Cost Center ▼ ]

Bank Account
[ Select Bank Account ▼ ]
```

hona chahiye.

Hard-coded fake options nahi banane.

Related backend domains ke actual APIs/contracts discover karke selectors connect karne hain.

---

# 26. New Payment Entry UI structure

New page:

```text
/accounting/payment-entry/new
```

Suggested UI:

```text
New Payment Entry
│
├── Payment Information
│   ├── Payment Type
│   ├── Posting Date
│   ├── Paid From
│   ├── Paid To
│   ├── Paid Amount
│   └── Received Amount
│
├── Party
│   ├── Party Type
│   ├── Party
│   └── Party Name
│
├── Payment & Banking
│   ├── Mode of Payment
│   ├── Bank Account
│   ├── Party Bank Account
│   └── Cost Center
│
├── Currency
│   ├── Source Exchange Rate
│   ├── Target Exchange Rate
│   ├── Paid From Account Currency
│   └── Paid To Account Currency
│
├── Reference
│   ├── Reference No
│   └── Reference Date
│
├── Additional Information
│   ├── Project
│   ├── Title
│   └── Remarks
│
├── Options
│   ├── Is Opening
│   └── Apply TDS
│
├── References[]
│
└── Deductions[]
```

Ye **UI grouping** hai. Backend field names/payload exactly backend schema ke according rahenge.

---

# 27. Important API path issue

Development ke dauran frontend ke ek earlier version mein route tha:

```text
/v1/accounts/payment-entry
```

Lekin current backend `main.py` registration hai:

```text
/v1/payment-entries
```

Therefore final integration se pehle frontend API file ko current backend route ke saath align karna zaroori hai.

**Current backend route source of truth hai.**

---

# 28. Ab tak kya complete hua

```text
[✓] Application shell
[✓] Sidebar
[✓] Module navigation
[✓] Accounting dashboard
[✓] Frequently Used section
[✓] Other Accounting Domains
[✓] Payment Entry list route
[✓] Payment Entry list UI
[✓] Payment Entry frontend API structure
[✓] PaymentEntry backend model inspected
[✓] PaymentEntry schema inspected
[✓] PaymentEntry repository inspected
[✓] PaymentEntry service inspected
[✓] PaymentEntry API inspected
[✓] PaymentEntry Reference domain inspected
[✓] PaymentEntry Deduction domain inspected
[✓] Backend business rules identified
[✓] Payment Entry lifecycle identified
```

---

# 29. Ab next kya banana hai

```text
[ ] /accounting/payment-entry/new/page.tsx

[ ] Connect POST /v1/payment-entries

[ ] Real Account selectors

[ ] Real Cost Center selector

[ ] Real Bank Account selector

[ ] Party selector

[ ] References[] table

[ ] Deductions[] table

[ ] Calculated totals

[ ] Save Draft

[ ] Submit

[ ] Payment Entry Detail

[ ] Edit Draft

[ ] Cancel Submitted Payment Entry

[ ] Complete end-to-end testing
```

---

# 30. Sabse important development principle

CreditBridge mein hum ye nahi karenge:

```text
Pehle pretty UI banao
↓
baad mein backend adjust karo
```

Hum ye karenge:

```text
BACKEND DOMAIN
      ↓
ACTUAL MODEL
      ↓
ACTUAL SCHEMA
      ↓
ACTUAL BUSINESS RULES
      ↓
ACTUAL API
      ↓
UI
```

Simple words mein:

> **Backend batayega ki system kya kar sakta hai. Frontend usko user ke liye achhe tareeke se dikhayega.**

Isi wajah se Payment Entry ko pehla proper end-to-end domain bana rahe hain.

---

# 31. Final target

Payment Entry ka final flow:

```text
Accounting
    ↓
Payment Entry
    ↓
Payment Entry List
    ↓
+ New Payment Entry
    ↓
Fill actual backend fields
    ↓
Save
    ↓
Draft
    ↓
Submit
    ↓
Backend validation
    ↓
GL Posting
    ↓
Submitted
    ↓
Cancel
    ↓
GL Reversal
    ↓
Cancelled
```

**Ye Payment Entry ka actual CreditBridge flow hai.**

Aur isi pattern ko successfully complete karne ke baad same architecture ko:

```text
Sales Invoice
Purchase Invoice
Journal Entry
Stock
Assets
HR
CRM
...
```

par apply karenge.
 ,,, 

 Haan. Ab **README mein isi point ko proper project documentation ke form mein likhna hai**. Main isko simple language mein, but technical details ke saath, aise structure kar raha hoon ki baad mein tu khud padh ke samajh sake ki **frontend mein kya bana, backend kya karta hai, aur next kya karna hai**.

Is section ko README mein **existing Payment Entry documentation ke baad** add kar:

````md
# Payment Entry — Frontend + Backend Integration

Payment Entry CreditBridge ERP ka pehla proper end-to-end accounting domain hai.

Iska purpose hai:

- money receive karna
- money pay karna
- internal account transfer record karna
- payment ko accounting ledger mein post karna
- payment ko cancel karne par ledger entries reverse karna

Important principle:

> Frontend backend ke fields aur business rules ko follow karega.
> Frontend apni taraf se accounting logic invent nahi karega.

The backend is the source of truth.

---

# 17. Payment Entry List

Current frontend list page:

```text
frontend/src/app/accounting/payment-entry/page.tsx
````

Payment Entry ko Accounting dashboard se open kiya ja sakta hai:

```text
Accounting
    ↓
Payment Entry
    ↓
Payment Entry List
```

Current page ka purpose existing Payment Entries ko backend se load karke user ko list mein dikhana hai.

---

## 17.1 Payment Entry List Header

UI:

```text
← Accounting

Payment Entry
Record money received, paid, or transferred internally

                    [+ New Payment Entry]
```

`New Payment Entry` button:

```text
/accounting/payment-entry/new
```

par navigate karta hai.

---

## 17.2 Filters

Payment Entry list mein filters hain:

```text
[ Search name, party or reference... ]

[ Payment Type ]

[ Status ]

[ Search ]
```

### Payment Type

Backend supported values:

```text
Receive
Pay
Internal Transfer
```

### Status

Backend `docstatus` ke according:

```text
0 → Draft
1 → Submitted
2 → Cancelled
```

---

## 17.3 Search

Backend search in fields par kaam karta hai:

```text
name
party
party_name
reference_no
```

Frontend search value backend ko:

```text
search
```

query parameter ke through bhejta hai.

Example:

```text
GET /v1/payment-entries?search=Rahul
```

Actual backend route:

```text
/v1/payment-entries
```

Important:

Earlier frontend implementation mein route:

```text
/v1/accounts/payment-entry
```

use hua tha.

Current backend `main.py` ke according correct route hai:

```text
/v1/payment-entries
```

Therefore frontend API integration ko current backend route ke saath aligned rakhna hai.

---

# 17.4 Payment Entry Table

List UI mein important fields:

```text
ID
Type
Party
Posting Date
Amount
Status
```

More complete list implementation mein:

```text
Payment Entry
Date
Type
Party
Amount
Allocated
Unallocated
Status
```

Payment Entry name clickable hona chahiye:

```text
/accounting/payment-entry/{id}
```

Isse future mein Payment Entry Detail page open hoga.

---

# 17.5 Frontend List States

List page ko backend request ke different states handle karne hain:

```text
Loading
    ↓
Data
```

ya:

```text
Loading
    ↓
Error
```

ya:

```text
Loading
    ↓
Empty
```

### Loading

```text
Loading Payment Entries...
```

### Error

Backend/API request fail hone par error message show hoga.

### Empty

Agar backend se koi Payment Entry nahi aati:

```text
No Payment Entries found.
```

Aur user ko:

```text
Create your first Payment Entry
```

ka option diya ja sakta hai.

---

# 18. Pagination

Payment Entry backend pagination support karta hai.

Main parameters:

```text
offset
limit
```

Backend response mein:

```text
items
total
offset
limit
```

type ka paginated result use hota hai.

Current frontend page size:

```text
20
```

Example:

```text
offset=0
limit=20
```

Next page:

```text
offset=20
limit=20
```

Pagination ka basic concept:

```text
Total = 47

Page 1
offset=0
limit=20

Page 2
offset=20
limit=20

Page 3
offset=40
limit=20
```

Frontend ko backend ke `total` ko use karke next/previous pagination control manage karna hai.

---

# 19. Payment Entry Backend Structure

Payment Entry backend domain:

```text
backend/app/accounts/payment_entry_domain/
```

Structure:

```text
payment_entry_domain/
│
├── api/
│   └── payment_entry.py
│
├── models/
│   └── payment_entry.py
│
├── repositories/
│   └── payment_entry_repository.py
│
├── schemas/
│   └── payment_entry.py
│
└── services/
    └── payment_entry_service.py
```

Payment Entry ke saath do child domains bhi exist karte hain:

```text
payment_entry_reference_domain
payment_entry_deduction_domain
```

Relationship:

```text
PaymentEntry
│
├── references[]
│
└── deductions[]
```

---

# 20. Payment Entry Model

Main backend model:

```text
PaymentEntry
```

Database table:

```text
payment_entries
```

Payment Entry supported payment types:

```text
Receive
Pay
Internal Transfer
```

---

# 21. Payment Entry Fields

Backend model ke actual fields:

## Identity

```text
id
business_id
name
naming_series
```

`name` naming series se generate hota hai.

Current naming series:

```text
ACC-PAY-.YYYY.-
```

Example:

```text
ACC-PAY-2026-00001
```

---

## Payment Information

```text
payment_type
posting_date
paid_from_id
paid_to_id
paid_amount
received_amount
```

Meaning:

```text
Payment Type
    ↓
Receive / Pay / Internal Transfer

Posting Date
    ↓
Accounting transaction date

Paid From
    ↓
Money kis account se ja raha hai

Paid To
    ↓
Money kis account mein ja raha hai

Paid Amount
    ↓
Payment amount

Received Amount
    ↓
Received amount
```

---

# 22. Currency Fields

Backend fields:

```text
source_exchange_rate
target_exchange_rate

paid_from_account_currency
paid_to_account_currency
```

Exchange rates backend business logic ka part hain.

Default exchange rate:

```text
1.0
```

---

# 23. Party Fields

Backend:

```text
party_type
party
party_name
```

Example conceptual UI:

```text
Party Type
[ Customer ▼ ]

Party
[ Select Customer ▼ ]

Party Name
[ Customer Name ]
```

Important:

`party` ko simple random text field nahi banana chahiye agar related party domain/API available hai.

Actual backend contract discover karke selector connect karna hai.

---

# 24. Accounting Fields

Backend:

```text
cost_center_id
mode_of_payment
```

UI:

```text
Cost Center
[ Select Cost Center ▼ ]

Mode of Payment
[ Select Mode of Payment ▼ ]
```

---

# 25. Banking Fields

Backend:

```text
bank_account_id
party_bank_account_id
```

UI eventually:

```text
Bank Account
[ Select Bank Account ▼ ]

Party Bank Account
[ Select Party Bank Account ▼ ]
```

These are relationship IDs.

Therefore frontend ko fake hard-coded UUIDs nahi bhejne.

---

# 26. Reference Fields

Main Payment Entry fields:

```text
reference_no
reference_date
```

Additionally Payment Entry has:

```text
references[]
```

Child reference rows are handled by the separate:

```text
PaymentEntryReference
```

domain.

---

# 27. Additional Fields

Backend:

```text
project
remarks
title
```

UI:

```text
Project
Title
Remarks
```

---

# 28. Options

Backend:

```text
is_opening
apply_tds
```

UI:

```text
Is Opening
[ toggle ]

Apply TDS
[ toggle ]
```

---

# 29. Derived Fields

Payment Entry backend mein kuch fields calculated/derived hain.

Examples:

```text
unallocated_amount
total_allocated_amount
total_deduction_amount
difference_amount
```

These are NOT normal user input fields.

Important rule:

```text
User Input
    ↓
Backend Calculation
    ↓
Derived Values
```

Therefore frontend mein:

```text
unallocated_amount
total_allocated_amount
total_deduction_amount
```

ko editable `<input>` nahi banana.

Ye values backend se read karke display ki ja sakti hain.

---

# 30. Payment Entry References

Payment Entry ke andar:

```text
references[]
```

child rows hain.

Concept:

```text
Payment Entry
    ↓
References
    ├── Invoice 1
    ├── Invoice 2
    └── Invoice 3
```

Reference rows allocated payment ko invoices/payment requests etc. ke against track karne ke liye use hote hain.

Backend duplicate references validate karta hai.

Duplicate reference combination allowed nahi hai.

---

# 31. Payment Entry Deductions

Payment Entry ke andar:

```text
deductions[]
```

child rows hain.

Concept:

```text
Payment Entry
    ↓
Deductions
    ├── Deduction 1
    ├── Deduction 2
    └── ...
```

Backend deductions ka total calculate karta hai.

---

# 32. Amount Calculation

Backend references se:

```text
total_allocated_amount
```

calculate karta hai.

Deductions se:

```text
total_deduction_amount
```

calculate hota hai.

Then unallocated amount calculate hota hai:

```text
Unallocated Amount
=
Paid Amount
-
Total Allocated Amount
-
Total Deduction Amount
```

Therefore:

```text
Paid Amount
      │
      ├──────────────→ Allocated
      │
      ├──────────────→ Deductions
      │
      └──────────────→ Unallocated
```

Frontend ko backend calculation ko replace nahi karna hai.

---

# 33. Payment Entry Validation

Backend important validations perform karta hai.

Mandatory business fields include:

```text
Paid Amount
Received Amount
Source Exchange Rate
Target Exchange Rate
```

Frontend helpful client-side validation dikha sakta hai, but final validation backend karega.

Important principle:

```text
Frontend validation
        ↓
User experience

Backend validation
        ↓
Actual authority
```

---

# 34. Received Amount Validation

Agar:

```text
paid_from_account_currency
==
paid_to_account_currency
```

to:

```text
received_amount
```

paid amount se greater nahi ho sakta.

Rule:

```text
Received Amount <= Paid Amount
```

Otherwise backend validation error return karega.

---

# 35. Reference Validation

Backend duplicate references detect karta hai.

Reference identity mein fields ka combination important hai:

```text
reference_doctype
reference_name
payment_term
payment_request
```

Same combination duplicate hone par backend validation error deta hai.

---

# 36. Allocated Amount Validation

Normal payment ke liye:

```text
allocated_amount
```

outstanding amount se greater nahi hona chahiye.

Internal Transfer ke case mein allocation validation skip hota hai.

Therefore frontend ko payment type ke according reference UI behavior eventually adjust karna hoga.

---

# 37. Payment Entry Lifecycle

Payment Entry ek submittable document hai.

Lifecycle:

```text
Draft
   ↓
Submit
   ↓
Submitted
   ↓
Cancel
   ↓
Cancelled
```

Backend `docstatus`:

```text
0 → Draft
1 → Submitted
2 → Cancelled
```

---

# 38. Draft UI

Draft Payment Entry mein actions:

```text
[ Save ]
[ Submit ]
[ Delete ]
```

Delete sirf draft entry ke liye allowed hai.

---

# 39. Submitted UI

Submitted Payment Entry:

```text
[ Cancel ]
```

Submitted document ko normal draft ki tarah edit nahi karna.

---

# 40. Cancelled UI

Cancelled Payment Entry:

```text
Read-only
```

Frontend ko cancelled state mein normal editing controls nahi dikhane.

---

# 41. Submit Is a Real Accounting Operation

Submit ka matlab sirf:

```text
status = Submitted
```

karna nahi hai.

Backend submit ke time GL entries post karta hai.

Concept:

```text
Paid From Account
        ↓
Credit

Paid To Account
        ↓
Debit
```

Backend balanced GL entries create karta hai.

GL entries mein information include ho sakti hai:

```text
account_id
cost_center_id
party_type
party
posting_date
voucher_type
voucher_no
remarks
```

Therefore:

```text
Submit Payment Entry
        ↓
Backend validation
        ↓
GL posting
        ↓
Payment Entry Submitted
```

---

# 42. Cancel Is Also a Real Accounting Operation

Cancel sirf frontend status update nahi hai.

Flow:

```text
Submitted Payment Entry
        ↓
Cancel
        ↓
Backend cancellation
        ↓
GL entries reversed/cancelled
        ↓
Payment Entry Cancelled
```

Frontend actual backend endpoint call karega:

```text
POST /v1/payment-entries/{entry_id}/cancel
```

---

# 43. Backend API

Current Payment Entry API prefix:

```text
/v1/payment-entries
```

Available operations:

```text
POST   /v1/payment-entries
GET    /v1/payment-entries
GET    /v1/payment-entries/{entry_id}
PATCH  /v1/payment-entries/{entry_id}
DELETE /v1/payment-entries/{entry_id}

POST   /v1/payment-entries/{entry_id}/submit
POST   /v1/payment-entries/{entry_id}/cancel
```

Meaning:

```text
POST
    Create Draft

GET
    List Payment Entries

GET /{id}
    Get Payment Entry

PATCH /{id}
    Update Draft

DELETE /{id}
    Delete Draft

POST /{id}/submit
    Submit Draft

POST /{id}/cancel
    Cancel Submitted Entry
```

---

# 44. New Payment Entry Page

Route:

```text
/accounting/payment-entry/new
```

File:

```text
frontend/src/app/accounting/payment-entry/new/page.tsx
```

This is the next major frontend page.

The page must be based on the actual backend `PaymentEntryCreate` schema.

---

# 45. New Payment Entry UI Structure

Recommended UI grouping:

```text
New Payment Entry
│
├── Payment Information
│   ├── Payment Type
│   ├── Posting Date
│   ├── Paid From
│   ├── Paid To
│   ├── Paid Amount
│   └── Received Amount
│
├── Party
│   ├── Party Type
│   ├── Party
│   └── Party Name
│
├── Payment & Banking
│   ├── Mode of Payment
│   ├── Bank Account
│   ├── Party Bank Account
│   └── Cost Center
│
├── Currency
│   ├── Source Exchange Rate
│   ├── Target Exchange Rate
│   ├── Paid From Account Currency
│   └── Paid To Account Currency
│
├── Reference
│   ├── Reference No
│   └── Reference Date
│
├── Additional Information
│   ├── Project
│   ├── Title
│   └── Remarks
│
├── Options
│   ├── Is Opening
│   └── Apply TDS
│
├── References[]
│
└── Deductions[]
```

This grouping is only for UI organization.

The actual API payload must continue to use backend field names.

---

# 46. Important: Relationship Fields

Fields ending in `_id` are generally relationships.

Examples:

```text
paid_from_id
paid_to_id
cost_center_id
bank_account_id
party_bank_account_id
```

Therefore UI should eventually use selectors:

```text
Paid From
[ Select Account ▼ ]

Paid To
[ Select Account ▼ ]

Cost Center
[ Select Cost Center ▼ ]

Bank Account
[ Select Bank Account ▼ ]

Party Bank Account
[ Select Bank Account ▼ ]
```

Do NOT create fake hard-coded database IDs.

The related backend domains and APIs should be discovered first.

---

# 47. Frontend Architecture

Payment Entry frontend API should live under:

```text
frontend/src/features/accounting/payment-entry/
```

Recommended structure:

```text
payment-entry/
│
├── api/
│   └── payment-entry.ts
│
├── components/
│   ├── payment-entry-form.tsx
│   ├── payment-entry-references.tsx
│   └── payment-entry-deductions.tsx
│
└── ...
```

Application routes:

```text
frontend/src/app/accounting/payment-entry/
│
├── page.tsx
│
├── new/
│   └── page.tsx
│
└── [id]/
    └── page.tsx
```

---

# 48. Current Frontend Structure

Current frontend contains:

```text
frontend/src/
│
├── app/
│   ├── accounting/
│   │   ├── page.tsx
│   │   ├── other/
│   │   │   └── page.tsx
│   │   └── payment-entry/
│   │       └── page.tsx
│   │
│   ├── page.tsx
│   └── globals.css
│
├── components/
│   └── navigation/
│       └── sidebar.tsx
│
├── config/
│   └── modules.ts
│
└── types/
    └── module.ts
```

Payment Entry API layer:

```text
frontend/src/features/accounting/payment-entry/api/payment-entry.ts
```

API client:

```text
frontend/src/lib/api/client.ts
```

---

# 49. ERP Navigation Pattern

CreditBridge ka frontend navigation pattern:

```text
MODULE
   ↓
MODULE DASHBOARD
   ↓
FREQUENTLY USED
   ↓
OTHER
   ↓
ALL DOMAINS
   ↓
DOMAIN
   ↓
LIST
   ↓
NEW / DETAIL / EDIT
```

Accounting example:

```text
Accounting
    ↓
Accounting Dashboard
    ↓
Payment Entry
    ↓
Payment Entry List
    ↓
New Payment Entry
```

This pattern will later be reused for other modules.

---

# 50. Why We Are Doing It This Way

Hum har page manually random way mein nahi bana rahe.

Instead:

```text
Backend Domain
      ↓
Model
      ↓
Schema
      ↓
Repository
      ↓
Service
      ↓
API
      ↓
Frontend API
      ↓
List UI
      ↓
Create UI
      ↓
Detail UI
      ↓
Edit UI
```

Backend tells us:

```text
What data exists
What data is required
What relationships exist
What validations exist
What calculations happen
What actions are allowed
```

Frontend's job is:

```text
Make those operations usable for the user.
```

---

# 51. Current Progress

Completed:

```text
[✓] Application shell
[✓] Sidebar
[✓] Module navigation
[✓] Accounting dashboard
[✓] Frequently Used section
[✓] Other Accounting Domains
[✓] Payment Entry list route
[✓] Payment Entry list UI
[✓] Payment Entry frontend API structure
[✓] PaymentEntry backend model inspected
[✓] PaymentEntry schema inspected
[✓] PaymentEntry repository inspected
[✓] PaymentEntry service inspected
[✓] PaymentEntry API inspected
[✓] PaymentEntry Reference domain inspected
[✓] PaymentEntry Deduction domain inspected
[✓] Backend business rules identified
[✓] Payment Entry lifecycle identified
```

---

# 52. Remaining Payment Entry Work

```text
[ ] /accounting/payment-entry/new/page.tsx

[ ] Connect POST /v1/payment-entries

[ ] Real Account selectors

[ ] Real Cost Center selector

[ ] Real Bank Account selector

[ ] Real Party selector

[ ] References[] UI

[ ] Deductions[] UI

[ ] Calculated totals display

[ ] Save Draft

[ ] Submit

[ ] Payment Entry Detail

[ ] Edit Draft

[ ] Cancel Submitted Payment Entry

[ ] Complete end-to-end testing
```

---

# 53. Final Payment Entry Flow

The complete target flow:

```text
Accounting
    ↓
Payment Entry
    ↓
Payment Entry List
    ↓
+ New Payment Entry
    ↓
Fill Payment Entry
    ↓
Save
    ↓
Draft
    ↓
Submit
    ↓
Backend Validation
    ↓
GL Posting
    ↓
Submitted
    ↓
Cancel
    ↓
GL Reversal
    ↓
Cancelled
```

---

# 54. Core Development Principle

CreditBridge development ka main rule:

```text
Do not build UI first and force the backend to fit it.
```

Instead:

```text
BACKEND DOMAIN
      ↓
ACTUAL MODEL
      ↓
ACTUAL SCHEMA
      ↓
ACTUAL BUSINESS RULES
      ↓
ACTUAL API
      ↓
FRONTEND
```

Simple words:

> Backend batayega system kya kar sakta hai.
> Frontend us capability ko user ke liye usable banayega.

Payment Entry is the first domain where we are following this complete process.

After Payment Entry is completed end-to-end, the same architecture can be reused for:

```text
Sales Invoice
Purchase Invoice
Journal Entry
Accounts Receivable
Accounts Payable
Stock
Assets
HR
Payroll
Manufacturing
CRM
Quality
Projects
Support
```

The goal is not to manually create hundreds of unrelated pages.

The goal is to establish a consistent ERP domain architecture that can scale across CreditBridge.

```

**Ye version README ke liye sahi hai:** isme ab tak frontend mein kya hua, backend se kya discover hua, actual API route kya hai, Payment Entry ka data flow kya hai, lifecycle kya hai, aur **exact next work** kya hai — sab ek jagah locked hai. :contentReference[oaicite:0]{index=0}
```
