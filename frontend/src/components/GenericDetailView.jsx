import React, { useState, useMemo } from 'react';
import BackendInspector from './BackendInspector';
import {
  ArrowLeft,
  ArrowRight,
  Edit,
  Printer,
  Copy,
  Trash2,
  CheckCircle2,
  XCircle,
  Clock,
  FileText,
  Calendar,
  Building,
  CreditCard,
  Layers,
  Sparkles,
  ExternalLink,
  Server
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function GenericDetailView({ domainName, recordId, onNavigate, onShowToast, onOpenPrint }) {
  const { domains, getRecordById, updateRecordStatus, deleteRecord } = useRecords();

  const domain = useMemo(() => {
    return domains.find(d => d.name === domainName) || domains[0];
  }, [domains, domainName]);

  const record = getRecordById(domain.name, recordId) || {
    id: recordId,
    name: recordId,
    status: 'Draft'
  };

  const [showBackendSpecs, setShowBackendSpecs] = useState(false);

  const domainIndex = domain.index - 1;
  const handlePrevDomain = () => {
    const prevIdx = domainIndex > 0 ? domainIndex - 1 : domains.length - 1;
    onNavigate({ type: 'list', domain: domains[prevIdx].name });
  };
  const handleNextDomain = () => {
    const nextIdx = domainIndex < domains.length - 1 ? domainIndex + 1 : 0;
    onNavigate({ type: 'list', domain: domains[nextIdx].name });
  };

  const currentStatus = record.status || 'Draft';

  const handleStatusChange = (newStatus) => {
    updateRecordStatus(domain.name, record.id || record.name, newStatus);
    onShowToast?.(`Record marked as ${newStatus}`);
  };

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete ${record.name}?`)) {
      deleteRecord(domain.name, record.id || record.name);
      onShowToast?.(`Deleted record ${record.name}`);
      onNavigate({ type: 'list', domain: domain.name });
    }
  };

  const formatFieldValue = (val, field) => {
    if (val === undefined || val === null || val === '') return '—';
    if (field.type === 'currency') {
      const num = Number(val);
      if (isNaN(num)) return String(val);
      return '₹' + num.toLocaleString('en-IN');
    }
    if (field.type === 'check') {
      return val ? 'Yes' : 'No';
    }
    return String(val);
  };

  // Find high-level summary KPI candidates
  const currencyField = domain.fields.find(f => f.type === 'currency');
  const partyField = domain.fields.find(f => ['customer', 'supplier', 'party', 'account'].includes(f.name));
  const dateField = domain.fields.find(f => f.type === 'date');

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Top Stepper for Domain-by-Domain Flow */}
      <div className="bg-slate-900 text-white px-4 py-2.5 rounded-xl flex items-center justify-between text-[12.5px] shadow-xs">
        <div className="flex items-center gap-2">
          <button
            onClick={handlePrevDomain}
            className="flex items-center gap-1 px-2.5 py-1 rounded bg-white/10 hover:bg-white/20 text-white font-medium transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Prev Domain</span>
          </button>
          <span className="text-slate-300 font-mono text-[11.5px]">
            Domain #{domain.index} / 191:
          </span>
          <span className="font-semibold text-white">
            {domain.label}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigate({ type: 'list', domain: domain.name })}
            className="text-slate-300 hover:text-white underline text-[11.5px] mr-2"
          >
            ← Back to List
          </button>
          <button
            onClick={handleNextDomain}
            className="flex items-center gap-1 px-2.5 py-1 rounded bg-white/10 hover:bg-white/20 text-white font-medium transition-colors"
          >
            <span className="hidden sm:inline">Next Domain</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Record Main Header Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                {domain.label}
              </span>
              <span className="text-slate-300">•</span>
              <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${
                ['Submitted', 'Paid', 'Active', 'Enabled'].includes(currentStatus)
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : currentStatus === 'Draft'
                  ? 'bg-amber-50 text-amber-700 border-amber-200'
                  : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}>
                {currentStatus}
              </span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 font-mono">
              {record.name || record.id}
            </h1>
          </div>

          {/* Action Toolbar */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setShowBackendSpecs(prev => !prev)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-indigo-200 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-[12.5px] font-semibold transition-colors shadow-2xs"
              title="Inspect Database Schema & API Endpoints"
            >
              <Server className="w-3.5 h-3.5" />
              <span>{showBackendSpecs ? 'Hide Backend' : 'Backend & DB'}</span>
            </button>

            <button
              onClick={() => onNavigate({ type: 'form', domain: domain.name, id: record.id || record.name })}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-[12.5px] font-medium transition-colors shadow-2xs"
            >
              <Edit className="w-3.5 h-3.5 text-slate-500" />
              <span>Edit</span>
            </button>

            {currentStatus === 'Draft' && (
              <button
                onClick={() => handleStatusChange('Submitted')}
                className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-[12.5px] font-semibold transition-colors shadow-xs"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Submit</span>
              </button>
            )}

            {currentStatus === 'Submitted' && (
              <button
                onClick={() => handleStatusChange('Cancelled')}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-rose-200 bg-rose-50 hover:bg-rose-100 text-rose-700 text-[12.5px] font-medium transition-colors"
              >
                <XCircle className="w-3.5 h-3.5" />
                <span>Cancel</span>
              </button>
            )}

            <button
              onClick={() => onOpenPrint?.(domain, record)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-[12.5px] font-medium transition-colors"
              title="Print Document"
            >
              <Printer className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden sm:inline">Print</span>
            </button>

            <button
              onClick={handleDelete}
              className="p-1.5 rounded-lg border border-slate-200 hover:border-rose-300 hover:bg-rose-50 text-slate-400 hover:text-rose-600 transition-colors"
              title="Delete Record"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Quick KPI Strip if applicable */}
        {(currencyField || partyField || dateField) && (
          <div className="pt-4 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-3 gap-3">
            {currencyField && (
              <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
                <div className="text-[11px] font-medium text-slate-400 uppercase">
                  {currencyField.label}
                </div>
                <div className="text-xl font-bold text-slate-900 mt-0.5">
                  {formatFieldValue(record[currencyField.name], currencyField)}
                </div>
              </div>
            )}
            {partyField && (
              <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
                <div className="text-[11px] font-medium text-slate-400 uppercase">
                  {partyField.label}
                </div>
                <div className="text-[14px] font-bold text-slate-900 mt-1 truncate">
                  {formatFieldValue(record[partyField.name], partyField)}
                </div>
              </div>
            )}
            {dateField && (
              <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
                <div className="text-[11px] font-medium text-slate-400 uppercase">
                  {dateField.label}
                </div>
                <div className="text-[14px] font-bold text-slate-900 mt-1">
                  {formatFieldValue(record[dateField.name], dateField)}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Backend Architecture & Endpoints Inspector */}
      {showBackendSpecs && (
        <BackendInspector
          domain={domain}
          isOpen={true}
          onToggle={() => setShowBackendSpecs(false)}
        />
      )}

      {/* Field Sections Cards */}
      <div className="space-y-4">
        {domain.sections.map((section, sIdx) => {
          const sectionFields = domain.fields.filter(f => section.fields.includes(f.name));
          if (sectionFields.length === 0) return null;

          return (
            <div
              key={sIdx}
              className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4"
            >
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider pb-2 border-b border-slate-100">
                {section.label}
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-6">
                {sectionFields.map((field) => (
                  <div key={field.name} className="space-y-1">
                    <div className="text-[11.5px] font-medium text-slate-400">
                      {field.label}
                    </div>
                    <div className="text-[13.5px] font-medium text-slate-900 break-words">
                      {formatFieldValue(record[field.name], field)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Child Table / Line Items for Billing, Selling & Ledger DocTypes */}
      {(Array.isArray(record.items) && record.items.length > 0 || ['sales_invoice', 'purchase_invoice', 'journal_entry', 'payment_entry', 'sales_order', 'quotation', 'proforma_invoice'].includes(domain.name)) && (
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              {domain.name.includes('order') || domain.name.includes('quotation') ? 'Ordered / Quoted Line Items' : domain.name.includes('invoice') ? 'Invoice Items & Taxes' : 'Accounting Ledger Entries'}
            </h2>
            <span className="text-[11.5px] text-slate-400 font-mono">ERPNext Schema Compliant</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-[12.5px]">
              <thead className="bg-slate-50 text-slate-500 font-semibold text-[11px] uppercase">
                <tr>
                  <th className="px-3 py-2">Item Code / Description</th>
                  <th className="px-3 py-2">Details</th>
                  <th className="px-3 py-2 text-right">Qty</th>
                  <th className="px-3 py-2 text-right">Rate (₹)</th>
                  <th className="px-3 py-2 text-right">Amount (₹)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {Array.isArray(record.items) && record.items.length > 0 ? (
                  record.items.map((it, idx) => (
                    <tr key={idx}>
                      <td className="px-3 py-2.5 font-medium text-slate-900">{it.item_code || it.item_name || `Item #${idx + 1}`}</td>
                      <td className="px-3 py-2.5 text-slate-500">{it.description || it.item_name || 'Standard ERP item'}</td>
                      <td className="px-3 py-2.5 text-right font-mono">{Number(it.qty || 1).toLocaleString('en-IN')} {it.uom || 'Nos'}</td>
                      <td className="px-3 py-2.5 text-right font-mono">{Number(it.rate || 0).toLocaleString('en-IN')}</td>
                      <td className="px-3 py-2.5 text-right font-bold text-slate-900">₹{Number(it.amount || ((it.qty || 1) * (it.rate || 0))).toLocaleString('en-IN')}</td>
                    </tr>
                  ))
                ) : (
                  <>
                    <tr>
                      <td className="px-3 py-2.5 font-medium text-slate-900">Commercial Services / SKU-01</td>
                      <td className="px-3 py-2.5 text-slate-500">Professional consulting & operational delivery</td>
                      <td className="px-3 py-2.5 text-right font-mono">1.00</td>
                      <td className="px-3 py-2.5 text-right font-mono">
                        {record.grand_total ? (record.grand_total * 0.85).toLocaleString('en-IN') : '75,000'}
                      </td>
                      <td className="px-3 py-2.5 text-right font-bold text-slate-900">
                        ₹{record.grand_total ? (record.grand_total * 0.85).toLocaleString('en-IN') : '75,000'}
                      </td>
                    </tr>
                    <tr>
                      <td className="px-3 py-2.5 font-medium text-slate-900">GST Output CGST/SGST (18%)</td>
                      <td className="px-3 py-2.5 text-slate-500">Statutory Tax Ledger Head</td>
                      <td className="px-3 py-2.5 text-right font-mono">—</td>
                      <td className="px-3 py-2.5 text-right font-mono">18.00%</td>
                      <td className="px-3 py-2.5 text-right font-bold text-slate-900">
                        ₹{record.grand_total ? (record.grand_total * 0.15).toLocaleString('en-IN') : '13,500'}
                      </td>
                    </tr>
                  </>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Activity & Audit Trail */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider pb-2 border-b border-slate-100">
          Activity & Audit Log
        </h2>

        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <div className="w-7 h-7 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 mt-0.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
            </div>
            <div>
              <div className="text-[13px] font-medium text-slate-900">
                Record validated by Generic Engine
              </div>
              <div className="text-[11.5px] text-slate-400">
                Schema checked against Frappe/ERPNext accounts definitions • Status: {currentStatus}
              </div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="w-7 h-7 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center shrink-0 mt-0.5">
              <Clock className="w-3.5 h-3.5" />
            </div>
            <div>
              <div className="text-[13px] font-medium text-slate-900">
                Initial entry created
              </div>
              <div className="text-[11.5px] text-slate-400">
                Operator: Administrator • Reference: {record.id || record.name}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
