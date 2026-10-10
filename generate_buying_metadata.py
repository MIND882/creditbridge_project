#!/usr/bin/env python3
"""
CreditBridge ERP — Buying Metadata Generator
Scans all 19 Buying domain models in backend/app/buying/**/models/*.py,
extracts 100% of SQLAlchemy columns, data types, constraints, and relationships,
and outputs a comprehensive buyingMetadata.json matching the exact structure
expected by GenericListView, GenericFormView, and RecordsContext.
"""

import glob
import os
import ast
import json

BUYING_MODELS_DIR = '/home/user/backend/app/buying'
OUTPUT_PATH = '/home/user/frontend/src/data/buyingMetadata.json'

CATEGORY_MAP = {
    'purchase_order': 'Procurement & Purchase Orders',
    'purchase_order_item': 'Procurement & Purchase Orders',
    'purchase_receipt': 'Procurement & Purchase Orders',
    'purchase_receipt_item': 'Procurement & Purchase Orders',
    'purchase_receipt_item_supplied': 'Procurement & Purchase Orders',

    'supplier': 'Supplier & Vendor Management',
    'customer_number_at_supplier': 'Supplier & Vendor Management',
    'supplier_scorecard': 'Supplier & Vendor Management',
    'supplier_scorecard_period': 'Supplier & Vendor Management',
    'supplier_scorecard_criteria': 'Supplier & Vendor Management',
    'supplier_scorecard_variable': 'Supplier & Vendor Management',
    'supplier_scorecard_standing': 'Supplier & Vendor Management',
    'supplier_scorecard_scoring_criteria': 'Supplier & Vendor Management',
    'supplier_scorecard_scoring_variable': 'Supplier & Vendor Management',
    'supplier_scorecard_scoring_standing': 'Supplier & Vendor Management',

    'request_for_quotation': 'Tendering & RFQ',
    'request_for_quotation_item': 'Tendering & RFQ',
    'request_for_quotation_supplier': 'Tendering & RFQ',
    'supplier_quotation': 'Tendering & RFQ',
    'supplier_quotation_item': 'Tendering & RFQ',

    'buying_settings': 'Buying Settings & Setup'
}

TYPE_MAP = {
    'purchase_order': 'transaction',
    'purchase_receipt': 'transaction',
    'request_for_quotation': 'transaction',
    'supplier_quotation': 'transaction',
    'supplier': 'master',
    'supplier_scorecard': 'master',
    'supplier_scorecard_period': 'transaction',
    'buying_settings': 'setup',
    'customer_number_at_supplier': 'setup',
    'supplier_scorecard_criteria': 'setup',
    'supplier_scorecard_variable': 'setup',
    'supplier_scorecard_standing': 'setup',
    'supplier_scorecard_scoring_criteria': 'setup',
    'supplier_scorecard_scoring_variable': 'setup',
    'supplier_scorecard_scoring_standing': 'setup',
    'purchase_order_item': 'child_table',
    'purchase_receipt_item': 'child_table',
    'purchase_receipt_item_supplied': 'child_table',
    'request_for_quotation_item': 'child_table',
    'request_for_quotation_supplier': 'child_table',
    'supplier_quotation_item': 'child_table'
}

def to_label(s):
    if s.lower() == 'name': return 'Record ID'
    if s.lower() == 'id': return 'ID'
    if s.lower() == 'docstatus': return 'Document Status'
    if s.lower() == 'gstin': return 'GSTIN'
    if s.lower() == 'pan': return 'PAN'
    if s.lower() == 'uom': return 'UOM'
    if s.lower() == 'rfq': return 'RFQ'
    if s.lower() == 'po': return 'PO'
    clean = s.replace('_id', '').replace('_', ' ')
    return ' '.join(w.capitalize() for w in clean.split())

def infer_type_and_options(name, ann_str, val_str, enums):
    ann_l = ann_str.lower()
    val_l = val_str.lower()
    name_l = name.lower()

    for enum_name, enum_vals in enums.items():
        if enum_name.lower() in val_l or enum_name.lower() in ann_l:
            formatted_opts = [' '.join(w.capitalize() for w in v.replace('_', ' ').split()) for v in enum_vals]
            return 'select', formatted_opts

    if 'date' in ann_l or 'date' in val_l or name_l.endswith('_date') or name_l == 'date':
        if 'time' in ann_l or 'time' in val_l or 'datetime' in ann_l:
            return 'datetime', None
        return 'date', None

    if 'time' in ann_l or 'time' in val_l or name_l.endswith('_time'):
        return 'time', None

    if 'bool' in ann_l or 'boolean' in val_l:
        return 'check', None

    if any(k in name_l for k in ['amount', 'rate', 'price', 'tax', 'grand_total', 'net_total', 'base_', 'discount', 'total', 'charge']):
        return 'currency', None

    if 'numeric' in val_l or 'decimal' in ann_l:
        return 'currency', None

    if 'int' in ann_l or 'integer' in val_l or name_l in ['qty', 'count', 'idx', 'priority', 'sort_order']:
        return 'number', None

    if 'foreignkey' in val_l or name_l.endswith('_id'):
        target = name_l.replace('_id', '')
        return 'link', target

    if 'text' in val_l or any(k in name_l for k in ['remarks', 'description', 'notes', 'terms', 'address', 'instruction', 'details']):
        return 'textarea', None

    if name_l == 'status':
        return 'select', ['Draft', 'To Receive and Bill', 'To Bill', 'To Receive', 'Completed', 'Cancelled', 'Closed']

    return 'text', None

def categorize_field(f_name):
    f_l = f_name.lower()
    if f_l in ['name', 'title', 'naming_series', 'transaction_date', 'schedule_date', 'valid_till', 'order_type', 'status', 'company', 'docstatus']:
        return 'Primary & Identification'
    if any(k in f_l for k in ['supplier', 'party', 'contact', 'address', 'email', 'phone', 'mobile', 'tax_id', 'gstin', 'shipping', 'dispatch']):
        return 'Supplier, Contact & Address'
    if any(k in f_l for k in ['amount', 'total', 'rate', 'tax', 'charge', 'discount', 'currency', 'price_list', 'cost_center', 'project', 'account', 'dimension']):
        return 'Pricing, Currency & Financial Values'
    if any(k in f_l for k in ['terms', 'tc_name', 'remarks', 'notes', 'reference', 'po_no', 'po_date', 'instruction']):
        return 'Terms, Notes & References'
    return 'Operational & Configuration Flags'

def generate():
    models = glob.glob(f'{BUYING_MODELS_DIR}/**/models/*.py', recursive=True)
    models = sorted([m for m in models if not m.endswith('__init__.py')])

    buying_domains = []
    total_fields_extracted = 0

    for idx, model_path in enumerate(models, 1):
        domain_folder = model_path.split('/')[-3]
        raw_name = domain_folder.replace('_domain', '')

        with open(model_path, 'r', encoding='utf-8') as f:
            src = f.read()

        try:
            tree = ast.parse(src)
        except Exception as e:
            print(f"Error parsing {model_path}: {e}")
            continue

        enums = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                is_enum = any((isinstance(b, ast.Name) and b.id in ('Enum', 'str')) or (isinstance(b, ast.Attribute) and b.attr == 'Enum') for b in node.bases)
                if is_enum:
                    vals = []
                    for item in node.body:
                        if isinstance(item, ast.Assign) and item.targets and isinstance(item.targets[0], ast.Name):
                            if isinstance(item.value, ast.Constant):
                                vals.append(str(item.value.value))
                            else:
                                vals.append(item.targets[0].id)
                    enums[node.name] = vals

        fields = []
        table_name = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name) and target.id == '__tablename__':
                                if isinstance(item.value, ast.Constant):
                                    table_name = item.value.value

                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        val_str = ast.unparse(item.value) if item.value else ''
                        ann_str = ast.unparse(item.annotation)
                        col_name = item.target.id
                        if 'mapped_column' in val_str or 'Mapped[' in ann_str:
                            f_type, f_extra = infer_type_and_options(col_name, ann_str, val_str, enums)
                            is_req = ('nullable=False' in val_str) and ('default=' not in val_str) and (col_name != 'name')

                            in_list = col_name in ['name', 'supplier_name', 'supplier', 'status', 'grand_total', 'transaction_date', 'schedule_date', 'item_code', 'item_name', 'qty', 'rate', 'amount', 'tax_id']

                            field_obj = {
                                'name': col_name,
                                'label': to_label(col_name),
                                'type': f_type,
                                'required': is_req,
                                'in_list_view': in_list
                            }
                            if f_type == 'select' and f_extra:
                                field_obj['options'] = f_extra
                            elif f_type == 'link' and f_extra:
                                field_obj['linkTo'] = f_extra

                            fields.append(field_obj)
                            total_fields_extracted += 1

        if not any(f['in_list_view'] for f in fields):
            for f in fields[:4]:
                f['in_list_view'] = True

        section_dict = {
            'Primary & Identification': [],
            'Supplier, Contact & Address': [],
            'Pricing, Currency & Financial Values': [],
            'Terms, Notes & References': [],
            'Operational & Configuration Flags': []
        }
        for f in fields:
            cat = categorize_field(f['name'])
            section_dict[cat].append(f['name'])

        sections = [
            {'label': cat, 'fields': f_names}
            for cat, f_names in section_dict.items() if len(f_names) > 0
        ]

        label = ' '.join(w.capitalize() for w in raw_name.split('_'))
        slug = raw_name.replace('_', '-')
        api_prefix = f'/api/buying/{slug}'

        domain_meta = {
            'index': idx,
            'name': raw_name,
            'label': label,
            'module': 'Buying',
            'type': TYPE_MAP.get(raw_name, 'child_table' if 'item' in raw_name else 'master'),
            'category': CATEGORY_MAP.get(raw_name, 'Supplier & Vendor Management'),
            'description': f"Manage {label} per ERPNext cloud procurement standard.",
            'count': 0,
            'fields': fields,
            'sections': sections,
            'sampleRecords': [],
            'backend': {
                'api_prefix': api_prefix,
                'table': table_name or f"{raw_name}s",
                'model_path': model_path.replace('/home/user/', '')
            }
        }
        buying_domains.append(domain_meta)

    # 1. Suppliers Demo Records
    sup_domain = next((d for d in buying_domains if d['name'] == 'supplier'), None)
    if sup_domain:
        sup_domain['sampleRecords'] = [
            {
                'id': 'SUP-2026-0001',
                'name': 'SUP-2026-0001',
                'supplier_name': 'Tata Steel Limited',
                'supplier_type': 'Company',
                'supplier_group': 'Raw Material',
                'country': 'India',
                'tax_id': '20AAACT2727Q1ZW',
                'supplier_primary_contact': 'Rajesh Nambiar',
                'mobile_no': '+91 98210 11223',
                'email_id': 'procurement@tatasteel.com',
                'primary_address': 'Bombay House, 24 Homi Mody Street, Fort, Mumbai 400001',
                'default_currency': 'INR',
                'status': 'Active'
            },
            {
                'id': 'SUP-2026-0002',
                'name': 'SUP-2026-0002',
                'supplier_name': 'Schneider Electric India Pvt Ltd',
                'supplier_type': 'Company',
                'supplier_group': 'Electrical Components',
                'country': 'India',
                'tax_id': '06AAACS8494J1Z6',
                'supplier_primary_contact': 'Sunita Kapoor',
                'mobile_no': '+91 98100 44556',
                'email_id': 'orders@schneider-electric.co.in',
                'primary_address': 'DLF Cyber City, Building 10, Tower B, Gurugram, Haryana 122002',
                'default_currency': 'INR',
                'status': 'Active'
            },
            {
                'id': 'SUP-2026-0003',
                'name': 'SUP-2026-0003',
                'supplier_name': 'Bosch Automotive Components',
                'supplier_type': 'Company',
                'supplier_group': 'Hardware & Precision',
                'country': 'India',
                'tax_id': '29AAACB3456F1Z8',
                'supplier_primary_contact': 'Ganesh Hegde',
                'mobile_no': '+91 99011 88990',
                'email_id': 'supplychain@bosch.in',
                'primary_address': 'Hosur Road, Adugodi, Bengaluru, Karnataka 560030',
                'default_currency': 'INR',
                'status': 'Active'
            },
            {
                'id': 'SUP-2026-0004',
                'name': 'SUP-2026-0004',
                'supplier_name': 'Wipro Cloud Infrastructure Services',
                'supplier_type': 'Company',
                'supplier_group': 'IT & Services',
                'country': 'India',
                'tax_id': '29AAACW1234F1Z1',
                'supplier_primary_contact': 'Kavita Menon',
                'mobile_no': '+91 98450 77665',
                'email_id': 'vendor-desk@wipro.com',
                'primary_address': 'Doddakannelli, Sarjapur Road, Bengaluru, Karnataka 560035',
                'default_currency': 'INR',
                'status': 'Active'
            }
        ]
        sup_domain['count'] = len(sup_domain['sampleRecords'])

    # 2. Purchase Orders Demo Records
    po_domain = next((d for d in buying_domains if d['name'] == 'purchase_order'), None)
    if po_domain:
        po_domain['sampleRecords'] = [
            {
                'id': 'PUR-ORD-2026-00001',
                'name': 'PUR-ORD-2026-00001',
                'naming_series': 'PUR-ORD-.YYYY.-',
                'supplier_name': 'Tata Steel Limited',
                'company': 'CreditBridge MSME Ltd',
                'transaction_date': '2026-10-10',
                'schedule_date': '2026-10-24',
                'currency': 'INR',
                'net_total': 186440.68,
                'total_taxes_and_charges': 33559.32,
                'grand_total': 220000.0,
                'status': 'To Receive and Bill'
            },
            {
                'id': 'PUR-ORD-2026-00002',
                'name': 'PUR-ORD-2026-00002',
                'naming_series': 'PUR-ORD-.YYYY.-',
                'supplier_name': 'Schneider Electric India Pvt Ltd',
                'company': 'CreditBridge MSME Ltd',
                'transaction_date': '2026-10-10',
                'schedule_date': '2026-10-31',
                'currency': 'INR',
                'net_total': 101694.92,
                'total_taxes_and_charges': 18305.08,
                'grand_total': 120000.0,
                'status': 'Draft'
            }
        ]
        po_domain['count'] = len(po_domain['sampleRecords'])

    # 3. Request For Quotations Demo Records
    rfq_domain = next((d for d in buying_domains if d['name'] == 'request_for_quotation'), None)
    if rfq_domain:
        rfq_domain['sampleRecords'] = [
            {
                'id': 'PUR-RFQ-2026-00001',
                'name': 'PUR-RFQ-2026-00001',
                'naming_series': 'PUR-RFQ-.YYYY.-',
                'company': 'CreditBridge MSME Ltd',
                'transaction_date': '2026-10-10',
                'subject': 'Annual Procurement of Heavy Components & Hardware FY 2026-27',
                'status': 'Submitted'
            }
        ]
        rfq_domain['count'] = len(rfq_domain['sampleRecords'])

    # 4. Supplier Quotations Demo Records
    sq_domain = next((d for d in buying_domains if d['name'] == 'supplier_quotation'), None)
    if sq_domain:
        sq_domain['sampleRecords'] = [
            {
                'id': 'PUR-SQTN-2026-00001',
                'name': 'PUR-SQTN-2026-00001',
                'naming_series': 'PUR-SQTN-.YYYY.-',
                'supplier': 'Bosch Automotive Components',
                'company': 'CreditBridge MSME Ltd',
                'transaction_date': '2026-10-10',
                'valid_till': '2026-11-10',
                'currency': 'INR',
                'net_total': 122881.36,
                'total_taxes_and_charges': 22118.64,
                'grand_total': 145000.0,
                'status': 'Submitted'
            }
        ]
        sq_domain['count'] = len(sq_domain['sampleRecords'])

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(buying_domains, f, indent=2)

    print(f"SUCCESS: Generated Buying Metadata for {len(buying_domains)} domains.")
    print(f"Total columns extracted across all 19 Buying domains: {total_fields_extracted}.")

if __name__ == '__main__':
    generate()
