export const OTHER_MODULES = {
  Selling: {
    name: 'Selling',
    label: 'Selling & Sales Orders',
    icon: 'ShoppingCart',
    description: 'Manage customers, quotations, sales orders, delivery tracking, and sales analytics.',
    kpis: [
      { label: 'Active Quotations', value: '143', change: '+12% this month' },
      { label: 'Pending Sales Orders', value: '48', change: '₹68.4L in pipeline' },
      { label: 'Total Customers', value: '1,240', change: '+34 new' },
      { label: 'Monthly Sales Run-Rate', value: '₹1.42 Cr', change: '+18.2% vs last month' }
    ],
    doctypes: [
      { name: 'customer', label: 'Customer', type: 'Master', desc: 'Customer profiles, credit limits, and billing terms' },
      { name: 'quotation', label: 'Quotation', type: 'Transaction', desc: 'Formal price quote sent to prospective buyers' },
      { name: 'sales_order', label: 'Sales Order', type: 'Transaction', desc: 'Confirmed customer purchase order awaiting fulfillment' },
      { name: 'sales_partner', label: 'Sales Partner', type: 'Master', desc: 'Channel partners, distributors, and commission tiers' },
      { name: 'sales_team', label: 'Sales Team', type: 'Master', desc: 'Sales executives and territory quota assignments' },
      { name: 'pricing_rule', label: 'Pricing Rule', type: 'Setting', desc: 'Discounts, tiered pricing, and campaign promotions' }
    ],
    workflow: [
      { step: '1. Lead / Prospect', desc: 'Identify opportunity in CRM or direct inbound' },
      { step: '2. Quotation', desc: 'Prepare line items, margins, and payment conditions' },
      { step: '3. Sales Order', desc: 'Book confirmed order against customer PO' },
      { step: '4. Delivery & Invoicing', desc: 'Handover to Stock for delivery & Accounting for Sales Invoice' }
    ]
  },
  Buying: {
    name: 'Buying',
    label: 'Buying & Procurement',
    icon: 'ShoppingBag',
    description: 'Procure raw materials, manage vendor contracts, purchase orders, and supplier bills.',
    kpis: [
      { label: 'Active Suppliers', value: '68', change: '5 preferred partners' },
      { label: 'Open Purchase Orders', value: '96', change: '₹34.2L committed' },
      { label: 'Pending Receipts', value: '18', change: 'Awaiting warehouse check' },
      { label: 'Procurement Savings', value: '8.4%', change: 'Negotiated rate delta' }
    ],
    doctypes: [
      { name: 'supplier', label: 'Supplier', type: 'Master', desc: 'Approved vendor directory, credit days, and tax registrations' },
      { name: 'purchase_order', label: 'Purchase Order', type: 'Transaction', desc: 'Legally binding order issued to material suppliers' },
      { name: 'purchase_receipt', label: 'Purchase Receipt', type: 'Transaction', desc: 'GRN inspection and stock intake acknowledgment' },
      { name: 'supplier_quotation', label: 'Supplier Quotation', type: 'Transaction', desc: 'Bids received from competing vendors' },
      { name: 'purchase_taxes_and_charges_template', label: 'Purchase Tax Template', type: 'Setting', desc: 'Inbound GST and freight charge structures' }
    ],
    workflow: [
      { step: '1. Material Request', desc: 'Triggered from manufacturing or minimum stock reorder' },
      { step: '2. Request for Quote', desc: 'Collect bids from certified suppliers' },
      { step: '3. Purchase Order', desc: 'Issue formal PO with delivery deadlines' },
      { step: '4. Receipt & Bill', desc: 'Inspect in Stock and match against Purchase Invoice' }
    ]
  },
  Stock: {
    name: 'Stock',
    label: 'Stock & Inventory Management',
    icon: 'Package',
    description: 'Track multi-warehouse inventory, item serial numbers, batches, valuations, and stock movements.',
    kpis: [
      { label: 'Tracked Items', value: '342', change: 'Across 12 categories' },
      { label: 'Total Stock Valuation', value: '₹2.18 Cr', change: 'FIFO valuation' },
      { label: 'Active Warehouses', value: '6', change: 'Central, Transit, 4 Regional' },
      { label: 'Low Stock Alerts', value: '7', change: 'Needs purchase replenishment' }
    ],
    doctypes: [
      { name: 'item', label: 'Item Master', type: 'Master', desc: 'Raw materials, finished goods, services, and consumables' },
      { name: 'warehouse', label: 'Warehouse', type: 'Master', desc: 'Storage locations, transit hubs, and retail outlets' },
      { name: 'stock_entry', label: 'Stock Entry', type: 'Transaction', desc: 'Material receipt, issue, transfer, and manufacturing scrap' },
      { name: 'delivery_note', label: 'Delivery Note', type: 'Transaction', desc: 'Outbound shipment dispatch document to customer' },
      { name: 'stock_reconciliation', label: 'Stock Reconciliation', type: 'Tool', desc: 'Physical audit count adjustment against system ledger' }
    ],
    workflow: [
      { step: '1. Item Master Setup', desc: 'Define SKU, barcode, unit of measure, and valuation method' },
      { step: '2. Inbound Intake', desc: 'Receive goods via Purchase Receipt or Stock Entry' },
      { step: '3. Internal Transfer', desc: 'Shift inventory between regional or transit warehouses' },
      { step: '4. Outbound Fulfillment', desc: 'Pick, pack, and issue Delivery Note for customer dispatch' }
    ]
  },
  Manufacturing: {
    name: 'Manufacturing',
    label: 'Manufacturing & Production',
    icon: 'Factory',
    description: 'Plan multi-level Bill of Materials (BOM), track work orders, production routing, and scrap.',
    kpis: [
      { label: 'Configured BOMs', value: '34', change: 'Multi-level assembly trees' },
      { label: 'Active Work Orders', value: '56', change: '14 currently on shop floor' },
      { label: 'Production Efficiency', value: '94.2%', change: '+2.1% this quarter' },
      { label: 'Scrap Rate', value: '1.2%', change: 'Well within 2% target' }
    ],
    doctypes: [
      { name: 'bom', label: 'Bill of Materials (BOM)', type: 'Master', desc: 'Product assembly recipes with component quantities and costs' },
      { name: 'work_order', label: 'Work Order', type: 'Transaction', desc: 'Shop-floor manufacturing batch authorization' },
      { name: 'production_plan', label: 'Production Plan', type: 'Transaction', desc: 'Demand-driven scheduling based on open sales orders' },
      { name: 'operation', label: 'Workstation & Operation', type: 'Master', desc: 'Machine centers, labor hourly costs, and capacities' }
    ],
    workflow: [
      { step: '1. BOM Engineering', desc: 'Define raw components, assembly steps, and labor costs' },
      { step: '2. Production Planning', desc: 'Schedule batches based on inventory demand' },
      { step: '3. Work Order Execution', desc: 'Transfer materials to WIP warehouse and track hours' },
      { step: '4. Finished Goods Entry', desc: 'Record completed output and transfer to main warehouse' }
    ]
  },
  CRM: {
    name: 'CRM',
    label: 'CRM & Customer Relationships',
    icon: 'Users',
    description: 'Track sales leads, opportunities, customer interactions, email logs, and conversion funnels.',
    kpis: [
      { label: 'Active Leads', value: '284', change: '+42 this week' },
      { label: 'Open Opportunities', value: '78', change: '₹1.85 Cr estimated value' },
      { label: 'Lead Conversion Rate', value: '26.8%', change: '+3.4% QoQ' },
      { label: 'Avg Sales Cycle', value: '18 Days', change: 'From inquiry to close' }
    ],
    doctypes: [
      { name: 'lead', label: 'Lead', type: 'Master', desc: 'Incoming prospective customer inquiries and source attribution' },
      { name: 'opportunity', label: 'Opportunity', type: 'Transaction', desc: 'Qualified deal stage with expected closing date and value' },
      { name: 'contact', label: 'Contact', type: 'Master', desc: 'Individual business contacts linked to customers & leads' },
      { name: 'customer_group', label: 'Customer Group', type: 'Setting', desc: 'Segmentation tiers: Enterprise, SME, Retail' }
    ],
    workflow: [
      { step: '1. Lead Capture', desc: 'Import from website, email, phone, or marketing campaign' },
      { step: '2. Qualification', desc: 'Assess budget, timeline, and customer requirements' },
      { step: '3. Opportunity Stage', desc: 'Demo, quotation preparation, and contract negotiations' },
      { step: '4. Account Conversion', desc: 'Convert winning deal into active Customer and Sales Order' }
    ]
  },
  Settings: {
    name: 'Settings',
    label: 'System & Company Settings',
    icon: 'Settings',
    description: 'Configure corporate entities, fiscal periods, user roles, security policies, and integrations.',
    kpis: [
      { label: 'System Health', value: '100% OK', change: 'All services connected' },
      { label: 'Active Companies', value: '2', change: 'Multi-entity consolidation' },
      { label: 'User Roles', value: '14', change: 'Role-based access active' },
      { label: 'Audit Records', value: '18,420', change: 'Full immutable trail' }
    ],
    doctypes: [
      { name: 'company', label: 'Company Master', type: 'Master', desc: 'Legal entity details, base currency, and fiscal year linkage' },
      { name: 'fiscal_year', label: 'Fiscal Year', type: 'Setting', desc: 'Statutory accounting year periods and lock dates' },
      { name: 'role_permission', label: 'Role & Permissions', type: 'Setting', desc: 'Granular read, write, submit, and delete rights per doctype' },
      { name: 'system_settings', label: 'System Settings', type: 'Setting', desc: 'Global date formats, currency symbols, and session timeouts' }
    ],
    workflow: [
      { step: '1. Organization Setup', desc: 'Set company legal names, tax IDs, and reporting currency' },
      { step: '2. Financial Calendar', desc: 'Define fiscal years and period lock controls' },
      { step: '3. Access Governance', desc: 'Assign role-based permissions across 191 accounting domains' },
      { step: '4. Provider Integrations', desc: 'Link banking APIs, GST portal, and CreditBridge intelligence' }
    ]
  }
};
