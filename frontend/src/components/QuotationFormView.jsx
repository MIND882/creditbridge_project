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

export default function QuotationFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('quotation', recordId) : null;
  const isEditing = !!existingRecord;

  useEffect(() => {
    fetchDomainRecords('customer');
  }, []);

  const [quotationTo, setQuotationTo] = useState(existingRecord?.quotation_to || 'Customer');
  const [partyName, setPartyName] = useState(existingRecord?.party_name || 'Acme Technologies Pvt Ltd');
  const [customerName, setCustomerName] = useState(existingRecord?.customer_name || 'Acme Technologies Pvt Ltd');
  const [transactionDate, setTransactionDate] = useState(existingRecord?.transaction_date || new Date().toISOString().slice(0, 10));
  const [validTill, setValidTill] = useState(() => {
    if (existingRecord?.valid_till) return existingRecord.valid_till;
    const d = new Date();
    d.setDate(d.getDate() + 30);
    return d.toISOString().slice(0, 10);
  });
  const [orderType, setOrderType] = useState(existingRecord?.order_type || 'Sales');
  const [currency, setCurrency] = useState(existingRecord?.currency || 'INR');
  const [status, setStatus] = useState(existingRecord?.status || 'Open');

  // Child table items
  const [items, setItems] = useState(() => {
    if (existingRecord?.items && Array.isArray(existingRecord.items) && existingRecord.items.length > 0) {
      return existingRecord.items;
    }
    return [
      {
        id: 'q-item-1',
        item_code: 'CB-PROD-001',
        item_name: 'Precision Fabricated Sheet Metal Enclosure',
        description: 'Commercial quotation for 25 units batch delivery',
        qty: 25,
        uom: 'Nos',
        rate: 21000,
        amount: 525000
      }
    ];
  });

  const [taxCategory, setTaxCategory] = useState(existingRecord?.tax_category || 'In-State GST 18%');
  const [terms, setTerms] = useState(existingRecord?.terms || 'Payment: 30% advance with order, balance on delivery. Validity: 30 days.');
  const [isSubmitting, setIsSubmitting] = useState(false);

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
    const newId = `q-item-${Date.now()}`;
    setItems(prev => [
      ...prev,
      {
        id: newId,
        item_code: `ITEM-${Math.floor(100 + Math.random() * 900)}`,
        item_name: 'Custom Fabricated Component',
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
      onShowToast?.('At least one item is required in quotation', 'error');
      return;
    }
    setItems(prev => prev.filter(item => item.id !== id));
  };

  const calculations = useMemo(() => {
    const netTotal = items.reduce((sum, item) => sum + (Number(item.amount) || 0), 0);
    const totalQty = items.reduce((sum, item) => sum + (Number(item.qty) || 0), 0);

    let taxes = 0;
    if (taxCategory.includes('18%')) {
      taxes = Math.round(netTotal * 0.18 * 100) / 100;
    }
    const grandTotal = Math.round(netTotal + taxes);

    return { netTotal, totalQty, taxes, grandTotal };
  }, [items, taxCategory]);

  const handleSave = async (submitStatus = 'Open') => {
    setIsSubmitting(true);
    const recordName = existingRecord?.name || `QTN-2026-${Math.floor(10000 + Math.random() * 90000)}`;

    const payload = {
      name: recordName,
      title: `${partyName} - ₹${calculations.grandTotal.toLocaleString('en-IN')}`,
      quotation_to: quotationTo,
      party_name: partyName,
      customer_name: customerName,
      transaction_date: transactionDate,
      valid_till: validTill,
      order_type: orderType,
      currency,
      status: submitStatus,
      net_total: calculations.netTotal,
      total_taxes_and_charges: calculations.taxes,
      grand_total: calculations.grandTotal,
      rounded_total: calculations.grandTotal,
      terms,
      items
    };

    try {
      const res = await fetch('/api/selling/quotation', {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(() => null);

      if (res && res.ok) {
        onShowToast?.(`Quotation ${recordName} saved & synced to PostgreSQL!`);
      } else {
        if (isEditing) updateRecord('quotation', recordId, payload);
        else addRecord('quotation', payload);
        onShowToast?.(`Quotation ${recordName} saved!`);
      }

      onNavigate({ type: 'list', domain: 'quotation', module: 'Selling' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Selling • Quotation</span>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">{isEditing ? `Edit Quotation: ${existingRecord?.name}` : 'New Commercial Quotation'}</h1>
        </div>

        <div className="flex items-center gap-2.5">
          <button type="button" onClick={() => onNavigate({ type: 'list', domain: 'quotation', module: 'Selling' })} className="px-4 py-2 border border-slate-200 text-slate-600 text-xs rounded-xl">Cancel</button>
          <button type="button" onClick={() => handleSave('Draft')} className="px-4 py-2 bg-slate-100 text-slate-800 text-xs font-semibold rounded-xl">Save Draft</button>
          <button type="button" onClick={() => handleSave('Open')} className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl">Send Quotation</button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900 border-b pb-2">Client & Proposal Schedule</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-700">Quotation To</label>
                <select value={quotationTo} onChange={(e) => setQuotationTo(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs">
                  <option value="Customer">Customer</option>
                  <option value="Lead">Lead</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700">Client / Party Name *</label>
                <input type="text" value={partyName} onChange={(e) => { setPartyName(e.target.value); setCustomerName(e.target.value); }} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700">Quotation Date</label>
                <input type="date" value={transactionDate} onChange={(e) => setTransactionDate(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700">Valid Till Date</label>
                <input type="date" value={validTill} onChange={(e) => setValidTill(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
              </div>
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="flex justify-between items-center border-b pb-2">
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900">Quoted Line Items</h2>
              <button type="button" onClick={handleAddItem} className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-lg">+ Add Row</button>
            </div>

            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 border-b">
                <tr><th className="p-2">Item</th><th className="p-2 w-20 text-right">Qty</th><th className="p-2 w-28 text-right">Rate (₹)</th><th className="p-2 w-32 text-right">Amount (₹)</th><th className="p-2 w-10"></th></tr>
              </thead>
              <tbody className="divide-y">
                {items.map(item => (
                  <tr key={item.id}>
                    <td className="p-2">
                      <input type="text" value={item.item_name} onChange={(e) => handleItemChange(item.id, 'item_name', e.target.value)} className="w-full font-medium border-0 focus:outline-none" />
                      <div className="text-[10px] text-slate-400">{item.item_code}</div>
                    </td>
                    <td className="p-2 text-right"><input type="number" value={item.qty} onChange={(e) => handleItemChange(item.id, 'qty', e.target.value)} className="w-16 border rounded p-1 text-right" /></td>
                    <td className="p-2 text-right"><input type="number" value={item.rate} onChange={(e) => handleItemChange(item.id, 'rate', e.target.value)} className="w-24 border rounded p-1 text-right font-mono" /></td>
                    <td className="p-2 text-right font-mono font-bold">₹{(Number(item.amount) || 0).toLocaleString('en-IN')}</td>
                    <td className="p-2 text-center"><button type="button" onClick={() => handleRemoveItem(item.id)} className="text-slate-300 hover:text-rose-600"><Trash2 className="w-3.5 h-3.5" /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div>
          <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg space-y-4 sticky top-6 border border-slate-800">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-300">Quotation Summary</h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between"><span>Net Total</span><span className="font-mono">₹{calculations.netTotal.toLocaleString('en-IN')}</span></div>
              <div className="flex justify-between text-blue-400"><span>Taxes (GST 18%)</span><span className="font-mono">+₹{calculations.taxes.toLocaleString('en-IN')}</span></div>
              <div className="border-t border-slate-800 pt-2 flex justify-between text-sm font-bold"><span>Total Quote</span><span className="text-emerald-400">₹{calculations.grandTotal.toLocaleString('en-IN')}</span></div>
            </div>
            <button type="button" onClick={() => handleSave('Open')} className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs uppercase rounded-xl">Submit Quotation</button>
          </div>
        </div>
      </div>
    </div>
  );
}
