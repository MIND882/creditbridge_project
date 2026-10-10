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

export default function SalesOrderFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('sales_order', recordId) : null;
  const isEditing = !!existingRecord;

  useEffect(() => {
    fetchDomainRecords('customer');
  }, []);

  const customers = getDomainRecords('customer') || [];

  const customerList = [
    { name: 'Acme Technologies Pvt Ltd', contact: 'Anil Mehta', phone: '+91 98200 12345', email: 'anil@acme.in', gstin: '27AABCA1234F1Z5', address: 'Plot 44, MIDC Industrial Area, Andheri East, Mumbai 400093' },
    { name: 'Bharat Retailers Ltd', contact: 'Pooja Sharma', phone: '+91 98111 23456', email: 'pooja@bharatretail.in', gstin: '07AABCB5678G1Z2', address: 'Shop 12, Phoenix Marketcity, Kurla West, Mumbai 400070' },
    { name: 'Zenith Logistics Corp', contact: 'Karan Malhotra', phone: '+91 98333 34567', email: 'karan@zenithlogistics.com', gstin: '27AABCZ9988H1Z1', address: 'Warehouse 8, Nhava Sheva Port Road, Navi Mumbai 410206' }
  ];

  // Primary State
  const [customer, setCustomer] = useState(existingRecord?.customer || 'Acme Technologies Pvt Ltd');
  const [customerName, setCustomerName] = useState(existingRecord?.customer_name || 'Acme Technologies Pvt Ltd');
  const [orderType, setOrderType] = useState(existingRecord?.order_type || 'Sales');
  const [transactionDate, setTransactionDate] = useState(existingRecord?.transaction_date || new Date().toISOString().slice(0, 10));
  const [deliveryDate, setDeliveryDate] = useState(() => {
    if (existingRecord?.delivery_date) return existingRecord.delivery_date;
    const d = new Date();
    d.setDate(d.getDate() + 15);
    return d.toISOString().slice(0, 10);
  });
  const [poNo, setPoNo] = useState(existingRecord?.po_no || `PO-CLIENT-${Math.floor(1000 + Math.random() * 9000)}`);
  const [poDate, setPoDate] = useState(existingRecord?.po_date || new Date().toISOString().slice(0, 10));
  const [currency, setCurrency] = useState(existingRecord?.currency || 'INR');
  const [status, setStatus] = useState(existingRecord?.status || 'Draft');

  // Customer Address & Contact
  const [customerAddress, setCustomerAddress] = useState(
    existingRecord?.customer_address || 'Plot 44, MIDC Industrial Area, Andheri East, Mumbai 400093'
  );
  const [contactPerson, setContactPerson] = useState(existingRecord?.contact_person || 'Anil Mehta');
  const [contactMobile, setContactMobile] = useState(existingRecord?.contact_mobile || '+91 98200 12345');
  const [contactEmail, setContactEmail] = useState(existingRecord?.contact_email || 'anil@acme.in');
  const [taxId, setTaxId] = useState(existingRecord?.tax_id || '27AABCA1234F1Z5');

  // Line Items Child Table
  const [items, setItems] = useState(() => {
    if (existingRecord?.items && Array.isArray(existingRecord.items) && existingRecord.items.length > 0) {
      return existingRecord.items;
    }
    return [
      {
        id: 'item-1',
        item_code: 'CB-PROD-001',
        item_name: 'Precision Fabricated Sheet Metal Enclosure',
        description: '2mm Galvanized finish per client manufacturing drawing',
        qty: 10,
        uom: 'Nos',
        rate: 22500,
        amount: 225000
      },
      {
        id: 'item-2',
        item_code: 'CB-SERV-010',
        item_name: 'Tooling & Laser Engraving Batch',
        description: 'Custom laser serial numbering & UV powder coating',
        qty: 10,
        uom: 'Nos',
        rate: 5000,
        amount: 50000
      }
    ];
  });

  // Taxes
  const [taxCategory, setTaxCategory] = useState(existingRecord?.tax_category || 'In-State GST 18%');
  const [paymentTerms, setPaymentTerms] = useState(existingRecord?.payment_terms || '50% Advance with PO, 50% against Delivery');
  const [remarks, setRemarks] = useState(existingRecord?.remarks || 'Priority dispatch schedule requested by client.');

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCustomerSelect = (name) => {
    setCustomer(name);
    setCustomerName(name);
    const found = customerList.find(c => c.name === name);
    if (found) {
      setContactPerson(found.contact);
      setContactMobile(found.phone);
      setContactEmail(found.email);
      setCustomerAddress(found.address);
      setTaxId(found.gstin);
    }
  };

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
        item_name: 'Standard Commercial Assembly',
        description: 'Standard product specifications',
        qty: 1,
        uom: 'Nos',
        rate: 15000,
        amount: 15000
      }
    ]);
  };

  const handleRemoveItem = (id) => {
    if (items.length <= 1) {
      onShowToast?.('At least one item row is required in Sales Order', 'error');
      return;
    }
    setItems(prev => prev.filter(item => item.id !== id));
  };

  // Calculations
  const calculations = useMemo(() => {
    const netTotal = items.reduce((sum, item) => sum + (Number(item.amount) || 0), 0);
    const totalQty = items.reduce((sum, item) => sum + (Number(item.qty) || 0), 0);

    let cgst = 0, sgst = 0, igst = 0;
    if (taxCategory === 'In-State GST 18%') {
      cgst = Math.round(netTotal * 0.09 * 100) / 100;
      sgst = Math.round(netTotal * 0.09 * 100) / 100;
    } else if (taxCategory === 'Out-of-State IGST 18%') {
      igst = Math.round(netTotal * 0.18 * 100) / 100;
    }

    const totalTaxes = cgst + sgst + igst;
    const grandTotal = Math.round(netTotal + totalTaxes);

    return {
      netTotal,
      totalQty,
      cgst,
      sgst,
      igst,
      totalTaxes,
      grandTotal
    };
  }, [items, taxCategory]);

  const handleSave = async (submitStatus = 'Draft') => {
    if (!customer) {
      onShowToast?.('Please specify a Customer', 'error');
      return;
    }
    if (items.length === 0) {
      onShowToast?.('At least one item is required', 'error');
      return;
    }

    setIsSubmitting(true);
    const recordName = existingRecord?.name || `SO-2026-${Math.floor(10000 + Math.random() * 90000)}`;

    const payload = {
      name: recordName,
      title: `${customer} - ₹${calculations.grandTotal.toLocaleString('en-IN')}`,
      customer,
      customer_name: customerName,
      order_type: orderType,
      transaction_date: transactionDate,
      delivery_date: deliveryDate,
      po_no: poNo,
      po_date: poDate,
      currency,
      status: submitStatus === 'Submitted' ? 'To Deliver and Bill' : 'Draft',
      docstatus: submitStatus === 'Submitted' ? 1 : 0,

      customer_address: customerAddress,
      contact_person: contactPerson,
      contact_mobile: contactMobile,
      contact_email: contactEmail,
      tax_id: taxId,

      net_total: calculations.netTotal,
      total_taxes_and_charges: calculations.totalTaxes,
      grand_total: calculations.grandTotal,
      rounded_total: calculations.grandTotal,

      payment_terms: paymentTerms,
      remarks,
      items
    };

    try {
      const res = await fetch('/api/selling/sales-order', {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(() => null);

      if (res && res.ok) {
        onShowToast?.(`Sales Order ${recordName} saved & synced to PostgreSQL!`);
      } else {
        if (isEditing) {
          updateRecord('sales_order', recordId, payload);
          onShowToast?.(`Sales Order ${recordName} updated in store!`);
        } else {
          addRecord('sales_order', payload);
          onShowToast?.(`Sales Order ${recordName} created!`);
        }
      }

      onNavigate({ type: 'list', domain: 'sales_order', module: 'Selling' });
    } catch (err) {
      console.error(err);
      onShowToast?.('Failed to save Sales Order', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      {/* Header Bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate({ type: 'list', domain: 'sales_order', module: 'Selling' })}
              className="p-1 -ml-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Selling • Sales Order
            </span>
            <span className="text-slate-300">•</span>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
              status === 'To Deliver and Bill' || status === 'Submitted'
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : 'bg-blue-50 text-blue-700 border border-blue-200'
            }`}>
              {status}
            </span>
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            {isEditing ? `Edit Sales Order: ${existingRecord?.name}` : 'New Sales Order'}
          </h1>
          <p className="text-[12.5px] text-slate-500">
            Record customer purchase commitment, schedule delivery, and initiate manufacturing/fulfillment per ERPNext.
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'list', domain: 'sales_order', module: 'Selling' })}
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
            className="flex items-center gap-1.5 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-[13px] font-semibold rounded-xl transition-all shadow-xs"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Confirm & Submit Order</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (2 Cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section 1: Customer & Dates */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-100 pb-2">
              Customer & Order Schedule
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Customer <span className="text-rose-500 font-bold">*</span>
                </label>
                <input
                  type="text"
                  list="so-customers"
                  value={customer}
                  onChange={(e) => handleCustomerSelect(e.target.value)}
                  placeholder="Select customer..."
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white text-slate-900"
                />
                <datalist id="so-customers">
                  {customerList.map(c => <option key={c.name} value={c.name} />)}
                </datalist>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Order Type</label>
                <select
                  value={orderType}
                  onChange={(e) => setOrderType(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                >
                  <option value="Sales">Sales</option>
                  <option value="Maintenance">Maintenance</option>
                  <option value="Shopping Cart">Shopping Cart</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Order Date</label>
                <input
                  type="date"
                  value={transactionDate}
                  onChange={(e) => setTransactionDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Delivery Due Date</label>
                <input
                  type="date"
                  value={deliveryDate}
                  onChange={(e) => setDeliveryDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Customer PO Number</label>
                <input
                  type="text"
                  value={poNo}
                  onChange={(e) => setPoNo(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Customer PO Date</label>
                <input
                  type="date"
                  value={poDate}
                  onChange={(e) => setPoDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* Section 2: Interactive Line Items Child Table */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                Sales Order Items Table
              </h2>
              <button
                type="button"
                onClick={handleAddItem}
                className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-lg hover:bg-blue-100"
              >
                + Add Item Row
              </button>
            </div>

            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3">Item Code & Name</th>
                    <th className="py-2.5 px-3">Description</th>
                    <th className="py-2.5 px-3 w-20 text-right">Qty</th>
                    <th className="py-2.5 px-3 w-20">UOM</th>
                    <th className="py-2.5 px-3 w-28 text-right">Rate (₹)</th>
                    <th className="py-2.5 px-3 w-32 text-right">Amount (₹)</th>
                    <th className="py-2.5 px-2 w-10 text-center"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {items.map((item, idx) => (
                    <tr key={item.id} className="hover:bg-slate-50/50">
                      <td className="py-2 px-3">
                        <input
                          type="text"
                          value={item.item_name}
                          onChange={(e) => handleItemChange(item.id, 'item_name', e.target.value)}
                          className="w-full font-medium text-slate-900 border-0 focus:outline-none"
                        />
                        <div className="text-[10px] font-mono text-slate-400">{item.item_code}</div>
                      </td>
                      <td className="py-2 px-3">
                        <input
                          type="text"
                          value={item.description}
                          onChange={(e) => handleItemChange(item.id, 'description', e.target.value)}
                          className="w-full text-slate-600 border-0 focus:outline-none"
                        />
                      </td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          value={item.qty}
                          onChange={(e) => handleItemChange(item.id, 'qty', e.target.value)}
                          className="w-16 text-right border border-slate-200 rounded p-1 font-medium"
                        />
                      </td>
                      <td className="py-2 px-3 text-slate-600">{item.uom}</td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          value={item.rate}
                          onChange={(e) => handleItemChange(item.id, 'rate', e.target.value)}
                          className="w-24 text-right border border-slate-200 rounded p-1 font-mono"
                        />
                      </td>
                      <td className="py-2 px-3 text-right font-mono font-bold text-slate-900">
                        ₹{(Number(item.amount) || 0).toLocaleString('en-IN')}
                      </td>
                      <td className="py-2 px-2 text-center">
                        <button
                          type="button"
                          onClick={() => handleRemoveItem(item.id)}
                          className="text-slate-300 hover:text-rose-600"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
              <span>Total Qty: <strong className="text-slate-800">{calculations.totalQty} Units</strong></span>
              <span>Net Total: <strong className="font-mono text-slate-900">₹{calculations.netTotal.toLocaleString('en-IN')}</strong></span>
            </div>
          </div>

          {/* Section 3: Tax & Commercial Terms */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-100 pb-2">
              GST Taxes & Payment Terms
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">GST Tax Category</label>
                <select
                  value={taxCategory}
                  onChange={(e) => setTaxCategory(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                >
                  <option value="In-State GST 18%">In-State GST 18% (CGST 9% + SGST 9%)</option>
                  <option value="Out-of-State IGST 18%">Out-of-State IGST 18%</option>
                  <option value="Export / Zero Rated">Export / Zero Rated (0%)</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Payment Terms</label>
                <input
                  type="text"
                  value={paymentTerms}
                  onChange={(e) => setPaymentTerms(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="sm:col-span-2 space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Dispatch / Production Instructions</label>
                <input
                  type="text"
                  value={remarks}
                  onChange={(e) => setRemarks(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (1 Col) - Financial Summary Card */}
        <div>
          <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg space-y-5 sticky top-6 border border-slate-800">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-300 border-b border-slate-800 pb-3">
              Sales Order Valuation
            </h3>

            <div className="space-y-2.5 text-xs">
              <div className="flex justify-between text-slate-300">
                <span>Net Order Total</span>
                <span className="font-mono font-medium text-white">₹{calculations.netTotal.toLocaleString('en-IN')}</span>
              </div>

              {calculations.cgst > 0 && (
                <div className="flex justify-between text-slate-400 pl-2">
                  <span>Output CGST (9%)</span>
                  <span className="font-mono text-blue-400">+₹{calculations.cgst.toLocaleString('en-IN')}</span>
                </div>
              )}

              {calculations.sgst > 0 && (
                <div className="flex justify-between text-slate-400 pl-2">
                  <span>Output SGST (9%)</span>
                  <span className="font-mono text-blue-400">+₹{calculations.sgst.toLocaleString('en-IN')}</span>
                </div>
              )}

              {calculations.igst > 0 && (
                <div className="flex justify-between text-slate-400 pl-2">
                  <span>Output IGST (18%)</span>
                  <span className="font-mono text-blue-400">+₹{calculations.igst.toLocaleString('en-IN')}</span>
                </div>
              )}

              <div className="border-t border-slate-800 pt-3 flex justify-between text-sm font-bold text-white">
                <span>Grand Total</span>
                <span className="font-mono text-lg text-emerald-400">₹{calculations.grandTotal.toLocaleString('en-IN')}</span>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="button"
                onClick={() => handleSave('Submitted')}
                disabled={isSubmitting}
                className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold text-xs uppercase tracking-wider rounded-xl transition-all shadow-md flex items-center justify-center gap-2"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Confirm Sales Order</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
