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
  ChevronDown,
  ArrowRightLeft,
  Banknote
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function PaymentEntryFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('payment_entry', recordId) : null;
  const isEditing = !!existingRecord;

  // Auto-fetch related domains for link choices
  useEffect(() => {
    fetchDomainRecords('account');
    fetchDomainRecords('cost_center');
    fetchDomainRecords('sales_invoice');
    fetchDomainRecords('purchase_invoice');
  }, []);

  const accounts = getDomainRecords('account');
  const salesInvoices = getDomainRecords('sales_invoice');
  const purchaseInvoices = getDomainRecords('purchase_invoice');

  // Primary State
  const [paymentType, setPaymentType] = useState(existingRecord?.payment_type || 'Receive');
  const [partyType, setPartyType] = useState(() => {
    if (existingRecord?.party_type) return existingRecord.party_type;
    return paymentType === 'Pay' ? 'Supplier' : 'Customer';
  });

  const [party, setParty] = useState(existingRecord?.party || 'Acme Technologies Pvt Ltd');
  const [partyName, setPartyName] = useState(existingRecord?.party_name || 'Acme Technologies Pvt Ltd');
  const [postingDate, setPostingDate] = useState(existingRecord?.posting_date || new Date().toISOString().slice(0, 10));
  const [namingSeries, setNamingSeries] = useState(existingRecord?.naming_series || 'ACC-PAY-.YYYY.-');
  const [status, setStatus] = useState(existingRecord?.status || 'Draft');

  // Bank & Cash Accounts
  const [paidFrom, setPaidFrom] = useState(() => {
    if (existingRecord?.paid_from) return existingRecord.paid_from;
    return paymentType === 'Receive' ? 'Debtors - 1310' : 'HDFC Bank Ltd - 1001';
  });

  const [paidTo, setPaidTo] = useState(() => {
    if (existingRecord?.paid_to) return existingRecord.paid_to;
    return paymentType === 'Receive' ? 'HDFC Bank Ltd - 1001' : 'Creditors - 2110';
  });

  const [paidAmount, setPaidAmount] = useState(Number(existingRecord?.paid_amount) || 50000);
  const [receivedAmount, setReceivedAmount] = useState(Number(existingRecord?.received_amount) || 50000);

  // References Child Table (Allocated Invoices)
  const [references, setReferences] = useState(() => {
    if (existingRecord?.references && Array.isArray(existingRecord.references) && existingRecord.references.length > 0) {
      return existingRecord.references;
    }
    return [
      {
        id: 'ref-1',
        reference_doctype: paymentType === 'Pay' ? 'Purchase Invoice' : 'Sales Invoice',
        reference_name: 'ACC-SINV-2026-00000001',
        total_amount: 150000,
        outstanding_amount: 100000,
        allocated_amount: 50000
      }
    ];
  });

  // Transaction details
  const [modeOfPayment, setModeOfPayment] = useState(existingRecord?.mode_of_payment || 'Bank Transfer / RTGS');
  const [referenceNo, setReferenceNo] = useState(existingRecord?.reference_no || `UTR-${Math.floor(100000 + Math.random() * 900000)}`);
  const [referenceDate, setReferenceDate] = useState(existingRecord?.reference_date || new Date().toISOString().slice(0, 10));
  const [remarks, setRemarks] = useState(existingRecord?.remarks || 'Payment cleared against invoice ledger balance.');

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Update partyType when paymentType changes
  const handlePaymentTypeChange = (type) => {
    setPaymentType(type);
    if (type === 'Receive') {
      setPartyType('Customer');
      setPaidFrom('Debtors - 1310');
      setPaidTo('HDFC Bank Ltd - 1001');
    } else if (type === 'Pay') {
      setPartyType('Supplier');
      setPaidFrom('HDFC Bank Ltd - 1001');
      setPaidTo('Creditors - 2110');
    } else {
      setPartyType('Internal');
      setPaidFrom('HDFC Bank Ltd - 1001');
      setPaidTo('Cash in Hand - 1002');
    }
  };

  // References Handlers
  const handleReferenceChange = (id, field, value) => {
    setReferences(prev => prev.map(ref => {
      if (ref.id === id) {
        return { ...ref, [field]: value };
      }
      return ref;
    }));
  };

  const handleAddReference = () => {
    const newId = `ref-${Date.now()}`;
    setReferences(prev => [
      ...prev,
      {
        id: newId,
        reference_doctype: paymentType === 'Pay' ? 'Purchase Invoice' : 'Sales Invoice',
        reference_name: `ACC-${paymentType === 'Pay' ? 'PINV' : 'SINV'}-2026-${Math.floor(1000 + Math.random() * 9000)}`,
        total_amount: 50000,
        outstanding_amount: 50000,
        allocated_amount: 0
      }
    ]);
  };

  const handleRemoveReference = (id) => {
    setReferences(prev => prev.filter(ref => ref.id !== id));
  };

  // Total Allocated
  const totalAllocated = useMemo(() => {
    return references.reduce((sum, ref) => sum + (Number(ref.allocated_amount) || 0), 0);
  }, [references]);

  const unallocatedAmount = useMemo(() => {
    return Math.max(0, paidAmount - totalAllocated);
  }, [paidAmount, totalAllocated]);

  // Handle Save / Submit
  const handleSave = async (submitStatus = 'Draft') => {
    if (paidAmount <= 0) {
      onShowToast?.('Paid Amount must be greater than zero', 'error');
      return;
    }

    setIsSubmitting(true);

    const recordName = existingRecord?.name || `ACC-PAY-2026-${Math.floor(10000 + Math.random() * 90000)}`;

    const payload = {
      name: recordName,
      title: `${paymentType} from ${party}`,
      payment_type: paymentType,
      party_type: partyType,
      party,
      party_name: partyName,
      posting_date: postingDate,
      naming_series: namingSeries,
      status: submitStatus === 'Submitted' ? 'Submitted' : 'Draft',
      docstatus: submitStatus === 'Submitted' ? 1 : 0,

      paid_from: paidFrom,
      paid_to: paidTo,
      paid_amount: paidAmount,
      received_amount: receivedAmount,
      total_allocated_amount: totalAllocated,
      unallocated_amount: unallocatedAmount,

      mode_of_payment: modeOfPayment,
      reference_no: referenceNo,
      reference_date: referenceDate,
      remarks,
      references
    };

    try {
      const res = await fetch('/v1/payment-entry', {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(() => null);

      if (res && res.ok) {
        onShowToast?.(`Payment Entry ${recordName} saved & ledger updated!`);
      } else {
        if (isEditing) {
          updateRecord('payment_entry', recordId, payload);
          onShowToast?.(`Payment Entry ${recordName} updated in store!`);
        } else {
          addRecord('payment_entry', payload);
          onShowToast?.(`Payment Entry ${recordName} created!`);
        }
      }

      onNavigate({ type: 'list', domain: 'payment_entry' });
    } catch (err) {
      console.error(err);
      onShowToast?.('Failed to save Payment Entry', 'error');
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
              onClick={() => onNavigate({ type: 'list', domain: 'payment_entry' })}
              className="p-1 -ml-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Treasury & Cash Flow • Payment Entry
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
            {isEditing ? `Edit Payment Entry: ${existingRecord?.name}` : 'New Payment Entry'}
          </h1>
          <p className="text-[12.5px] text-slate-500">
            Post money received from customers, disbursements to vendors, or internal bank-to-bank ledger transfers.
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'list', domain: 'payment_entry' })}
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
            <span>Submit to General Ledger</span>
          </button>
        </div>
      </div>

      {/* Payment Type Selection Tabs */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-2xs flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => handlePaymentTypeChange('Receive')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs transition-all ${
            paymentType === 'Receive'
              ? 'bg-emerald-600 text-white shadow-xs'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
          }`}
        >
          <Banknote className="w-4 h-4" />
          <span>Receive (From Customer)</span>
        </button>

        <button
          type="button"
          onClick={() => handlePaymentTypeChange('Pay')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs transition-all ${
            paymentType === 'Pay'
              ? 'bg-rose-600 text-white shadow-xs'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
          }`}
        >
          <CreditCard className="w-4 h-4" />
          <span>Pay (To Supplier / Vendor)</span>
        </button>

        <button
          type="button"
          onClick={() => handlePaymentTypeChange('Internal Transfer')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs transition-all ${
            paymentType === 'Internal Transfer'
              ? 'bg-indigo-600 text-white shadow-xs'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
          }`}
        >
          <ArrowRightLeft className="w-4 h-4" />
          <span>Internal Transfer (Bank to Bank / Cash)</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (2 Cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section 1: Party & Posting */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-indigo-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Party & Payment Information
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 1 of 4</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Party Type
                </label>
                <select
                  value={partyType}
                  onChange={(e) => setPartyType(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                >
                  <option value="Customer">Customer</option>
                  <option value="Supplier">Supplier</option>
                  <option value="Employee">Employee</option>
                  <option value="Shareholder">Shareholder</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Party Name / Account <span className="text-rose-500 font-bold">*</span>
                </label>
                <input
                  type="text"
                  value={party}
                  onChange={(e) => { setParty(e.target.value); setPartyName(e.target.value); }}
                  placeholder="e.g. Acme Technologies Pvt Ltd"
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
                  Naming Series
                </label>
                <select
                  value={namingSeries}
                  onChange={(e) => setNamingSeries(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                >
                  <option value="ACC-PAY-.YYYY.-">ACC-PAY-.YYYY.-</option>
                  <option value="PAY-RET-.YYYY.-">PAY-RET-.YYYY.-</option>
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Accounts & Amounts */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Banknote className="w-4 h-4 text-emerald-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  General Ledger Accounts & Paid Amount
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 2 of 4</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Account Paid From (Credit Source)
                </label>
                <input
                  type="text"
                  value={paidFrom}
                  onChange={(e) => setPaidFrom(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] font-medium bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Account Paid To (Debit Destination)
                </label>
                <input
                  type="text"
                  value={paidTo}
                  onChange={(e) => setPaidTo(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] font-medium bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Paid Amount (₹) <span className="text-rose-500 font-bold">*</span>
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs font-semibold">₹</span>
                  <input
                    type="number"
                    value={paidAmount}
                    onChange={(e) => {
                      const v = Number(e.target.value);
                      setPaidAmount(v);
                      setReceivedAmount(v);
                    }}
                    className="w-full pl-8 pr-3 py-2 text-[14px] font-mono font-bold bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Received Amount (₹)
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs font-semibold">₹</span>
                  <input
                    type="number"
                    value={receivedAmount}
                    onChange={(e) => setReceivedAmount(Number(e.target.value))}
                    className="w-full pl-8 pr-3 py-2 text-[14px] font-mono bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: References Child Table (Allocated Invoices) */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-violet-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Payment Allocation / Invoice References Table
                </h2>
              </div>
              <button
                type="button"
                onClick={handleAddReference}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-lg transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Invoice</span>
              </button>
            </div>

            {/* Desktop Table View */}
            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3 w-10 text-center">#</th>
                    <th className="py-2.5 px-3 min-w-[140px]">Voucher Type</th>
                    <th className="py-2.5 px-3 min-w-[180px]">Voucher No</th>
                    <th className="py-2.5 px-3 w-28 text-right">Invoice Total</th>
                    <th className="py-2.5 px-3 w-28 text-right">Outstanding</th>
                    <th className="py-2.5 px-3 w-32 text-right">Allocated (₹)</th>
                    <th className="py-2.5 px-2 w-10 text-center"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-sans">
                  {references.map((ref, idx) => (
                    <tr key={ref.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="py-2 px-3 text-center text-slate-400 font-mono">{idx + 1}</td>
                      <td className="py-2 px-3">
                        <select
                          value={ref.reference_doctype}
                          onChange={(e) => handleReferenceChange(ref.id, 'reference_doctype', e.target.value)}
                          className="w-full bg-slate-50 border border-slate-200 rounded p-1 text-slate-800"
                        >
                          <option value="Sales Invoice">Sales Invoice</option>
                          <option value="Purchase Invoice">Purchase Invoice</option>
                          <option value="Journal Entry">Journal Entry</option>
                        </select>
                      </td>
                      <td className="py-2 px-3">
                        <input
                          type="text"
                          value={ref.reference_name}
                          onChange={(e) => handleReferenceChange(ref.id, 'reference_name', e.target.value)}
                          className="w-full font-mono text-slate-900 bg-transparent border-0 border-b border-transparent focus:border-indigo-500 focus:bg-white focus:outline-none p-1 rounded"
                        />
                      </td>
                      <td className="py-2 px-3 text-right font-mono text-slate-500">
                        ₹{(Number(ref.total_amount) || 0).toLocaleString('en-IN')}
                      </td>
                      <td className="py-2 px-3 text-right font-mono text-rose-600 font-medium">
                        ₹{(Number(ref.outstanding_amount) || 0).toLocaleString('en-IN')}
                      </td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          value={ref.allocated_amount}
                          onChange={(e) => handleReferenceChange(ref.id, 'allocated_amount', Number(e.target.value))}
                          className="w-28 text-right font-mono font-bold text-slate-900 bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:outline-none p-1.5 rounded"
                        />
                      </td>
                      <td className="py-2 px-2 text-center">
                        <button
                          type="button"
                          onClick={() => handleRemoveReference(ref.id)}
                          className="text-slate-300 hover:text-rose-600 p-1 rounded transition-colors"
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
                onClick={handleAddReference}
                className="flex items-center gap-1.5 px-3 py-1.5 border border-dashed border-slate-300 hover:border-indigo-500 hover:text-indigo-600 text-slate-600 text-xs font-semibold rounded-lg transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>+ Add Invoice Reference</span>
              </button>
              <div className="text-xs text-slate-500">
                Total Allocated: <span className="font-mono font-bold text-slate-900">₹{totalAllocated.toLocaleString('en-IN')}</span>
              </div>
            </div>
          </div>

          {/* Section 4: Transaction & Reference Details */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Cheque / Transaction Reference & Remarks
                </h2>
              </div>
              <span className="text-[11px] font-semibold text-slate-400">Section 4 of 4</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Mode of Payment
                </label>
                <select
                  value={modeOfPayment}
                  onChange={(e) => setModeOfPayment(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                >
                  <option value="Bank Transfer / RTGS">Bank Transfer / RTGS</option>
                  <option value="UPI / QR Code">UPI / QR Code</option>
                  <option value="Cheque">Cheque</option>
                  <option value="Cash">Cash</option>
                  <option value="Demand Draft">Demand Draft</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Cheque / UTR Ref No
                </label>
                <input
                  type="text"
                  value={referenceNo}
                  onChange={(e) => setReferenceNo(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] font-mono bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Reference Date
                </label>
                <input
                  type="date"
                  value={referenceDate}
                  onChange={(e) => setReferenceDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
                />
              </div>

              <div className="sm:col-span-3 space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">
                  Payment Remarks / Narration
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

        {/* Right Column (1 Col) - Allocation Card */}
        <div className="space-y-6">
          <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg border border-slate-800 space-y-6 sticky top-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center gap-2">
                <Calculator className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold uppercase tracking-widest text-slate-300">
                  Payment Reconciliation
                </h3>
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                INR (₹)
              </span>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between text-slate-300">
                <span>Total Paid Amount</span>
                <span className="font-mono font-bold text-white text-sm">
                  ₹{paidAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              <div className="flex items-center justify-between text-slate-400">
                <span>Total Allocated to Invoices</span>
                <span className="font-mono text-emerald-400">
                  ₹{totalAllocated.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              <div className="border-t border-slate-800 pt-3 flex items-center justify-between text-xs">
                <span>Unallocated / Advance</span>
                <span className={`font-mono font-semibold ${unallocatedAmount > 0 ? 'text-amber-400' : 'text-slate-400'}`}>
                  ₹{unallocatedAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </span>
              </div>

              <div className="p-3 bg-slate-800/80 rounded-xl space-y-1">
                <div className="text-[11px] font-semibold text-slate-300">Allocation Status:</div>
                <div className="text-[11px] text-slate-400">
                  {unallocatedAmount === 0
                    ? '100% of payment amount is allocated to pending invoices.'
                    : `₹${unallocatedAmount.toLocaleString('en-IN')} will remain as an Advance on Account.`}
                </div>
              </div>
            </div>

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
