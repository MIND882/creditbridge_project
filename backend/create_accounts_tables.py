#!/usr/bin/env python3
"""
CreditBridge ERP - Create All 191 Accounts Tables
Connects to PostgreSQL via DATABASE_URL and creates all 191 accounts tables.
"""

import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.db.session import engine, Base
from app.config import settings

# 1. Import core models
import app.models

# 2. Import all 191 accounts models
print("Importing all 191 Accounts Domain models...")
import app.accounts.all_models

print(f"Total tables registered in SQLAlchemy metadata: {len(Base.metadata.tables)}")

# 3. Create all tables in database
print(f"Connecting to database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}...")
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Successfully executed Base.metadata.create_all()!")
except Exception as e:
    print(f"✗ Error during create_all: {e}")
    sys.exit(1)

# 4. Verify created tables in PostgreSQL
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """))
    tables = [row[0] for row in result.fetchall()]

print("\n" + "=" * 60)
print(f"DATABASE VERIFICATION SUMMARY:")
print(f"Total tables in public schema: {len(tables)}")
print("=" * 60)

accounts_tables = [t for t in tables if t not in [
    'audit_logs', 'bank_accounts', 'bank_transactions', 'businesses',
    'ca_partners', 'consents', 'customers', 'gst_filings', 'invoices',
    'lead_activities', 'lead_ai_insights', 'lead_attachments', 'leads',
    'lenders', 'loan_offers', 'opportunities', 'payment_reminders',
    'rejections', 'risk_scores'
]]

print(f"Core Platform Tables: {len(tables) - len(accounts_tables)}")
print(f"Accounts Module Tables: {len(accounts_tables)}")
print("\nFirst 30 Accounts Tables:")
for t in accounts_tables[:30]:
    print(f"  • {t}")

if len(accounts_tables) > 30:
    print(f"  ... and {len(accounts_tables) - 30} more accounts tables.")
print("=" * 60)
