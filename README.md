# CreditBridge ERP — Unified Workspace & Architecture Guide

Welcome to the unified CreditBridge ERP repository. This repository organizes both the **FastAPI Backend** and the **Generic Engine Frontend** for all **191 Accounting Domains** in a clean, non-duplicated structure.

---

## 1. Directory Structure

```text
/home/user/
├── backend/                       # Python FastAPI Backend
│   ├── app/
│   │   ├── accounts/              # All 191 accounting domain folders (*_domain)
│   │   │   ├── account_domain/    # models, api, schemas, repositories, services
│   │   │   ├── sales_invoice_domain/
│   │   │   ├── payment_entry_domain/
│   │   │   └── ... (191 domains)
│   │   ├── api/                   # Core API routes (auth, business, KYC, loans, etc.)
│   │   ├── models/                # Core SQLAlchemy models
│   │   ├── services/              # Integrations & provider adapters
│   │   ├── main.py                # Router registrations & API prefixes
│   │   └── config.py              # Environment configuration
│   ├── alembic.ini                # Database migrations
│   └── requirements.txt           # Python dependencies
│
├── frontend/                      # React 19 + Tailwind CSS + Vite Generic Engine Frontend
│   ├── src/
│   │   ├── App.jsx                # View router & state controller
│   │   ├── data/
│   │   │   ├── accountsMetadata.json # 191 domains with backend models, endpoints & seed data
│   │   │   └── otherModules.js    # Selling, Buying, Stock, Manufacturing, CRM overviews
│   │   ├── context/
│   │   │   └── RecordsContext.jsx # In-memory reactive state management
│   │   └── components/
│   │       ├── Sidebar.jsx        # Module-only left navigation (Dashboard, Accounting, etc.)
│   │       ├── Header.jsx         # Breadcrumbs, quick jump, and search trigger
│   │       ├── DashboardView.jsx  # ERP overview & financial KPIs
│   │       ├── AccountingHubView.jsx # 191-domain directory & 1-by-1 navigator
│   │       ├── GenericListView.jsx # Generic List view with backend specs toggle
│   │       ├── GenericDetailView.jsx # Generic Detail view with DB mapping & action buttons
│   │       ├── GenericFormView.jsx # Generic Create/Edit form with validation
│   │       ├── BackendInspector.jsx # FastAPI endpoints & SQLAlchemy database schema inspector
│   │       ├── AccountsReceivableView.jsx # Aging report with overdue buckets
│   │       ├── ModulePlaceholderView.jsx # Overview view for other ERP modules
│   │       ├── CommandPaletteModal.jsx # Global ⌘K / ⌘G search modal
│   │       ├── PrintModal.jsx     # Printable invoice / voucher modal
│   │       └── Toast.jsx          # Toast feedback notifications
│   ├── package.json               # Frontend dependencies & scripts
│   ├── vite.config.js             # Vite configuration with singlefile & CORS
│   └── dist/index.html            # Compiled production deliverable (1.3 MB)
│
├── docs/                          # Architecture, PRD, design system & API specifications
│   ├── ARCHITECTURE.md            # System architecture boundaries
│   ├── PRD.md                     # Product requirements document
│   ├── DESIGN.md                  # Product & design direction
│   ├── RULES.md                   # Engineering standards & boundary rules
│   ├── TASKS.md                   # Feature tracking queue
│   ├── API_DOCS.md                # Backend API documentation
│   ├── README_ACCOUNTING_FRONTEND_SETUP.md # Detailed 191 accounting domain specifications
│   └── Erpnext-Generic-Engine-Screens.html # Original design reference
│
└── CreditBridge-ERP-Accounting-191-Domains.html # Standalone single-file HTML deliverable
```

---

## 2. Organization & De-duplication Summary

- **`backend_repo` removed:** The cloned temporary repository was split into root `backend/` and merged documentation under `docs/`.
- **`frontend-lender` excluded:** As requested, the lender frontend has been removed as it is not needed for the operational ERP frontend.
- **`app/` moved to `frontend/`:** The separate `app/` folder was promoted to the standard `frontend/` directory, serving as the official user interface.
- **Scratch files deleted:** All intermediate raw JSON dumps (`doctypes_raw/`, `accounts_doctypes_191.json`) were cleaned up. The consolidated dataset lives in `frontend/src/data/accountsMetadata.json`.

---

## 3. Backend & Database Integration for All 191 Domains

The frontend Generic Engine is directly wired to the backend structure:
- **728 FastAPI Endpoints:** Mapped from `backend/app/main.py` and `backend/app/accounts/*_domain/api/`.
- **2,395 Database Columns:** Extracted from SQLAlchemy `models/*.py` with exact types, nullability, and defaults.
- **28 Foreign Key Relationships:** Detailed entity relations (e.g. `paid_from -> accounts.id`, `cost_center -> cost_centers.id`, `parent_account -> accounts.id`).
- **Interactive Backend Inspector:** View live endpoints, table schemas, and foreign keys on any domain via the **`Backend API & DB`** / **`Backend Specs`** toggle.

---

## 4. Running the Development Server

The live preview runs directly from `frontend/`:

```bash
cd /home/user/frontend
npm run dev
```

- **Host & Port:** `0.0.0.0:3000`
- **Live Preview:** Viewable in the live preview window.
- **Production Build:** `npm run build` compiles into `dist/index.html` (also copied to `CreditBridge-ERP-Accounting-191-Domains.html`).
