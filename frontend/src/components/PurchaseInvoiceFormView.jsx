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

export default function PurchaseInvoiceFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('purchase_invoice', recordId) : null;
  const isEditing = !!existingRecord;

  // Auto-fetch cost centers, accounts, and suppliers
  useEffect(() => {
    fetchDomainRecords('account');
    fetchDomainRecords('cost_center');
    fetchDomainRecords('supplier');
  }, []);

  const costCenters = getDomainRecords('cost_center');
  const accounts = getDomainRecords('account');

  // Supplier suggestions
  const supplierList = [
    { name: 'Tata Steel Processing Ltd', contact: 'Rajesh Nair', phone: '+91 98555 56789', email: 'rajesh@tatasteel.com', gstin: '27AABCT1332L1Z1', address: 'Industrial Area, Jamshedpur 831001' },
    { name: 'Schneider Electric India Pvt Ltd', contact: 'Amit Sengupta', phone: '+91 98222 67890', email: 'amit@schneider.in', gstin: '27AABCS9821M1Z2', address: 'Plot 18, MIDC Tarapur, Palghar 401506' },
    { name: 'Bosch Automotive Components', contact: 'Suresh Patil', phone: '+91 98111 78901', email: 'suresh@bosch.in', gstin: '27AABCB4455N1Z3', address: 'MIDC Chakan, Phase 2, Pune 410501' },
    { name: 'Dell Technologies India', contact: 'Deepak Varma', phone: '+91 98777 89012', email: 'deepak@dell.in', gstin: '29AABCD1122K1Z4', address: 'Bagmane Tech Park, CV Raman Nagar, Bengaluru 560093' },
    { name: 'Godrej Office Supplies Ltd', contact: 'Neha Kulkarni', phone: '+91 98666 90123', email: 'neha@godrej.in', gstin: '27AABCG5544P1Z5', address: 'Pirojshanagar, Vikhroli East, Mumbai 400079' }
  ];

  // Primary State
  const [supplier, setSupplier] = useState(existingRecord?.supplier || 'Tata Steel Processing Ltd');
  const [supplierName, setSupplierName] = useState(existingRecord?.supplier_name || 'Tata Steel Processing Ltd');
  const [billNo, setBillNo] = useState(existingRecord?.bill_no || `INV-SUP-${Math.floor(1000 + Math.random() * 9000)}`);
  const [billDate, setBillDate] = useState(existingRecord?.bill_date || new Date().toISOString().slice(0, 10));
  const [namingSeries, setNamingSeries] = useState(existingRecord?.naming_series || 'ACC-PINV-.YYYY.-');
  const [postingDate, setPostingDate] = useState(existingRecord?.posting_date || new Date().toISOString().slice(0, 10));
  const [dueDate, setDueDate] = useState(() => {
    if (existingRecord?.due_date) return existingRecord.due_date;
    const d = new Date();
    d.setDate(d.getDate() + 30);
    return d.toISOString().slice(0, 10);
  });
  const [currency, setCurrency] = useState(existingRecord?.currency || 'INR');
  const [costCenterId, setCostCenterId] = useState(existingRecord?.cost_center_id || 'Main - CB');
  const [status, setStatus] = useState(existingRecord?.status || 'Draft');

  // Supplier Address & Contact
  const [supplierAddress, setSupplierAddress] = useState(
    existingRecord?.supplier_address || 'Industrial Area, Jamshedpur 831001'
  );
  const [contactPerson, setContactPerson] = useState(existingRecord?.contact_person || 'Rajesh Nair');
  const [contactMobile, setContactMobile] = useState(existingRecord?.contact_mobile || '+91 98555 56789');
  const [contactEmail, setContactEmail] = useState(existingRecord?.contact_email || 'rajesh@tatasteel.com');
  const [supplierGstin, setSupplierGstin] = useState(existingRecord?.tax_id || '27AABCT1332L1Z1');

  // Purchase Line Items (Child Table)
  const [items, setItems] = useState(() => {
    if (existingRecord?.items && Array.isArray(existingRecord.items) && existingRecord.items.length > 0) {
      return existingRecord.items;
    }
    return [
      {
        id: 'item-1',
        item_code: 'RM-STEEL-001',
        item_name: 'CRCA Steel Coils Grade-A (2mm)',
        description: 'Cold Rolled Close Annealed Steel Sheets for chassis fabrication',
        qty: 5,
        uom: 'Ton',
        rate: 55000,
        amount: 275000
      },
      {
        id: 'item-2',
        item_code: 'CONS-FAST-010',
        item_name: 'High Tensile Fasteners M12x50',
        description: 'Grade 8.8 Galvanized Hex Bolt assemblies with spring washers',
        qty: 200,
        uom: 'Nos',
        rate: 125,
        amount: 25000
      }
    ];
  });

  // Taxes & Charges
  const [taxCategory, setTaxCategory] = useState(existingRecord?.tax_category || 'In-State GST 18%');
  const [applyTds, setApplyTds] = useState(existingRecord?.apply_tds ?? true);
  const [tdsRate, setTdsRate] = useState(2); // 2% TDS u/s 194C

  // Payment Terms & Remarks
  const [paymentTerms, setPaymentTerms] = useState(existingRecord?.payment_terms || 'Net 30 Days after 3-way GRN verification');
  const [remarks, setRemarks] = useState(existingRecord?.remarks || 'Received against Purchase Order PO-2026-0042. Quality QA passed.');

  const [isSubmitting, setIsSubmitting] = useState(false);

  // When supplier changes, auto-populate details
  const handleSupplierSelect = (name) => {
    setSupplier(name);
    setSupplierName(name);
    const found = supplierList.find(s => s.name === name);
    if (found) {
      setContactPerson(found.contact);
      setContactMobile(found.phone);
      setContactEmail(found.email);
      setSupplierAddress(found.address);
      setSupplierGstin(found.gstin);
    }
  };

  // Line Item Row Handlers
  const handleItemChange = (id, field, value) => {
    setItems(prev => prev.map(item => {
      if (item.id === id) {
        const updated = { ...item, [field]: value };
        if (field === 'qty' || field === 'rate') {
          const q = field === 'qty' ? Number(value) || 0 : Number(item.qty) || 0;
          const r = field === 'rate' ? Number(value) || 0 : Number(item.rate) || 0;
          updated.amount = q * r;
        }
        return updated;
      }
      return item;
    }));
  };

  const handleAddItem = () => {
    const newId = `item-${Date.now()}`;
    setItems(prev => [
      ...prev,
      {
        id: newId,
        item_code: `ITEM-${Math.floor(100 + Math.random() * 900)}`,
        item_name: 'Industrial Raw Material Batch',
        description: 'Standard technical specification per PO',
        qty: 1,
        uom: 'Nos',
        rate: 10000,
        amount: 10000
      }
    ]);
  };

  const handleRemoveItem = (id) => {
    if (items.length <= 1) {
      onShowToast?.('At least one purchase item row is required', 'error');
      return;
    }
    setItems(prev => prev.filter(item => item.id !== id));
  };

  // Calculations
  const calculations = useMemo(() => {
    const netTotal = items.reduce((sum, item) => sum + (Number(item.amount) || 0), 0);
    const totalQty = items.reduce((sum, item) => sum + (Number(item.qty) || 0), 0);

    let cgst = 0;
    let sgst = 0;
    let igst = 0;

    if (taxCategory === 'In-State GST 18%') {
      cgst = Math.round(netTotal * 0.09 * 100) / 100;
      sgst = Math.round(netTotal * 0.09 * 100) / 100;
    } else if (taxCategory === 'Out-of-State IGST 18%') {
      igst = Math.round(netTotal * 0.18 * 100) / 100;
    }

    const totalTaxes = cgst + sgst + igst;
    const tdsAmount = applyTds ? Math.round(netTotal * (tdsRate / 100) * 100) / 100 : 0;
    const grandTotal = netTotal + totalTaxes - tdsAmount;
    const roundedTotal = Math.round(grandTotal);
    const roundingDiff = Math.round((roundedTotal - grandTotal) * 100) / 100;

    return {
      netTotal,
      totalQty,
      cgst,
      sgst,
      igst,
      totalTaxes,
      tdsAmount,
      grandTotal: roundedTotal,
      roundingDiff,
      outstandingAmount: roundedTotal
    };
  }, [items, taxCategory, applyTds, tdsRate]);

  // Handle Save / Submit
  const handleSave = async (submitStatus = 'Draft') => {
    if (!supplier) {
      onShowToast?.('Please enter or select a Supplier', 'error');
      return;
    }
    if (items.length === 0) {
      onShowToast?.('Please add at least one line item', 'error');
      return;
    }

    setIsSubmitting(true);

    const recordName = existingRecord?.name || `ACC-PINV-2026-${Math.floor(10000 + Math.random() * 90000)}`;

    const payload = {
      name: recordName,
      title: `${supplier} - ${billNo}`,
      supplier,
      supplier_name: supplierName,
      bill_no: billNo,
      bill_date: billDate,
      naming_series: namingSeries,
      posting_date: postingDate,
      due_date: dueDate,
      currency,
      cost_center_id: costCenterId,
      status: submitStatus === 'Submitted' ? 'Submitted' : 'Draft',
      docstatus: submitStatus === 'Submitted' ? 1 : 0,

      supplier_address: supplierAddress,
      contact_person: contactPerson,
      contact_mobile: contactMobile,
      contact_email: contactEmail,
      tax_id: supplierGstin,

      net_total: calculations.netTotal,
      total_taxes_and_charges: calculations.totalTaxes,
      apply_tds: applyTds,
      grand_total: calculations.grandTotal,
      rounded_total: calculations.grandTotal,
      outstanding_amount: calculations.outstandingAmount,

      payment_terms: paymentTerms,
      remarks,
      items
    };

    try {
      // 1. Direct Backend API attempt
      const res = await fetch('/v1/purchase-invoice', {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(() => null);

      if (res && res.ok) {
        onShowToast?.(`Purchase Invoice ${recordName} saved & synced to PostgreSQL!`);
      } else {
        // 2. RecordsContext Store Update
        if (isEditing) {
          updateRecord('purchase_invoice', recordId, payload);
          onShowToast?.(`Purchase Invoice ${recordName} updated in local store!`);
        } else {
          addRecord('purchase_invoice', payload);
          onShowToast?.(`Purchase Invoice ${recordName} saved!`);
        }
      }

      onNavigate({ type: 'list', domain: 'purchase_invoice' });
    } catch (err) {
      console.error(err);
      onShowToast?.('Failed to save purchase invoice', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      {/* Top Header Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate({ type: 'list', domain: 'purchase_invoice' })}
              className="p-1 -ml-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Accounts Payable • Purchase Invoice
            </span>
            <span className="text-slate-300">•</span>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
              status === 'Submitted'
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : 'bg-amber-50 text-amber-700 border border-amber-200'
            }`}>
              {status}
            </span>
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            {isEditing ? `Edit Purchase Invoice: ${existingRecord?.name}` : 'New Purchase Invoice'}
          </h1>
          <p className="text-[12.5px] text-slate-500">
            Record supplier bill, credit purchase ledger, and claim Input Tax Credit (ITC) per ERPNext standards.
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'list', domain: 'purchase_invoice' })}
            className="flex items-center gap-1.5 px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-600 text-[13px] font-medium rounded-xl transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            <span>Cancel</span>
          </button>

          <button
            type="button"
            onClick={() => handleSave('Draft')}
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-[13px] font-semibold rounded-xl transition-colors"
          >
            <Save className="w-3.5 h-3.5" />
            <span>Save Draft</span>
          </button>

          <button
            type="button"
            onClick={() => handleSave('Submitted')}
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-[13px] font-semibold rounded-xl transition-all shadow-xs"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Submit to Payable Ledger</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (2 Cols wide) - Invoice Form Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section 1: Supplier & Dates */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-5">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Building2 className="w-4 h-4 text-indigo-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Supplier & Billing Details
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 1 of 5</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Supplier <span className="text-rose-500 font-bold">*</span>
                </label>
                <div className="relative">
                  <input
                    type="text"
                    list="supplier-options"
                    value={supplier}
                    onChange={(e) => handleSupplierSelect(e.target.value)}
                    placeholder="Search or select supplier..."
                    className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                  />
                  <datalist id="supplier-options">
                    {supplierList.map(s => (
                      <option key={s.name} value={s.name}>{s.name} ({s.gstin})</option>
                    ))}
                  </datalist>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Supplier Invoice / Bill No <span className="text-rose-500 font-bold">*</span>
                </label>
                <input
                  type="text"
                  value={billNo}
                  onChange={(e) => setBillNo(e.target.value)}
                  placeholder="e.g. INV/2026/089"
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Supplier Bill Date
                </label>
                <input
                  type="date"
                  value={billDate}
                  onChange={(e) => setBillDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Posting Date
                </label>
                <input
                  type="date"
                  value={postingDate}
                  onChange={(e) => setPostingDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Payment Due Date
                </label>
                <input
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Cost Center
                </label>
                <select
                  value={costCenterId}
                  onChange={(e) => setCostCenterId(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                >
                  <option value="Main - CB">Main - CB</option>
                  <option value="Operations - CB">Operations - CB</option>
                  <option value="Manufacturing - CB">Manufacturing - CB</option>
                  <option value="Procurement - CB">Procurement - CB</option>
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Address & GSTIN */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-emerald-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Supplier Address & Tax ID
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 2 of 5</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="sm:col-span-2 space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Supplier Factory / Billing Address
                </label>
                <input
                  type="text"
                  value={supplierAddress}
                  onChange={(e) => setSupplierAddress(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Supplier GSTIN / Tax ID
                </label>
                <input
                  type="text"
                  value={supplierGstin}
                  onChange={(e) => setSupplierGstin(e.target.value)}
                  placeholder="27AABCT1332L1Z1"
                  className="w-full px-3 py-2 text-[13px] font-mono bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Contact Person / Dispatch Officer
                </label>
                <input
                  type="text"
                  value={contactPerson}
                  onChange={(e) => setContactPerson(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>
            </div>
          </div>

          {/* Section 3: Interactive Line Items Child Table */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-violet-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Purchase Line Items Table
                </h2>
              </div>
              <button
                type="button"
                onClick={handleAddItem}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-lg transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Row</span>
              </button>
            </div>

            {/* Desktop Table View */}
            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3 w-10 text-center">#</th>
                    <th className="py-2.5 px-3 min-w-[180px]">Item Code & Name</th>
                    <th className="py-2.5 px-3 min-w-[200px]">Description</th>
                    <th className="py-2.5 px-3 w-24 text-right">Qty</th>
                    <th className="py-2.5 px-3 w-20">UOM</th>
                    <th className="py-2.5 px-3 w-28 text-right">Rate (₹)</th>
                    <th className="py-2.5 px-3 w-32 text-right">Amount (₹)</th>
                    <th className="py-2.5 px-2 w-10 text-center"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-sans">
                  {items.map((item, idx) => (
                    <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="py-2 px-3 text-center text-slate-400 font-mono">
                        {idx + 1}
                      </td>
                      <td className="py-2 px-3 space-y-1">
                        <input
                          type="text"
                          value={item.item_name}
                          onChange={(e) => handleItemChange(item.id, 'item_name', e.target.value)}
                          className="w-full font-medium text-slate-900 bg-transparent border-0 border-b border-transparent focus:border-indigo-500 focus:bg-white focus:outline-none p-1 rounded"
                        />
                        <div className="text-[10.5px] font-mono text-slate-400 px-1">
                          {item.item_code}
                        </div>
                      </td>
                      <td className="py-2 px-3">
                        <input
                          type="text"
                          value={item.description}
                          onChange={(e) => handleItemChange(item.id, 'description', e.target.value)}
                          className="w-full text-slate-600 bg-transparent border-0 border-b border-transparent focus:border-indigo-500 focus:bg-white focus:outline-none p-1 rounded"
                        />
                      </td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          min="1"
                          value={item.qty}
                          onChange={(e) => handleItemChange(item.id, 'qty', e.target.value)}
                          className="w-20 text-right font-medium text-slate-900 bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:outline-none p-1.5 rounded"
                        />
                      </td>
                      <td className="py-2 px-3">
                        <select
                          value={item.uom}
                          onChange={(e) => handleItemChange(item.id, 'uom', e.target.value)}
                          className="w-full text-slate-700 bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:outline-none p-1.5 rounded"
                        >
                          <option value="Nos">Nos</option>
                          <option value="Ton">Ton</option>
                          <option value="Kg">Kg</option>
                          <option value="Meter">Meter</option>
                          <option value="Hours">Hours</option>
                        </select>
                      </td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          value={item.rate}
                          onChange={(e) => handleItemChange(item.id, 'rate', e.target.value)}
                          className="w-24 text-right font-mono text-slate-900 bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:outline-none p-1.5 rounded"
                        />
                      </td>
                      <td className="py-2 px-3 text-right font-mono font-semibold text-slate-900">
                        ₹{(Number(item.amount) || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="py-2 px-2 text-center">
                        <button
                          type="button"
                          onClick={() => handleRemoveItem(item.id)}
                          className="text-slate-300 hover:text-rose-600 p-1 rounded transition-colors"
                          title="Delete Row"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between pt-1">
              <button
                type="button"
                onClick={handleAddItem}
                className="flex items-center gap-1.5 px-3 py-1.5 border border-dashed border-slate-300 hover:border-indigo-500 hover:text-indigo-600 text-slate-600 text-xs font-semibold rounded-lg transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>+ Add Item Row</span>
              </button>
              <div className="text-xs text-slate-500">
                Total Units: <span className="font-semibold text-slate-800">{calculations.totalQty}</span> • Items: <span className="font-semibold text-slate-800">{items.length}</span>
              </div>
            </div>
          </div>

          {/* Section 4: Taxes, ITC & TDS */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Percent className="w-4 h-4 text-amber-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Input GST (ITC) & TDS Deductions
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 4 of 5</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  GST Tax Template
                </label>
                <select
                  value={taxCategory}
                  onChange={(e) => setTaxCategory(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                >
                  <option value="In-State GST 18%">In-State GST 18% (CGST 9% + SGST 9%) - Full ITC</option>
                  <option value="Out-of-State IGST 18%">Out-of-State IGST 18% - Full ITC</option>
                  <option value="Exempt / Nil Rated">Exempt / Nil Rated (0%)</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  TDS Deduction (Income Tax Act)
                </label>
                <div className="flex items-center gap-3 pt-1">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={applyTds}
                      onChange={(e) => setApplyTds(e.target.checked)}
                      className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span className="text-xs text-slate-700 font-medium">Apply TDS u/s 194C</span>
                  </label>
                  {applyTds && (
                    <select
                      value={tdsRate}
                      onChange={(e) => setTdsRate(Number(e.target.value))}
                      className="text-xs px-2 py-1 bg-slate-50 border border-slate-200 rounded"
                    >
                      <option value={1}>1% (Individual/HUF)</option>
                      <option value={2}>2% (Corporate Contractor)</option>
                      <option value={10}>10% (Technical Services 194J)</option>
                    </select>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Section 5: Terms & Remarks */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Payment Terms & Commercial Remarks
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 5 of 5</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Payment Terms Template
                </label>
                <input
                  type="text"
                  value={paymentTerms}
                  onChange={(e) => setPaymentTerms(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Internal Notes & PO Reference
                </label>
                <input
                  type="text"
                  value={remarks}
                  onChange={(e) => setRemarks(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (1 Col wide) - Real-Time Financial Summary Card */}
        <div className="space-y-6">
          <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg border border-slate-800 space-y-6 sticky top-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center gap-2">
                <Calculator className="w-4 h-4 text-indigo-400" />
                <h3 className="text-xs font-bold uppercase tracking-widest text-slate-300">
                  Accounts Payable Summary
                </h3>
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                INR (₹)
              </span>
            </div>

            {/* Calculations Breakdown */}
            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between text-slate-300">
                <span>Net Total (Excl. Tax)</span>
                <span className="font-mono font-medium text-white">
                  ₹{calculations.netTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              {calculations.cgst > 0 && (
                <div className="flex items-center justify-between text-slate-400 pl-2">
                  <span>Input CGST (9%)</span>
                  <span className="font-mono text-emerald-400">
                    +₹{calculations.cgst.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              )}

              {calculations.sgst > 0 && (
                <div className="flex items-center justify-between text-slate-400 pl-2">
                  <span>Input SGST (9%)</span>
                  <span className="font-mono text-emerald-400">
                    +₹{calculations.sgst.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              )}

              {calculations.igst > 0 && (
                <div className="flex items-center justify-between text-slate-400 pl-2">
                  <span>Input IGST (18%)</span>
                  <span className="font-mono text-emerald-400">
                    +₹{calculations.igst.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              )}

              {calculations.tdsAmount > 0 && (
                <div className="flex items-center justify-between text-slate-400 pl-2">
                  <span>Less: TDS u/s 194C ({tdsRate}%)</span>
                  <span className="font-mono text-amber-400">
                    -₹{calculations.tdsAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              )}

              <div className="border-t border-slate-800 pt-3 flex items-center justify-between text-sm font-bold text-white">
                <span>Grand Total (Payable)</span>
                <span className="font-mono text-lg text-emerald-400">
                  ₹{calculations.grandTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-400 pt-1 border-t border-slate-800">
                <span>Outstanding Payable</span>
                <span className="font-mono font-semibold text-rose-400">
                  ₹{calculations.outstandingAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>
            </div>

            {/* Quick Submit Button in Card */}
            <div className="pt-2">
              <button
                type="button"
                onClick={() => handleSave('Submitted')}
                disabled={isSubmitting}
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold text-xs uppercase tracking-wider rounded-xl transition-all shadow-md flex items-center justify-center gap-2"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Submit to Ledger</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
