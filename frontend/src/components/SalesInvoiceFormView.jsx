import React, { useState, useMemo, useEffect } from 'react';
import {
  ArrowLeft,
  Save,
  X,
  Plus,
  Trash2,
  Calculator,
  User,
  Building2,
  Calendar,
  Clock,
  MapPin,
  Phone,
  Mail,
  Truck,
  FileText,
  CreditCard,
  Percent,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Sparkles,
  Layers,
  ChevronDown
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function SalesInvoiceFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('sales_invoice', recordId) : null;
  const isEditing = !!existingRecord;

  // Auto-fetch cost centers, accounts, and customers for dropdown links
  useEffect(() => {
    fetchDomainRecords('account');
    fetchDomainRecords('cost_center');
    fetchDomainRecords('mode_of_payment');
  }, []);

  const costCenters = getDomainRecords('cost_center');
  const accounts = getDomainRecords('account');

  // Customer suggestions
  const customerList = [
    { name: 'Acme Technologies Pvt Ltd', contact: 'Anil Mehta', phone: '+91 98200 12345', email: 'anil@acme.in', address: 'Plot 44, MIDC Industrial Area, Andheri East, Mumbai 400093' },
    { name: 'Bharat Retailers Ltd', contact: 'Pooja Sharma', phone: '+91 98111 23456', email: 'pooja@bharatretail.in', address: 'Shop 12, Phoenix Marketcity, Kurla West, Mumbai 400070' },
    { name: 'Zenith Logistics Corp', contact: 'Karan Malhotra', phone: '+91 98333 34567', email: 'karan@zenithlogistics.com', address: 'Warehouse 8, Nhava Sheva Port Road, Navi Mumbai 410206' },
    { name: 'Reliance Infotech Solutions', contact: 'Vikram Sethi', phone: '+91 98444 45678', email: 'vikram@relianceinfotech.in', address: 'Tower 4, Mindspace Tech Park, Malad West, Mumbai 400064' },
    { name: 'Tata Steel Processing Ltd', contact: 'Rajesh Nair', phone: '+91 98555 56789', email: 'rajesh@tatasteel.com', address: 'Industrial Estate, Jamshedpur 831001' }
  ];

  // Primary State
  const [customer, setCustomer] = useState(existingRecord?.customer || 'Acme Technologies Pvt Ltd');
  const [customerName, setCustomerName] = useState(existingRecord?.customer_name || 'Acme Technologies Pvt Ltd');
  const [namingSeries, setNamingSeries] = useState(existingRecord?.naming_series || 'ACC-SINV-.YYYY.-');
  const [postingDate, setPostingDate] = useState(existingRecord?.posting_date || new Date().toISOString().slice(0, 10));
  const [dueDate, setDueDate] = useState(() => {
    if (existingRecord?.due_date) return existingRecord.due_date;
    const d = new Date();
    d.setDate(d.getDate() + 30);
    return d.toISOString().slice(0, 10);
  });
  const [postingTime, setPostingTime] = useState(existingRecord?.posting_time || '12:00:00');
  const [costCenter, setCostCenter] = useState(existingRecord?.cost_center || 'Main - CB');
  const [project, setProject] = useState(existingRecord?.project || 'MSME Credit Onboarding');

  // Address & Contact
  const [customerAddress, setCustomerAddress] = useState(existingRecord?.customer_address || 'Plot 44, MIDC Industrial Area, Andheri East, Mumbai 400093');
  const [contactPerson, setContactPerson] = useState(existingRecord?.contact_person || 'Anil Mehta');
  const [contactMobile, setContactMobile] = useState(existingRecord?.contact_mobile || '+91 98200 12345');
  const [contactEmail, setContactEmail] = useState(existingRecord?.contact_email || 'anil@acme.in');
  const [shippingAddress, setShippingAddress] = useState(existingRecord?.shipping_address || 'Plot 44, MIDC Industrial Area, Andheri East, Mumbai 400093');

  // Currency & Pricing
  const [currency, setCurrency] = useState(existingRecord?.currency || 'INR');
  const [conversionRate, setConversionRate] = useState(existingRecord?.conversion_rate || 1.0);
  const [priceList, setPriceList] = useState(existingRecord?.selling_price_list || 'Standard Selling');

  // Line Items Table (ERPNext style Child Table)
  const [items, setItems] = useState(() => {
    if (existingRecord?.items && Array.isArray(existingRecord.items) && existingRecord.items.length > 0) {
      return existingRecord.items;
    }
    return [
      {
        id: 1,
        item_code: 'CB-SERV-01',
        item_name: 'Financial Advisory & Credit Assessment',
        description: 'Comprehensive MSME Balance Sheet & Cashflow Underwriting Service',
        qty: 1,
        uom: 'Nos',
        rate: 85000,
        amount: 85000
      },
      {
        id: 2,
        item_code: 'CB-SERV-02',
        item_name: 'GST Reconciliation & Audit Verification',
        description: 'Automated 2A/2B vs GSTR-3B Tax Input Credit Verification Module',
        qty: 1,
        uom: 'Nos',
        rate: 42000,
        amount: 42000
      }
    ];
  });

  // Taxes and Charges (GST Structure)
  const [taxTemplate, setTaxTemplate] = useState('in_state_18');
  const [taxCategory, setTaxCategory] = useState('In-State GST (CGST + SGST)');

  // Payment Terms & Remarks
  const [paymentTermsTemplate, setPaymentTermsTemplate] = useState(existingRecord?.payment_terms_template || 'Standard Net 30');
  const [terms, setTerms] = useState(existingRecord?.terms || '1. Payment due within 30 days of invoice date.\n2. Interest @ 18% p.a. applicable on overdue balance after 30 days.');
  const [remarks, setRemarks] = useState(existingRecord?.remarks || 'Generated via CreditBridge ERP Generic Engine');
  const [paidAdvance, setPaidAdvance] = useState(Number(existingRecord?.paid_amount || 0));
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Synchronize customer select change
  const handleCustomerChange = (custName) => {
    setCustomer(custName);
    const found = customerList.find(c => c.name === custName);
    if (found) {
      setCustomerName(found.name);
      setContactPerson(found.contact);
      setContactMobile(found.phone);
      setContactEmail(found.email);
      setCustomerAddress(found.address);
      setShippingAddress(found.address);
    } else {
      setCustomerName(custName);
    }
  };

  // Line Item Management
  const handleItemChange = (idx, field, value) => {
    setItems(prev => {
      const next = [...prev];
      const updated = { ...next[idx], [field]: value };
      if (field === 'qty' || field === 'rate') {
        const q = field === 'qty' ? Number(value) || 0 : Number(updated.qty) || 0;
        const r = field === 'rate' ? Number(value) || 0 : Number(updated.rate) || 0;
        updated.amount = q * r;
      }
      next[idx] = updated;
      return next;
    });
  };

  const handleAddItem = () => {
    setItems(prev => [
      ...prev,
      {
        id: Date.now(),
        item_code: `CB-ITEM-0${prev.length + 1}`,
        item_name: 'Operational Enterprise Fulfillment',
        description: 'Standard product / service fulfillment line item',
        qty: 1,
        uom: 'Nos',
        rate: 20000,
        amount: 20000
      }
    ]);
  };

  const handleRemoveItem = (idx) => {
    if (items.length <= 1) {
      onShowToast?.('At least one line item is required', 'error');
      return;
    }
    setItems(prev => prev.filter((_, i) => i !== idx));
  };

  // Live Automatic Calculations
  const netTotal = useMemo(() => {
    return items.reduce((sum, it) => sum + (Number(it.amount) || 0), 0);
  }, [items]);

  const taxBreakdown = useMemo(() => {
    if (taxTemplate === 'in_state_18') {
      const cgst = netTotal * 0.09;
      const sgst = netTotal * 0.09;
      return {
        rows: [
          { account: 'Output CGST 9%', rate: '9.0%', amount: cgst },
          { account: 'Output SGST 9%', rate: '9.0%', amount: sgst }
        ],
        totalTax: cgst + sgst
      };
    } else if (taxTemplate === 'out_state_18') {
      const igst = netTotal * 0.18;
      return {
        rows: [
          { account: 'Output IGST 18%', rate: '18.0%', amount: igst }
        ],
        totalTax: igst
      };
    }
    return { rows: [], totalTax: 0 };
  }, [netTotal, taxTemplate]);

  const grandTotal = netTotal + taxBreakdown.totalTax;
  const roundedTotal = Math.round(grandTotal);
  const roundingAdjustment = roundedTotal - grandTotal;
  const outstandingAmount = Math.max(0, roundedTotal - paidAdvance);

  const calculatedStatus = useMemo(() => {
    if (paidAdvance >= roundedTotal && roundedTotal > 0) return 'Paid';
    if (paidAdvance > 0) return 'Partly Paid';
    return 'Unpaid';
  }, [paidAdvance, roundedTotal]);

  // Form Submission
  const handleSubmit = async (submitStatus = 'Submitted') => {
    if (!customer) {
      onShowToast?.('Customer is required', 'error');
      return;
    }
    if (items.length === 0 || netTotal <= 0) {
      onShowToast?.('At least one valid item amount is required', 'error');
      return;
    }

    setIsSubmitting(true);

    const docId = existingRecord?.id || existingRecord?.name || `ACC-SINV-2026-${String(Math.floor(100000 + Math.random() * 900000))}`;

    const invoicePayload = {
      id: docId,
      name: docId,
      naming_series: namingSeries,
      customer,
      customer_name: customerName,
      posting_date: postingDate,
      due_date: dueDate,
      posting_time: postingTime,
      cost_center: costCenter,
      project,
      customer_address: customerAddress,
      address_display: customerAddress,
      contact_person: contactPerson,
      contact_mobile: contactMobile,
      contact_email: contactEmail,
      shipping_address: shippingAddress,
      currency,
      conversion_rate: conversionRate,
      selling_price_list: priceList,
      price_list_currency: currency,
      plc_conversion_rate: 1.0,
      items,
      total_qty: items.reduce((s, it) => s + (Number(it.qty) || 0), 0),
      net_total: netTotal,
      base_net_total: netTotal,
      total: netTotal,
      taxes_and_charges: taxTemplate === 'in_state_18' ? 'In-State GST 18% (CGST 9% + SGST 9%)' : 'Out-of-State GST 18% (IGST 18%)',
      total_taxes_and_charges: taxBreakdown.totalTax,
      base_total_taxes_and_charges: taxBreakdown.totalTax,
      grand_total: grandTotal,
      base_grand_total: grandTotal,
      rounded_total: roundedTotal,
      rounding_adjustment: roundingAdjustment,
      paid_amount: paidAdvance,
      outstanding_amount: outstandingAmount,
      payment_terms_template: paymentTermsTemplate,
      terms,
      remarks,
      status: submitStatus,
      docstatus: submitStatus === 'Draft' ? 0 : 1,
      is_pos: false,
      is_return: false,
      update_stock: false
    };

    try {
      if (isEditing) {
        await updateRecord('sales_invoice', recordId, invoicePayload);
        onShowToast?.(`Sales Invoice ${docId} updated successfully`);
      } else {
        await addRecord('sales_invoice', invoicePayload);
        onShowToast?.(`Sales Invoice ${docId} created and posted to ledger!`);
      }
      onNavigate({ type: 'receivables' });
    } catch (err) {
      console.error(err);
      onShowToast?.('Failed to submit sales invoice: ' + err.message, 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Header Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col md:flex-row md:items-center justify-between gap-4 sticky top-16 z-20 backdrop-blur-md bg-white/95">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate({ type: 'receivables' })}
              className="p-1 -ml-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-mono font-semibold text-slate-400">
              ERPNext Cloud Sales Invoice
            </span>
            <span className="text-slate-300">•</span>
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              {calculatedStatus}
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            {isEditing ? `Edit Invoice: ${existingRecord.name}` : 'New Sales Invoice'}
            <span className="text-xs font-mono font-normal text-slate-400 px-2 py-0.5 bg-slate-100 rounded-md">
              {namingSeries}
            </span>
          </h1>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'receivables' })}
            className="flex items-center gap-1.5 px-3.5 py-2 border border-slate-200 hover:bg-slate-50 text-slate-600 text-[12.5px] font-medium rounded-xl transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            <span>Discard</span>
          </button>

          <button
            type="button"
            onClick={() => handleSubmit('Draft')}
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-3.5 py-2 border border-indigo-200 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-[12.5px] font-semibold rounded-xl transition-colors"
          >
            <span>Save Draft</span>
          </button>

          <button
            type="button"
            onClick={() => handleSubmit('Submitted')}
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white text-[12.5px] font-semibold rounded-xl shadow-xs transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{isSubmitting ? 'Posting...' : 'Save & Submit'}</span>
          </button>
        </div>
      </div>

      {/* Section 1: Customer & Primary Accounting */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-5">
        <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-indigo-600" />
            <h2 className="text-[13.5px] font-bold text-slate-900 uppercase tracking-wider">
              1. Customer & General Ledger Details
            </h2>
          </div>
          <span className="text-[11px] font-medium text-slate-400">ERPNext Frappe Cloud Spec</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-[13px]">
          {/* Customer Selection */}
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">
              Customer <span className="text-rose-500 font-bold">*</span>
            </label>
            <select
              value={customer}
              onChange={(e) => handleCustomerChange(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 font-medium"
            >
              {customerList.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {/* Customer Name Display */}
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Customer Legal Name</label>
            <input
              type="text"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 font-medium"
            />
          </div>

          {/* Naming Series */}
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Series</label>
            <input
              type="text"
              value={namingSeries}
              onChange={(e) => setNamingSeries(e.target.value)}
              className="w-full px-3 py-2 bg-slate-100 border border-slate-200 rounded-lg text-slate-500 font-mono text-xs"
              readOnly
            />
          </div>

          {/* Posting Date */}
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700 flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              Posting Date <span className="text-rose-500 font-bold">*</span>
            </label>
            <input
              type="date"
              value={postingDate}
              onChange={(e) => setPostingDate(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900"
            />
          </div>

          {/* Due Date */}
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              Payment Due Date <span className="text-rose-500 font-bold">*</span>
            </label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-indigo-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900 font-medium"
            />
          </div>

          {/* Cost Center */}
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700 flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5 text-slate-400" />
              Cost Center
            </label>
            <select
              value={costCenter}
              onChange={(e) => setCostCenter(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900"
            >
              <option value="Main - CB">Main - CB (01)</option>
              <option value="Operations - CB">Operations - CB (02)</option>
              <option value="Sales & Marketing - CB">Sales & Marketing - CB (03)</option>
              <option value="Admin - CB">Admin - CB (04)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Section 2: Address & Contact Details */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
        <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-emerald-600" />
            <h2 className="text-[13.5px] font-bold text-slate-900 uppercase tracking-wider">
              2. Address & Contact
            </h2>
          </div>
          <span className="text-[11px] text-slate-400">GST Billing & Shipping Place</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[13px]">
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Billing Address</label>
            <textarea
              rows={3}
              value={customerAddress}
              onChange={(e) => setCustomerAddress(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Shipping Address</label>
            <textarea
              rows={3}
              value={shippingAddress}
              onChange={(e) => setShippingAddress(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Contact Person</label>
            <input
              type="text"
              value={contactPerson}
              onChange={(e) => setContactPerson(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div className="space-y-1.5">
              <label className="block font-medium text-slate-700">Mobile Phone</label>
              <input
                type="text"
                value={contactMobile}
                onChange={(e) => setContactMobile(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
              />
            </div>
            <div className="space-y-1.5">
              <label className="block font-medium text-slate-700">Email Address</label>
              <input
                type="email"
                value={contactEmail}
                onChange={(e) => setContactEmail(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Section 3: ERPNext Interactive Items Child Table */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-600" />
            <h2 className="text-[13.5px] font-bold text-slate-900 uppercase tracking-wider">
              3. Items (Products & Services Fulfillment)
            </h2>
          </div>
          <button
            type="button"
            onClick={handleAddItem}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Row</span>
          </button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto border border-slate-200 rounded-xl">
          <table className="w-full text-left text-[12.5px]">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold text-[11px] uppercase tracking-wider">
              <tr>
                <th className="py-2.5 px-3 w-10 text-center">#</th>
                <th className="py-2.5 px-3 min-w-[200px]">Item Code / Name</th>
                <th className="py-2.5 px-3 min-w-[220px]">Description</th>
                <th className="py-2.5 px-3 w-24 text-right">Quantity</th>
                <th className="py-2.5 px-3 w-24">UOM</th>
                <th className="py-2.5 px-3 w-32 text-right">Rate (₹)</th>
                <th className="py-2.5 px-3 w-32 text-right">Amount (₹)</th>
                <th className="py-2.5 px-2 w-10 text-center"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {items.map((it, idx) => (
                <tr key={it.id || idx} className="hover:bg-slate-50/50">
                  <td className="py-2.5 px-3 text-center text-slate-400 font-mono text-xs">
                    {idx + 1}
                  </td>
                  <td className="py-2.5 px-3">
                    <input
                      type="text"
                      value={it.item_name}
                      onChange={(e) => handleItemChange(idx, 'item_name', e.target.value)}
                      placeholder="Item name..."
                      className="w-full px-2 py-1.5 bg-slate-50 border border-slate-200 rounded focus:bg-white text-slate-900 font-medium text-xs"
                    />
                  </td>
                  <td className="py-2.5 px-3">
                    <input
                      type="text"
                      value={it.description || ''}
                      onChange={(e) => handleItemChange(idx, 'description', e.target.value)}
                      placeholder="Line item description..."
                      className="w-full px-2 py-1.5 bg-slate-50 border border-slate-200 rounded focus:bg-white text-slate-600 text-xs"
                    />
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <input
                      type="number"
                      value={it.qty}
                      min="1"
                      onChange={(e) => handleItemChange(idx, 'qty', e.target.value)}
                      className="w-full px-2 py-1.5 bg-slate-50 border border-slate-200 rounded text-right focus:bg-white font-mono text-xs"
                    />
                  </td>
                  <td className="py-2.5 px-3">
                    <select
                      value={it.uom || 'Nos'}
                      onChange={(e) => handleItemChange(idx, 'uom', e.target.value)}
                      className="w-full px-2 py-1.5 bg-slate-50 border border-slate-200 rounded text-xs"
                    >
                      <option value="Nos">Nos</option>
                      <option value="Box">Box</option>
                      <option value="Hrs">Hrs</option>
                      <option value="Kg">Kg</option>
                      <option value="Set">Set</option>
                    </select>
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <input
                      type="number"
                      value={it.rate}
                      onChange={(e) => handleItemChange(idx, 'rate', e.target.value)}
                      className="w-full px-2 py-1.5 bg-slate-50 border border-slate-200 rounded text-right focus:bg-white font-mono font-medium text-xs"
                    />
                  </td>
                  <td className="py-2.5 px-3 text-right font-mono font-bold text-slate-900">
                    ₹{Number(it.amount || 0).toLocaleString('en-IN')}
                  </td>
                  <td className="py-2.5 px-2 text-center">
                    <button
                      type="button"
                      onClick={() => handleRemoveItem(idx)}
                      className="p-1 text-slate-300 hover:text-rose-600 transition-colors"
                      title="Delete line"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot className="bg-slate-50 font-bold border-t border-slate-200">
              <tr>
                <td colSpan={6} className="py-2.5 px-4 text-right text-slate-600 uppercase tracking-wider text-[11px]">
                  Net Total of Items:
                </td>
                <td className="py-2.5 px-3 text-right font-mono text-sm text-slate-900">
                  ₹{netTotal.toLocaleString('en-IN')}
                </td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      {/* Section 4: Taxes and Charges (Indian GST Engine) */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
        <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Percent className="w-4 h-4 text-amber-600" />
            <h2 className="text-[13.5px] font-bold text-slate-900 uppercase tracking-wider">
              4. Taxes and Charges (Indian GST Calculation)
            </h2>
          </div>
          <span className="text-[11px] font-medium text-slate-400">Automated CGST/SGST/IGST</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[13px]">
          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Tax Category</label>
            <select
              value={taxCategory}
              onChange={(e) => setTaxCategory(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900"
            >
              <option value="In-State GST (CGST + SGST)">In-State GST (Intra-State MSME)</option>
              <option value="Out-of-State GST (IGST)">Out-of-State GST (Inter-State Trade)</option>
              <option value="Reverse Charge Mechanism (RCM)">Reverse Charge Mechanism (RCM)</option>
              <option value="Zero Rated / SEZ Export">Zero Rated / SEZ Export</option>
            </select>
          </div>

          <div className="space-y-1.5">
            <label className="block font-medium text-slate-700">Sales Taxes & Charges Template</label>
            <select
              value={taxTemplate}
              onChange={(e) => setTaxTemplate(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
            >
              <option value="in_state_18">In-State GST 18% (CGST 9% + SGST 9%)</option>
              <option value="out_state_18">Out-of-State GST 18% (IGST 18%)</option>
              <option value="exempt">Nil Rated / Exempt (0%)</option>
            </select>
          </div>
        </div>

        {/* Tax Breakdown Preview */}
        {taxBreakdown.rows.length > 0 && (
          <div className="border border-slate-200 rounded-xl overflow-hidden mt-3">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase">
                <tr>
                  <th className="py-2 px-3">Type</th>
                  <th className="py-2 px-3">Account Head</th>
                  <th className="py-2 px-3 text-right">Tax Rate</th>
                  <th className="py-2 px-3 text-right">Computed Tax (₹)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {taxBreakdown.rows.map((tx, i) => (
                  <tr key={i} className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 text-slate-500 font-medium">On Net Total</td>
                    <td className="py-2 px-3 font-semibold text-slate-800">{tx.account}</td>
                    <td className="py-2 px-3 text-right font-mono text-slate-600">{tx.rate}</td>
                    <td className="py-2 px-3 text-right font-mono font-bold text-slate-900">
                      ₹{tx.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Section 5: Real-time Totals & Financial Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Payment Terms & Notes */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center gap-2">
              <FileText className="w-4 h-4 text-indigo-600" />
              <h2 className="text-[13.5px] font-bold text-slate-900 uppercase tracking-wider">
                5. Payment Terms & Commercial Notes
              </h2>
            </div>

            <div className="space-y-3 text-[13px]">
              <div>
                <label className="block font-medium text-slate-700 mb-1">
                  Payment Terms Template
                </label>
                <select
                  value={paymentTermsTemplate}
                  onChange={(e) => setPaymentTermsTemplate(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
                >
                  <option value="Standard Net 30">Standard Net 30 (Full payment in 30 days)</option>
                  <option value="Net 15 Days">Net 15 Days (Quick MSME settlement)</option>
                  <option value="100% Advance">Immediate Payment (100% Advance on order)</option>
                  <option value="Milestone 50-50">Milestone 50-50 (50% Advance, 50% on Delivery)</option>
                </select>
              </div>

              <div>
                <label className="block font-medium text-slate-700 mb-1">Terms & Conditions</label>
                <textarea
                  rows={2}
                  value={terms}
                  onChange={(e) => setTerms(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-700 mb-1">Internal Remarks</label>
                <input
                  type="text"
                  value={remarks}
                  onChange={(e) => setRemarks(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Live Computation Card (Exact ERPNext Totals) */}
        <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-xl space-y-5 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <span className="text-xs font-semibold tracking-wider uppercase text-slate-400">
                Invoice Financial Summary
              </span>
              <span className="text-[11px] font-mono text-emerald-400 font-semibold">
                Auto-Computed
              </span>
            </div>

            <div className="space-y-2.5 text-xs text-slate-300">
              <div className="flex justify-between items-center">
                <span>Net Total (Base):</span>
                <span className="font-mono text-white text-sm">
                  ₹{netTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span>Total Taxes & Charges (18%):</span>
                <span className="font-mono text-amber-400 text-sm">
                  + ₹{taxBreakdown.totalTax.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              <div className="flex justify-between items-center text-slate-400 pt-1 border-t border-slate-800">
                <span>Rounding Adjustment:</span>
                <span className="font-mono text-xs">
                  ₹{roundingAdjustment.toFixed(2)}
                </span>
              </div>

              <div className="flex justify-between items-center pt-2 border-t-2 border-slate-700 text-sm font-bold text-white">
                <span>Grand Total:</span>
                <span className="font-mono text-lg text-emerald-400 font-black">
                  ₹{roundedTotal.toLocaleString('en-IN')}
                </span>
              </div>
            </div>

            {/* Advance / Paid Allocation */}
            <div className="bg-slate-800/80 p-3.5 rounded-xl space-y-2 border border-slate-700/50 mt-4">
              <label className="block text-[11.5px] font-medium text-slate-300">
                Advance / Instant Payment Received (₹):
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs font-bold">
                  ₹
                </span>
                <input
                  type="number"
                  min="0"
                  max={roundedTotal}
                  value={paidAdvance}
                  onChange={(e) => setPaidAdvance(Math.max(0, Number(e.target.value) || 0))}
                  placeholder="0.00"
                  className="w-full pl-8 pr-3 py-1.5 bg-slate-900 border border-slate-600 rounded-lg text-white font-mono text-sm focus:outline-none focus:ring-1 focus:ring-emerald-400"
                />
              </div>

              <div className="flex justify-between items-center pt-2 text-xs border-t border-slate-700">
                <span className="text-slate-400 font-medium">Outstanding Balance:</span>
                <span className="font-mono font-bold text-rose-400 text-sm">
                  ₹{outstandingAmount.toLocaleString('en-IN')}
                </span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 space-y-2">
            <button
              type="button"
              onClick={() => handleSubmit('Submitted')}
              disabled={isSubmitting}
              className="w-full py-2.5 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs uppercase tracking-wider transition-all shadow-md flex items-center justify-center gap-2"
            >
              <Save className="w-4 h-4" />
              <span>{isSubmitting ? 'Posting...' : 'Post Sales Invoice to Ledger'}</span>
            </button>
            <p className="text-[11px] text-slate-400 text-center leading-relaxed">
              Updates PostgreSQL, General Ledger, Accounts Receivable Aging & Customer Balance.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}