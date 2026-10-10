#!/usr/bin/env python3
"""
CreditBridge ERP - Direct Raw SQL Database Inspector
Connects directly to PostgreSQL using SQLAlchemy raw connection or psycopg2
and prints exact table counts and live rows without ORM overhead.
"""

import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.db.session import engine
from sqlalchemy import text

def inspect_sql():
    print("\n" + "=" * 80)
    print("🔍 CREDITBRIDGE ERP — RAW SQL LIVE DATABASE INSPECTION")
    print("=" * 80)

    with engine.connect() as conn:
        # 1. Businesses
        biz_res = conn.execute(text("SELECT id, business_name, owner_name, owner_phone, status FROM businesses")).fetchall()
        print(f"\n[1] BUSINESS TENANTS (Total: {len(biz_res)})")
        print("-" * 80)
        for b in biz_res:
            print(f"  • ID: {b[0]} | Name: {b[1]} | Owner: {b[2]} ({b[3]}) | Status: {b[4]}")

        active_id = biz_res[0][0] if biz_res else None

        # 2. Table Counts
        tables = [
            "accounts", "cost_centers", "modes_of_payment", "fiscal_years",
            "sales_invoices", "payment_entries", "journal_entries", "gl_entries"
        ]
        print(f"\n[2] RECORD COUNTS BY TABLE")
        print("-" * 80)
        for tbl in tables:
            try:
                cnt = conn.execute(text(f"SELECT count(*) FROM {tbl}")).scalar()
                print(f"  • {tbl:<25} : {cnt} rows")
            except Exception as e:
                print(f"  • {tbl:<25} : Error ({e})")

        # 3. Chart of Accounts Sample
        print(f"\n[3] CHART OF ACCOUNTS (First 15 Ledgers)")
        print("-" * 80)
        try:
            accs = conn.execute(text(
                "SELECT account_number, account_name, root_type, account_type, is_group "
                "FROM accounts ORDER BY account_number NULLS LAST LIMIT 15"
            )).fetchall()
            print(f"  {'Number':<12} | {'Account Name':<32} | {'Root':<10} | {'Type':<12} | {'Group?'}")
            print("  " + "-" * 76)
            for a in accs:
                is_grp = "Group" if a[4] else "Ledger"
                print(f"  {str(a[0] or '—'):<12} | {str(a[1]):<32} | {str(a[2] or '—'):<10} | {str(a[3] or '—'):<12} | {is_grp}")
        except Exception as e:
            print(f"  Error reading accounts: {e}")

        # 4. Sales Invoices
        print(f"\n[4] SALES INVOICES")
        print("-" * 80)
        try:
            sinvs = conn.execute(text(
                "SELECT name, customer, grand_total, outstanding_amount, status, docstatus "
                "FROM sales_invoices LIMIT 10"
            )).fetchall()
            if sinvs:
                for s in sinvs:
                    print(f"  • {s[0]} | {s[1]} | Total: ₹{float(s[2] or 0):,.2f} | Due: ₹{float(s[3] or 0):,.2f} | Status: {s[4]} | Docstatus: {s[5]}")
            else:
                print("  (Table 'sales_invoices' has 0 rows)")
        except Exception as e:
            print(f"  Error reading sales_invoices: {e}")

    print("\n" + "=" * 80)
    print("✅ RAW SQL INSPECTION FINISHED!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    inspect_sql()
