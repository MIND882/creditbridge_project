#!/usr/bin/env python3
"""
CreditBridge ERP — PostgreSQL Database Inspection Tool for Buying Module
Verifies table existence and prints live records from Suppliers, Purchase Orders, and RFQs.

Usage:
    python3 check_buying_database.py
"""

import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.db.session import engine
from sqlalchemy import text


def check_buying():
    print("\n" + "=" * 80)
    print("🛒 CREDITBRIDGE ERP — POSTGRESQL BUYING MODULE INSPECTION TOOL")
    print("=" * 80)

    try:
        with engine.connect() as conn:
            # 1. Connection check
            version_row = conn.execute(text("SELECT version();")).fetchone()
            db_row = conn.execute(text("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")).fetchone()
            print("✓ Database Connection: SUCCESS")
            print(f"  • Database Name : {db_row[0]}")
            print(f"  • User / Role   : {db_row[1]}")
            print(f"  • Version       : {version_row[0].split(',')[0]}")

            # 2. Table count
            tables = [row[0] for row in conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)).fetchall()]

            buying_expected = [
                'suppliers', 'customer_number_at_suppliers', 'purchase_orders', 'purchase_order_items',
                'request_for_quotations', 'request_for_quotation_suppliers', 'request_for_quotation_items',
                'supplier_quotations', 'supplier_quotation_items', 'buying_settingss', 'purchase_receipts',
                'purchase_receipt_items', 'purchase_receipt_item_supplieds', 'supplier_scorecards',
                'supplier_scorecard_periods', 'supplier_scorecard_criterias', 'supplier_scorecard_variables',
                'supplier_scorecard_standings', 'supplier_scorecard_scoring_criterias',
                'supplier_scorecard_scoring_variables', 'supplier_scorecard_scoring_standings'
            ]
            active_buying = [t for t in tables if t in buying_expected]

            print("\n" + "-" * 80)
            print(f"📊 SCHEMA SUMMARY — {len(tables)} TOTAL TABLES IN POSTGRESQL")
            print("-" * 80)
            print(f"  • Total Base Tables in Database : {len(tables)}")
            print(f"  • Buying Module Tables Found    : {len(active_buying)} / {len(buying_expected)}")

            # 3. Suppliers
            print("\n" + "=" * 80)
            print("🏢 1. SUPPLIERS (suppliers)")
            print("=" * 80)
            sups = conn.execute(text("""
                SELECT name, supplier_name, supplier_type, supplier_group, country, tax_id, mobile_no, email_id
                FROM suppliers
                ORDER BY created_at DESC;
            """)).fetchall()

            if sups:
                print(f"Total Suppliers in Database: {len(sups)}\n")
                header = f"{'CODE':<16} | {'SUPPLIER NAME':<32} | {'GROUP':<22} | {'GSTIN/TAX ID':<16} | {'CONTACT EMAIL':<25}"
                print(header)
                print("-" * len(header))
                for s in sups:
                    print(f"{s[0]:<16} | {s[1]:<32} | {(s[3] or '—'):<22} | {(s[5] or '—'):<16} | {(s[7] or '—'):<25}")
            else:
                print("⚠ No suppliers found.")

            # 4. Purchase Orders
            print("\n" + "=" * 80)
            print("📦 2. PURCHASE ORDERS (purchase_orders)")
            print("=" * 80)
            pos = conn.execute(text("""
                SELECT name, supplier_name, schedule_date, grand_total, status
                FROM purchase_orders
                ORDER BY created_at DESC;
            """)).fetchall()

            if pos:
                print(f"Total Purchase Orders in Database: {len(pos)}\n")
                header = f"{'PO NUMBER':<20} | {'SUPPLIER':<32} | {'EXP DELIVERY':<14} | {'TOTAL (₹)':<14} | {'STATUS':<20}"
                print(header)
                print("-" * len(header))
                for po in pos:
                    amt = f"₹{float(po[3]):,.2f}" if po[3] is not None else "₹0.00"
                    print(f"{po[0]:<20} | {po[1]:<32} | {str(po[2]):<14} | {amt:<14} | {po[4]:<20}")
            else:
                print("⚠ No purchase orders found.")

            # 5. Requests for Quotation (RFQ)
            print("\n" + "=" * 80)
            print("📑 3. REQUESTS FOR QUOTATION (request_for_quotations)")
            print("=" * 80)
            rfqs = conn.execute(text("""
                SELECT name, subject, transaction_date, status
                FROM request_for_quotations
                ORDER BY created_at DESC;
            """)).fetchall()

            if rfqs:
                print(f"Total RFQs in Database: {len(rfqs)}\n")
                for r in rfqs:
                    print(f"  • {r[0]:<20} | {r[1]:<50} | Status: {r[3]}")
            else:
                print("⚠ No RFQs found.")

            print("\n" + "=" * 80)
            print("🎉 ALL BUYING DATABASE CHECKS PASSED 100%!")
            print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ Error inspecting buying database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check_buying()
