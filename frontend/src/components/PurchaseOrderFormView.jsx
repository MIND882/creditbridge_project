import React, { useState, useMemo, useEffect } from 'react';
import {
  ArrowLeft,
  Save,
  X,
  Plus,
  Trash2,
  Calculator,
  Truck,
  Building2,
  Calendar,
  Clock,
  MapPin,
  Phone,
  Mail,
  FileText,
  CreditCard,
  Percent,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Layers,
  ChevronDown
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function PurchaseOrderFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('purchase_order', recordId) : null;
  const isEditing = !!existingRecord;

  useEffect(() => {
    fetchDomainRecords('supplier');
  }, []);

  const suppliersFromDb = getDomainRecords('supplier') || [];

  const defaultSuppliers = [
    { name: 'Tata Steel Limited', contact: 'Rajesh Nambiar', phone: '+91 98210 11223', email: 'procurement@tatasteel.com', gstin: '20AAACT2727Q1ZW', address: 'Bombay House, 24 Homi Mody Street, Fort, Mumbai 400001' },
    { name: 'Schneider Electric India Pvt Ltd', contact: 'Sunita Kapoor', phone: '+91 98100 44556', email: 'orders@schneider-electric.co.in', gstin: '06AAACS8494J1Z6', address: 'DLF Cyber City, Building 10, Tower B, Gurugram, Haryana 122002' },
    { name: 'Bosch Automotive Components', contact: 'Ganesh Hegde', phone: '+91 99011 88990', email: 'supplychain@bosch.in', gstin: '29AAACB3456F1Z8', address: 'Hosur Road, Adugodi, Bengaluru, Karnataka 560030' },
    { name: 'Wipro Cloud Infrastructure Services', contact: 'Kavita Menon', phone: '+91 98450 77665', email: 'vendor-desk@wipro.com', gstin: '29AAACW1234F1Z1', address: 'Doddakannelli, Sarjapur Road, Bengaluru, Karnataka 560035' }
  ];

  const supplierList = suppliersFromDb.length > 0 ? suppliersFromDb : defaultSuppliers;

  // Primary Form State
  const [supplierName, setSupplierName] = useState(
    existingRecord?.supplier_name || existingRecord?.supplier || supplierList[0]?.supplier_name || supplierList[0]?.name || 'Tata Steel Limited'
  );
  const [transactionDate, setTransactionDate] = useState(
    existingRecord?.transaction_date || new Date().toISOString().slice(0, 10)
  );
  const [scheduleDate, setScheduleDate] = useState(() => {
    if (existingRecord?.schedule_date) return existingRecord.schedule_date;
    const d = new Date();
    d.setDate(d.getDate() + 14);
    return d.toISOString().slice(0, 10);
  });
  const [company, setCompany] = useState(existingRecord?.company || 'CreditBridge MSME Ltd');
  const [currency, setCurrency] = useState(existingRecord?.currency || 'INR');
  const [status, setStatus] = useState(existingRecord?.status || 'Draft');

  // Supplier Details auto-sync
  const activeSupplier = useMemo(() => {
    return supplierList.find(s => (s.supplier_name === supplierName || s.name === supplierName)) || supplierList[0] || {};
  }, [supplierName, supplierList]);

  // Line Items Child Table
  const [items, setItems] = useState(() => {
    if (existingRecord?.items && existingRecord.items.length > 0) {
      return existingRecord.items;
    }
    return [
      {
        id: '1',
        item_code: 'RAW-STL-01',
        item_name: 'Hot Rolled Structural Steel Beams (Grade E250)',
        uom: 'Ton',
        qty: 2.0,
        rate: 55000.0,
        amount: 110000.0
      },
      {
        id: '2',
        item_code: 'ELEC-SW-02',
        item_name: 'Heavy Industrial Relays & Switchgear Units',
        uom: 'Nos',
        qty: 10.0,
        rate: 7644.06,
        amount: 76440.68
      }
    ];
  });

  const [taxRate, setTaxRate] = useState(18); // 18% GST standard
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Financial auto-calculations
  const netTotal = useMemo(() => {
    return items.reduce((acc, it) => acc + (Number(it.amount) || 0), 0);
  }, [items]);

  const taxAmount = useMemo(() => {
    return (netTotal * taxRate) / 100;
  }, [netTotal, taxRate]);

  const grandTotal = useMemo(() => {
    return Math.round((netTotal + taxAmount) * 100) / 100;
  }, [netTotal, taxAmount]);

  const handleItemChange = (index, field, value) => {
    setItems(prev => {
      const next = [...prev];
      const row = { ...next[index], [field]: value };
      if (field === 'qty' || field === 'rate') {
        const q = field === 'qty' ? parseFloat(value) || 0 : parseFloat(row.qty) || 0;
        const r = field === 'rate' ? parseFloat(value) || 0 : parseFloat(row.rate) || 0;
        row.amount = Math.round(q * r * 100) / 100;
      }
      next[index] = row;
      return next;
    });
  };

  const addItemRow = () => {
    setItems(prev => [
      ...prev,
      {
        id: String(Date.now()),
        item_code: `ITEM-PR-${Math.floor(100 + Math.random() * 900)}`,
        item_name: 'Industrial Consumables & Spare Parts',
        uom: 'Nos',
        qty: 1,
        rate: 10000,
        amount: 10000
      }
    ]);
  };

  const removeItemRow = (index) => {
    if (items.length <= 1) {
      onShowToast?.('At least one item line is required.', 'error');
      return;
    }
    setItems(prev => prev.filter((_, idx) => idx !== index));
  };

  const handleSave = async (submitNow = false) => {
    if (!supplierName) {
      onShowToast?.('Please select a Supplier.', 'error');
      return;
    }
    if (items.length === 0) {
      onShowToast?.('Please add at least one line item.', 'error');
      return;
    }

    setIsSubmitting(true);
    const docstatus = submitNow ? 1 : 0;
    const finalStatus = submitNow ? 'To Receive and Bill' : status;
    const poNumber = existingRecord?.name || `PUR-ORD-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    const payload = {
      name: poNumber,
      naming_series: 'PUR-ORD-.YYYY.-',
      supplier_id: activeSupplier.id || null,
      supplier_name: activeSupplier.supplier_name || supplierName,
      company: company,
      transaction_date: transactionDate,
      schedule_date: scheduleDate,
      currency: currency,
      conversion_rate: 1.0,
      net_total: netTotal,
      total_taxes_and_charges: taxAmount,
      grand_total: grandTotal,
      rounded_total: grandTotal,
      status: finalStatus,
      billing_status: 'Not Billed',
      delivery_status: 'Not Delivered',
      docstatus: docstatus,
      items: items
    };

    try {
      let savedToDb = false;
      try {
        const res = await fetch('/api/buying/purchase-order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          savedToDb = true;
        }
      } catch (err) {
        console.warn('[PostgreSQL PO API notice]', err.message);
      }

      if (isEditing) {
        await updateRecord('purchase_order', recordId, payload);
        onShowToast?.(
          savedToDb
            ? `Purchase Order ${poNumber} updated & synced with PostgreSQL!`
            : `Purchase Order ${poNumber} updated successfully!`,
          'success'
        );
      } else {
        await addRecord('purchase_order', payload);
        onShowToast?.(
          savedToDb
            ? `Purchase Order ${poNumber} created & stored in PostgreSQL database!`
            : `Purchase Order ${poNumber} created successfully!`,
          'success'
        );
      }

      fetchDomainRecords('purchase_order', true);
      onNavigate?.('list', 'purchase_order');
    } catch (err) {
      onShowToast?.(`Error saving PO: ${err.message}`, 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6 animate-fadeIn pb-12">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b pb-4">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => onNavigate?.('list', 'purchase_order')}
            className="p-2 hover:bg-slate-100 rounded-lg text-slate-600 transition"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded">
                Buying Module
              </span>
              <span className="text-xs text-slate-500">Domain #3 / 19</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">
              {isEditing ? `Purchase Order: ${existingRecord?.name}` : 'New Purchase Order (PO)'}
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              ERPNext Cloud standard procurement order • Submittable transaction with live GST taxes
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            type="button"
            onClick={() => onNavigate?.('list', 'purchase_order')}
            className="px-4 py-2 border rounded-lg text-slate-700 hover:bg-slate-50 transition flex items-center space-x-2"
          >
            <X className="w-4 h-4" />
            <span>Cancel</span>
          </button>
          <button
            type="button"
            onClick={() => handleSave(false)}
            disabled={isSubmitting}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg transition font-medium flex items-center space-x-2 disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>Save Draft</span>
          </button>
          <button
            type="button"
            onClick={() => handleSave(true)}
            disabled={isSubmitting}
            className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition font-medium shadow-sm flex items-center space-x-2 disabled:opacity-50"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>{isSubmitting ? 'Submitting...' : 'Submit PO to Database'}</span>
          </button>
        </div>
      </div>

      {/* Main Form Body */}
      <div className="space-y-6">
        {/* Section 1: Supplier & Date Master Details */}
        <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b pb-2">
            <div className="flex items-center space-x-2 text-slate-900 font-semibold">
              <Truck className="w-5 h-5 text-emerald-600" />
              <span>Supplier & Procurement Details</span>
            </div>
            <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${
              status === 'Draft' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
            }`}>
              Status: {status}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Supplier <span className="text-rose-500">*</span>
              </label>
              <select
                value={supplierName}
                onChange={(e) => setSupplierName(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                {supplierList.map((s, idx) => (
                  <option key={idx} value={s.supplier_name || s.name}>
                    {s.supplier_name || s.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                PO Posting Date <span className="text-rose-500">*</span>
              </label>
              <input
                type="date"
                value={transactionDate}
                onChange={(e) => setTransactionDate(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Required By / Delivery Date <span className="text-rose-500">*</span>
              </label>
              <input
                type="date"
                value={scheduleDate}
                onChange={(e) => setScheduleDate(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>
          </div>

          {/* Supplier Auto-Filled Context Card */}
          {activeSupplier && (
            <div className="bg-slate-50 border rounded-lg p-3 text-xs text-slate-600 grid grid-cols-1 md:grid-cols-3 gap-2">
              <div>
                <span className="font-semibold text-slate-800">GSTIN: </span>
                <span className="font-mono">{activeSupplier.tax_id || '20AAACT2727Q1ZW'}</span>
              </div>
              <div>
                <span className="font-semibold text-slate-800">Key Contact: </span>
                <span>{activeSupplier.supplier_primary_contact || activeSupplier.contact || 'Purchase Dept'}</span>
              </div>
              <div>
                <span className="font-semibold text-slate-800">Operating Address: </span>
                <span className="truncate block">{activeSupplier.primary_address || activeSupplier.address || 'Works, India'}</span>
              </div>
            </div>
          )}
        </div>

        {/* Section 2: Items Child Table */}
        <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b pb-2">
            <div className="flex items-center space-x-2 text-slate-900 font-semibold">
              <Layers className="w-5 h-5 text-emerald-600" />
              <span>Purchase Order Items & Pricing</span>
            </div>
            <button
              type="button"
              onClick={addItemRow}
              className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-medium rounded-lg transition flex items-center space-x-1"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Item Line</span>
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-600 text-xs uppercase font-semibold border-b">
                  <th className="py-2.5 px-3 w-12 text-center">#</th>
                  <th className="py-2.5 px-3 w-44">Item Code</th>
                  <th className="py-2.5 px-3">Description</th>
                  <th className="py-2.5 px-3 w-28">UOM</th>
                  <th className="py-2.5 px-3 w-28 text-right">Qty</th>
                  <th className="py-2.5 px-3 w-36 text-right">Rate (₹)</th>
                  <th className="py-2.5 px-3 w-36 text-right">Amount (₹)</th>
                  <th className="py-2.5 px-3 w-12 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.map((row, idx) => (
                  <tr key={row.id || idx} className="hover:bg-slate-50 transition">
                    <td className="py-2.5 px-3 text-center text-slate-400 font-mono text-xs">
                      {idx + 1}
                    </td>
                    <td className="py-2.5 px-3">
                      <input
                        type="text"
                        value={row.item_code}
                        onChange={(e) => handleItemChange(idx, 'item_code', e.target.value)}
                        className="w-full px-2 py-1.5 border rounded text-xs font-mono focus:ring-1 focus:ring-emerald-500 outline-none uppercase"
                        placeholder="ITEM-001"
                      />
                    </td>
                    <td className="py-2.5 px-3">
                      <input
                        type="text"
                        value={row.item_name}
                        onChange={(e) => handleItemChange(idx, 'item_name', e.target.value)}
                        className="w-full px-2 py-1.5 border rounded text-xs focus:ring-1 focus:ring-emerald-500 outline-none"
                        placeholder="Item description"
                      />
                    </td>
                    <td className="py-2.5 px-3">
                      <select
                        value={row.uom}
                        onChange={(e) => handleItemChange(idx, 'uom', e.target.value)}
                        className="w-full px-2 py-1.5 border rounded text-xs bg-white focus:ring-1 focus:ring-emerald-500 outline-none"
                      >
                        <option value="Nos">Nos</option>
                        <option value="Ton">Ton</option>
                        <option value="Kg">Kg</option>
                        <option value="Meter">Meter</option>
                        <option value="Box">Box</option>
                        <option value="Set">Set</option>
                      </select>
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <input
                        type="number"
                        step="any"
                        min="0"
                        value={row.qty}
                        onChange={(e) => handleItemChange(idx, 'qty', e.target.value)}
                        className="w-full px-2 py-1.5 border rounded text-xs text-right font-mono focus:ring-1 focus:ring-emerald-500 outline-none"
                      />
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <input
                        type="number"
                        step="any"
                        min="0"
                        value={row.rate}
                        onChange={(e) => handleItemChange(idx, 'rate', e.target.value)}
                        className="w-full px-2 py-1.5 border rounded text-xs text-right font-mono focus:ring-1 focus:ring-emerald-500 outline-none"
                      />
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-medium text-slate-800">
                      ₹{(Number(row.amount) || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="py-2.5 px-3 text-center">
                      <button
                        type="button"
                        onClick={() => removeItemRow(idx)}
                        className="p-1 hover:bg-rose-50 text-slate-400 hover:text-rose-600 rounded transition"
                        title="Delete Line"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Section 3: Taxes, Summary & Totals */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
            <div className="flex items-center space-x-2 text-slate-900 font-semibold border-b pb-2">
              <Percent className="w-5 h-5 text-emerald-600" />
              <span>Taxes & Duties Breakdown</span>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  GST Applicable Rate
                </label>
                <select
                  value={taxRate}
                  onChange={(e) => setTaxRate(Number(e.target.value))}
                  className="w-full px-3 py-2 border rounded-lg text-sm bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
                >
                  <option value={18}>18% GST (CGST 9% + SGST 9% / IGST 18%)</option>
                  <option value={12}>12% GST (CGST 6% + SGST 6%)</option>
                  <option value={5}>5% GST (CGST 2.5% + SGST 2.5%)</option>
                  <option value={28}>28% GST (Luxury / Heavy Duty)</option>
                  <option value={0}>0% GST (Exempt / SEZ)</option>
                </select>
              </div>

              <div className="p-3 bg-slate-50 border rounded-lg text-xs space-y-1 text-slate-600">
                <div className="flex justify-between">
                  <span>Input Tax Credit (ITC) Eligible:</span>
                  <span className="font-semibold text-emerald-700">Yes (100% GSTR-2B)</span>
                </div>
                <div className="flex justify-between">
                  <span>Calculated GST Tax:</span>
                  <span className="font-mono">₹{taxAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
            <div className="flex items-center space-x-2 text-slate-900 font-semibold border-b pb-2">
              <Calculator className="w-5 h-5 text-emerald-600" />
              <span>Purchase Order Totals</span>
            </div>

            <div className="space-y-2.5 text-sm">
              <div className="flex justify-between text-slate-600">
                <span>Net Total (Excl. Tax):</span>
                <span className="font-mono">₹{netTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Taxes & Charges (GST {taxRate}%):</span>
                <span className="font-mono text-emerald-700">+ ₹{taxAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="border-t pt-2 flex justify-between font-bold text-lg text-slate-900">
                <span>Grand Total:</span>
                <span className="font-mono text-emerald-700">₹{grandTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3 pt-2">
          <button
            type="button"
            onClick={() => onNavigate?.('list', 'purchase_order')}
            className="px-5 py-2.5 border rounded-lg text-slate-700 hover:bg-slate-50 transition"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={() => handleSave(false)}
            disabled={isSubmitting}
            className="px-5 py-2.5 bg-slate-800 hover:bg-slate-900 text-white rounded-lg transition font-medium disabled:opacity-50"
          >
            Save Draft
          </button>
          <button
            type="button"
            onClick={() => handleSave(true)}
            disabled={isSubmitting}
            className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg shadow-sm transition disabled:opacity-50 flex items-center space-x-2"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>{isSubmitting ? 'Submitting to PostgreSQL...' : 'Submit Purchase Order'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
