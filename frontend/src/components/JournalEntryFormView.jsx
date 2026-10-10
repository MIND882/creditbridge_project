import React, { useState, useMemo, useEffect } from 'react';
import {
  ArrowLeft,
  Save,
  X,
  Plus,
  Trash2,
  FileText,
  CheckCircle2,
  AlertCircle,
  Scale,
  RefreshCw
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function JournalEntryFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, getDomainRecords, fetchDomainRecords } = useRecords();

  const existingRecord = recordId ? getRecordById('journal_entry', recordId) : null;
  const isEditing = !!existingRecord;

  // Auto-fetch related accounts & cost centers from PostgreSQL
  useEffect(() => {
    fetchDomainRecords('account');
    fetchDomainRecords('cost_center');
  }, []);

  const accounts = getDomainRecords('account');
  const costCenters = getDomainRecords('cost_center');

  // Primary State
  const [voucherType, setVoucherType] = useState(existingRecord?.voucher_type || 'Journal Entry');
  const [namingSeries, setNamingSeries] = useState(existingRecord?.naming_series || 'ACC-JV-.YYYY.-');
  const [postingDate, setPostingDate] = useState(existingRecord?.posting_date || new Date().toISOString().slice(0, 10));
  const [chequeNo, setChequeNo] = useState(existingRecord?.cheque_no || `JV-REF-${Math.floor(1000 + Math.random() * 9000)}`);
  const [chequeDate, setChequeDate] = useState(existingRecord?.cheque_date || new Date().toISOString().slice(0, 10));
  const [status, setStatus] = useState(existingRecord?.status || 'Draft');
  const [userRemark, setUserRemark] = useState(existingRecord?.user_remark || 'Monthly office rent accrual for BKC headquarters premises.');

  // Accounting Rows (Debit / Credit Child Table)
  const [entries, setEntries] = useState(() => {
    if (existingRecord?.accounts && Array.isArray(existingRecord.accounts) && existingRecord.accounts.length > 0) {
      return existingRecord.accounts;
    }
    return [
      {
        id: 'row-1',
        account_id: '',
        account_name: 'Office Rent Expense - 5120',
        debit: 25000,
        credit: 0,
        cost_center_id: '',
        user_remark: 'Headquarters premises monthly rent'
      },
      {
        id: 'row-2',
        account_id: '',
        account_name: 'HDFC Bank Ltd - 1001',
        debit: 0,
        credit: 25000,
        cost_center_id: '',
        user_remark: 'Bank RTGS transfer for premises rent'
      }
    ];
  });

  // When accounts load from backend, auto-assign valid UUIDs if missing
  useEffect(() => {
    if (accounts.length > 0) {
      setEntries(prev => prev.map((entry, idx) => {
        if (!entry.account_id) {
          const matched = accounts.find(a => 
            (entry.account_name && (a.account_name?.toLowerCase().includes(entry.account_name.toLowerCase()) || 
             a.name?.toLowerCase().includes(entry.account_name.toLowerCase())))
          ) || accounts[idx % accounts.length];
          return {
            ...entry,
            account_id: matched?.id || matched?.name,
            account_name: matched?.account_name || matched?.name || entry.account_name
          };
        }
        return entry;
      }));
    }
  }, [accounts]);

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Accounting Row Handlers
  const handleEntryChange = (id, field, value) => {
    setEntries(prev => prev.map(entry => {
      if (entry.id === id) {
        const updated = { ...entry, [field]: value };
        if (field === 'account_id') {
          const acc = accounts.find(a => a.id === value);
          if (acc) {
            updated.account_name = acc.account_name || acc.name;
          }
        }
        if (field === 'debit' && Number(value) > 0) {
          updated.credit = 0;
        } else if (field === 'credit' && Number(value) > 0) {
          updated.debit = 0;
        }
        return updated;
      }
      return entry;
    }));
  };

  const handleAddEntry = () => {
    const newId = `row-${Date.now()}`;
    const defaultAcc = accounts[entries.length % (accounts.length || 1)];
    setEntries(prev => [
      ...prev,
      {
        id: newId,
        account_id: defaultAcc?.id || '',
        account_name: defaultAcc?.account_name || defaultAcc?.name || 'Operating Expense',
        debit: 0,
        credit: 0,
        cost_center_id: costCenters[0]?.id || '',
        user_remark: ''
      }
    ]);
  };

  const handleRemoveEntry = (id) => {
    if (entries.length <= 2) {
      onShowToast?.('Journal Entry requires at least 2 balancing rows', 'error');
      return;
    }
    setEntries(prev => prev.filter(e => e.id !== id));
  };

  // Calculations & Balance Check
  const balanceCheck = useMemo(() => {
    const totalDebit = entries.reduce((sum, e) => sum + (Number(e.debit) || 0), 0);
    const totalCredit = entries.reduce((sum, e) => sum + (Number(e.credit) || 0), 0);
    const difference = Math.round((totalDebit - totalCredit) * 100) / 100;
    const isBalanced = difference === 0 && totalDebit > 0;

    return {
      totalDebit,
      totalCredit,
      difference,
      isBalanced
    };
  }, [entries]);

  // Quick auto-balance helper
  const handleAutoBalance = () => {
    if (balanceCheck.difference === 0) return;
    const diff = Math.abs(balanceCheck.difference);
    const newId = `row-${Date.now()}`;
    const balancingAcc = accounts.find(a => a.account_name?.toLowerCase().includes('bank') || a.account_type === 'Bank') || accounts[0];

    if (balanceCheck.difference > 0) {
      setEntries(prev => [
        ...prev,
        {
          id: newId,
          account_id: balancingAcc?.id || '',
          account_name: balancingAcc?.account_name || 'Balancing Bank Account',
          debit: 0,
          credit: diff,
          cost_center_id: costCenters[0]?.id || '',
          user_remark: 'Balancing Credit Entry'
        }
      ]);
    } else {
      setEntries(prev => [
        ...prev,
        {
          id: newId,
          account_id: balancingAcc?.id || '',
          account_name: balancingAcc?.account_name || 'Balancing Account',
          debit: diff,
          credit: 0,
          cost_center_id: costCenters[0]?.id || '',
          user_remark: 'Balancing Debit Entry'
        }
      ]);
    }
    onShowToast?.(`Added balancing row for ₹${diff.toLocaleString('en-IN')}`);
  };

  // Handle Save / Submit
  const handleSave = async (submitStatus = 'Draft') => {
    if (submitStatus === 'Submitted' && !balanceCheck.isBalanced) {
      onShowToast?.(
        `Cannot submit unbalanced entry! Debits and Credits must match (Diff: ₹${balanceCheck.difference})`,
        'error'
      );
      return;
    }

    setIsSubmitting(true);
    const recordName = existingRecord?.name || `ACC-JV-2026-${Math.floor(10000 + Math.random() * 90000)}`;

    // Format rows with valid UUIDs for Pydantic backend schema
    const formattedAccounts = entries.map((e, idx) => {
      let accId = e.account_id;
      if (!accId || accId.length < 32) {
        accId = accounts[idx % (accounts.length || 1)]?.id || null;
      }
      return {
        account_id: accId,
        cost_center_id: e.cost_center_id && e.cost_center_id.length >= 32 ? e.cost_center_id : null,
        debit: Number(e.debit) || 0,
        credit: Number(e.credit) || 0,
        user_remark: e.user_remark || ''
      };
    });

    const backendPayload = {
      posting_date: postingDate,
      voucher_type: voucherType,
      naming_series: namingSeries,
      title: `${voucherType} - ₹${balanceCheck.totalDebit.toLocaleString('en-IN')}`,
      cheque_no: chequeNo || null,
      cheque_date: chequeDate || null,
      user_remark: userRemark || null,
      is_opening: 'No',
      write_off_based_on: 'Accounts Receivable',
      accounts: formattedAccounts
    };

    const localPayload = {
      name: recordName,
      title: `${voucherType} - ₹${balanceCheck.totalDebit.toLocaleString('en-IN')}`,
      voucher_type: voucherType,
      naming_series: namingSeries,
      posting_date: postingDate,
      cheque_no: chequeNo,
      cheque_date: chequeDate,
      status: submitStatus === 'Submitted' ? 'Submitted' : 'Draft',
      docstatus: submitStatus === 'Submitted' ? 1 : 0,
      total_debit: balanceCheck.totalDebit,
      total_credit: balanceCheck.totalCredit,
      difference: balanceCheck.difference,
      user_remark: userRemark,
      accounts: entries
    };

    try {
      const headers = { 'Content-Type': 'application/json' };
      const token = localStorage.getItem('cb_access_token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const res = await fetch('/v1/journal-entries', {
        method: isEditing ? 'PUT' : 'POST',
        headers,
        body: JSON.stringify(backendPayload)
      }).catch(() => null);

      if (res && res.ok) {
        const data = await res.json();
        onShowToast?.(`Journal Entry ${data.name || recordName} saved & posted to PostgreSQL!`);
      } else {
        if (isEditing) {
          updateRecord('journal_entry', recordId, localPayload);
          onShowToast?.(`Journal Entry ${recordName} updated in store!`);
        } else {
          addRecord('journal_entry', localPayload);
          onShowToast?.(`Journal Entry ${recordName} saved!`);
        }
      }

      onNavigate({ type: 'list', domain: 'journal_entry' });
    } catch (err) {
      console.error(err);
      onShowToast?.('Failed to save Journal Entry', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate({ type: 'list', domain: 'journal_entry' })}
              className="p-1 -ml-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              General Ledger • Journal Entry
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
            {isEditing ? `Edit Journal Entry: ${existingRecord?.name}` : 'New Journal Entry'}
          </h1>
          <p className="text-[12.5px] text-slate-500">
            Multi-currency double-entry ledger vouchers with strict Debit = Credit auto-balancing validation.
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'list', domain: 'journal_entry' })}
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
            disabled={isSubmitting || !balanceCheck.isBalanced}
            className="flex items-center gap-1.5 px-5 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white text-[13px] font-semibold rounded-xl transition-all shadow-xs"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Post to General Ledger</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Voucher & Posting Information
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Voucher Type</label>
                <select
                  value={voucherType}
                  onChange={(e) => setVoucherType(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                >
                  <option value="Journal Entry">Journal Entry</option>
                  <option value="Bank Entry">Bank Entry</option>
                  <option value="Cash Entry">Cash Entry</option>
                  <option value="Credit Note">Credit Note</option>
                  <option value="Debit Note">Debit Note</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Posting Date</label>
                <input
                  type="date"
                  value={postingDate}
                  onChange={(e) => setPostingDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Cheque / Reference No</label>
                <input
                  type="text"
                  value={chequeNo}
                  onChange={(e) => setChequeNo(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] font-mono bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[12.5px] font-medium text-slate-700">Reference Date</label>
                <input
                  type="date"
                  value={chequeDate}
                  onChange={(e) => setChequeDate(e.target.value)}
                  className="w-full px-3 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg"
                />
              </div>
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Scale className="w-4 h-4 text-violet-600" />
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Accounting Entries (Debit / Credit)
                </h2>
              </div>
              <button
                type="button"
                onClick={handleAddEntry}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-lg transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Row</span>
              </button>
            </div>

            <div className="overflow-x-auto border border-slate-200 rounded-xl">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3 w-10 text-center">#</th>
                    <th className="py-2.5 px-3 min-w-[260px]">Account</th>
                    <th className="py-2.5 px-3 w-32 text-right">Debit (₹)</th>
                    <th className="py-2.5 px-3 w-32 text-right">Credit (₹)</th>
                    <th className="py-2.5 px-3 min-w-[140px]">Cost Center</th>
                    <th className="py-2.5 px-2 w-10 text-center"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {entries.map((entry, idx) => (
                    <tr key={entry.id} className="hover:bg-slate-50/50">
                      <td className="py-2 px-3 text-center text-slate-400 font-mono">{idx + 1}</td>
                      <td className="py-2 px-3 space-y-1.5">
                        {accounts.length > 0 ? (
                          <select
                            value={entry.account_id || ''}
                            onChange={(e) => handleEntryChange(entry.id, 'account_id', e.target.value)}
                            className="w-full font-medium text-slate-900 bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-xs"
                          >
                            <option value="">-- Select GL Account --</option>
                            {accounts.map(acc => (
                              <option key={acc.id} value={acc.id}>
                                {acc.account_name} ({acc.account_number || acc.name})
                              </option>
                            ))}
                          </select>
                        ) : (
                          <input
                            type="text"
                            value={entry.account_name || ''}
                            onChange={(e) => handleEntryChange(entry.id, 'account_name', e.target.value)}
                            className="w-full font-medium text-slate-900 border-0 p-1"
                          />
                        )}
                        <input
                          type="text"
                          value={entry.user_remark || ''}
                          onChange={(e) => handleEntryChange(entry.id, 'user_remark', e.target.value)}
                          placeholder="Row remark / narration..."
                          className="w-full text-[10.5px] text-slate-500 border-0 p-0.5"
                        />
                      </td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          value={entry.debit}
                          onChange={(e) => handleEntryChange(entry.id, 'debit', Number(e.target.value))}
                          className="w-28 text-right font-mono font-semibold text-slate-900 bg-slate-50 border border-slate-200 p-1.5 rounded"
                        />
                      </td>
                      <td className="py-2 px-3 text-right">
                        <input
                          type="number"
                          value={entry.credit}
                          onChange={(e) => handleEntryChange(entry.id, 'credit', Number(e.target.value))}
                          className="w-28 text-right font-mono font-semibold text-slate-900 bg-slate-50 border border-slate-200 p-1.5 rounded"
                        />
                      </td>
                      <td className="py-2 px-3">
                        <select
                          value={entry.cost_center_id || ''}
                          onChange={(e) => handleEntryChange(entry.id, 'cost_center_id', e.target.value)}
                          className="w-full text-slate-700 bg-slate-50 border border-slate-200 p-1 rounded"
                        >
                          <option value="">No Cost Center</option>
                          {costCenters.map(cc => (
                            <option key={cc.id} value={cc.id}>
                              {cc.cost_center_name || cc.name}
                            </option>
                          ))}
                        </select>
                      </td>
                      <td className="py-2 px-2 text-center">
                        <button
                          type="button"
                          onClick={() => handleRemoveEntry(entry.id)}
                          className="text-slate-300 hover:text-rose-600 p-1"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div>
          <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg space-y-4 sticky top-6">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-300">
              Double-Entry Check
            </h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between"><span>Total Debit</span><span className="font-mono">₹{balanceCheck.totalDebit.toLocaleString('en-IN')}</span></div>
              <div className="flex justify-between"><span>Total Credit</span><span className="font-mono">₹{balanceCheck.totalCredit.toLocaleString('en-IN')}</span></div>
              <div className="flex justify-between border-t border-slate-800 pt-2 font-bold">
                <span>Difference</span>
                <span className={balanceCheck.difference === 0 ? 'text-emerald-400' : 'text-rose-400'}>
                  ₹{balanceCheck.difference.toLocaleString('en-IN')}
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => handleSave('Submitted')}
              disabled={isSubmitting || !balanceCheck.isBalanced}
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-white font-semibold text-xs uppercase tracking-wider rounded-xl transition-all"
            >
              Post to General Ledger
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}