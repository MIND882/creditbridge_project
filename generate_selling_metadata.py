import glob
import os
import ast
import json
import re

SELLING_MODELS_DIR = '/home/user/backend/app/selling'
OUTPUT_PATH = '/home/user/frontend/src/data/sellingMetadata.json'

CATEGORY_MAP = {
    'quotation': 'Sales Orders & Quotations',
    'quotation_item': 'Sales Orders & Quotations',
    'sales_order': 'Sales Orders & Quotations',
    'sales_order_item': 'Sales Orders & Quotations',
    'proforma_invoice': 'Sales Orders & Quotations',
    'proforma_invoice_item': 'Sales Orders & Quotations',

    'customer': 'Customer & Partner Management',
    'customer_credit_limit': 'Customer & Partner Management',
    'sales_team': 'Customer & Partner Management',
    'sales_partner_type': 'Customer & Partner Management',
    'industry_type': 'Customer & Partner Management',
    'supplier_number_at_customer': 'Customer & Partner Management',

    'product_bundle': 'Products & Bundles',
    'product_bundle_item': 'Products & Bundles',
    'party_specific_item': 'Products & Bundles',

    'installation_note': 'Delivery & Installation',
    'installation_note_item': 'Delivery & Installation',
    'delivery_schedule_item': 'Delivery & Installation',

    'selling_settings': 'Settings & Communication',
    'sms_center': 'Settings & Communication'
}

TYPE_MAP = {
    'quotation': 'transaction',
    'sales_order': 'transaction',
    'proforma_invoice': 'transaction',
    'installation_note': 'transaction',
    'customer': 'master',
    'product_bundle': 'master',
    'party_specific_item': 'master',
    'sales_team': 'master',
    'sales_partner_type': 'setup',
    'industry_type': 'setup',
    'selling_settings': 'setup',
    'sms_center': 'setup',
    'customer_credit_limit': 'setup',
    'supplier_number_at_customer': 'setup'
}

def to_label(s):
    if s.lower() == 'name': return 'Record ID'
    if s.lower() == 'id': return 'ID'
    if s.lower() == 'docstatus': return 'Document Status'
    if s.lower() == 'gstin': return 'GSTIN'
    if s.lower() == 'pan': return 'PAN'
    if s.lower() == 'uom': return 'UOM'
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
        return 'select', ['Draft', 'To Deliver and Bill', 'To Bill', 'To Deliver', 'Completed', 'Cancelled', 'Closed']

    return 'text', None

def categorize_field(f_name):
    f_l = f_name.lower()
    if f_l in ['name', 'title', 'naming_series', 'transaction_date', 'delivery_date', 'valid_till', 'order_type', 'status', 'company', 'docstatus']:
        return 'Primary & Identification'
    if any(k in f_l for k in ['customer', 'party', 'contact', 'address', 'email', 'phone', 'mobile', 'tax_id', 'gstin', 'shipping', 'dispatch']):
        return 'Customer, Contact & Address'
    if any(k in f_l for k in ['amount', 'total', 'rate', 'tax', 'charge', 'discount', 'currency', 'price_list', 'cost_center', 'project', 'account', 'dimension']):
        return 'Pricing, Currency & Financial Values'
    if any(k in f_l for k in ['terms', 'tc_name', 'remarks', 'notes', 'reference', 'po_no', 'po_date', 'instruction']):
        return 'Terms, Notes & PO References'
    return 'Operational & Configuration Flags'

def generate():
    models = glob.glob(f'{SELLING_MODELS_DIR}/**/models/*.py', recursive=True)
    models = sorted([m for m in models if not m.endswith('__init__.py')])

    selling_domains = []
    total_fields_extracted = 0

    for idx, model_path in enumerate(models, 1):
        domain_folder = model_path.split('/')[-3]
        raw_name = domain_folder.replace('_domain', '')

        with open(model_path, 'r') as f:
            src = f.read()

        try:
            tree = ast.parse(src)
        except Exception as e:
            print(f"Error parsing {model_path}: {e}")
            continue

        enums = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                is_enum = any('Enum' in ast.unparse(b) for b in node.bases)
                if is_enum:
                    vals = []
                    for item in node.body:
                        if isinstance(item, ast.Assign) and item.targets and isinstance(item.targets[0], ast.Name):
                            vals.append(item.targets[0].id)
                    enums[node.name] = vals

        fields = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        val_str = ast.unparse(item.value) if item.value else ''
                        ann_str = ast.unparse(item.annotation)
                        col_name = item.target.id
                        if 'mapped_column' in val_str:
                            f_type, f_extra = infer_type_and_options(col_name, ann_str, val_str, enums)
                            is_req = ('nullable=False' in val_str) and ('default=' not in val_str) and (col_name != 'name')

                            # Determine in_list_view (first 4-5 meaningful fields)
                            in_list = col_name in ['name', 'customer_name', 'customer', 'status', 'grand_total', 'transaction_date', 'delivery_date', 'item_code', 'item_name', 'qty', 'rate', 'amount']

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

        # Make sure at least name is in_list_view
        if not any(f['in_list_view'] for f in fields):
            for f in fields[:4]:
                f['in_list_view'] = True

        # Group into sections
        section_dict = {
            'Primary & Identification': [],
            'Customer, Contact & Address': [],
            'Pricing, Currency & Financial Values': [],
            'Terms, Notes & PO References': [],
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
        api_prefix = f'/api/selling/{slug}'

        domain_meta = {
            'index': idx,
            'name': raw_name,
            'label': label,
            'module': 'Selling',
            'type': TYPE_MAP.get(raw_name, 'child_table' if 'item' in raw_name else 'master'),
            'category': CATEGORY_MAP.get(raw_name, 'Sales & Customers'),
            'description': f"Manage {label} per ERPNext cloud sales standard.",
            'count': 0,
            'fields': fields,
            'sections': sections,
            'sampleRecords': [],
            'backend': {
                'api_prefix': api_prefix,
                'table': f"{raw_name}s",
                'model_path': model_path.replace('/home/user/', '')
            }
        }
        selling_domains.append(domain_meta)

    # Seed realistic MSME sample records for primary Selling domains
    # 1. Customers
    cust_domain = next((d for d in selling_domains if d['name'] == 'customer'), None)
    if cust_domain:
        cust_domain['sampleRecords'] = [
            {
                'id': 'CUST-2026-0001',
                'name': 'CUST-2026-0001',
                'customer_name': 'Acme Technologies Pvt Ltd',
                'customer_type': 'Company',
                'customer_group': 'Commercial',
                'territory': 'India West - Mumbai',
                'tax_id': '27AABCA1234F1Z5',
                'status': 'Active'
            },
            {
                'id': 'CUST-2026-0002',
                'name': 'CUST-2026-0002',
                'customer_name': 'Bharat Retailers Ltd',
                'customer_type': 'Company',
                'customer_group': 'Retail Chains',
                'territory': 'India North - Delhi NCR',
                'tax_id': '07AABCB5678G1Z2',
                'status': 'Active'
            },
            {
                'id': 'CUST-2026-0003',
                'name': 'CUST-2026-0003',
                'customer_name': 'Zenith Logistics Corp',
                'customer_type': 'Company',
                'customer_group': 'Commercial',
                'territory': 'India West - Pune',
                'tax_id': '27AABCZ9988H1Z1',
                'status': 'Active'
            }
        ]
        cust_domain['count'] = len(cust_domain['sampleRecords'])

    # 2. Sales Orders
    so_domain = next((d for d in selling_domains if d['name'] == 'sales_order'), None)
    if so_domain:
        so_domain['sampleRecords'] = [
            {
                'id': 'SO-2026-0001',
                'name': 'SO-2026-0001',
                'customer': 'Acme Technologies Pvt Ltd',
                'customer_name': 'Acme Technologies Pvt Ltd',
                'transaction_date': '2026-10-05',
                'delivery_date': '2026-10-25',
                'net_total': 275000.0,
                'total_taxes_and_charges': 49500.0,
                'grand_total': 324500.0,
                'status': 'To Deliver and Bill'
            },
            {
                'id': 'SO-2026-0002',
                'name': 'SO-2026-0002',
                'customer': 'Bharat Retailers Ltd',
                'customer_name': 'Bharat Retailers Ltd',
                'transaction_date': '2026-10-06',
                'delivery_date': '2026-11-01',
                'net_total': 180000.0,
                'total_taxes_and_charges': 32400.0,
                'grand_total': 212400.0,
                'status': 'To Deliver and Bill'
            }
        ]
        so_domain['count'] = len(so_domain['sampleRecords'])

    # 3. Quotations
    q_domain = next((d for d in selling_domains if d['name'] == 'quotation'), None)
    if q_domain:
        q_domain['sampleRecords'] = [
            {
                'id': 'QTN-2026-0001',
                'name': 'QTN-2026-0001',
                'party_name': 'Acme Technologies Pvt Ltd',
                'customer_name': 'Acme Technologies Pvt Ltd',
                'transaction_date': '2026-10-01',
                'valid_till': '2026-10-31',
                'net_total': 350000.0,
                'grand_total': 413000.0,
                'status': 'Open'
            },
            {
                'id': 'QTN-2026-0002',
                'name': 'QTN-2026-0002',
                'party_name': 'Reliance Infotech Solutions',
                'customer_name': 'Reliance Infotech Solutions',
                'transaction_date': '2026-10-04',
                'valid_till': '2026-11-15',
                'net_total': 520000.0,
                'grand_total': 613600.0,
                'status': 'Open'
            }
        ]
        q_domain['count'] = len(q_domain['sampleRecords'])

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(selling_domains, f, indent=2)

    print(f"SUCCESS: Generated Selling Metadata for {len(selling_domains)} domains.")
    print(f"Total columns extracted across all 20 Selling domains: {total_fields_extracted}.")

if __name__ == '__main__':
    generate()
