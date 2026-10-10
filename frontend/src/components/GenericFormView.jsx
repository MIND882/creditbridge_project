import React, { useState, useMemo } from 'react';
import {
  ArrowLeft,
  Save,
  X,
  AlertCircle,
  CheckCircle2,
  Sparkles,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Search,
  Layers,
  Filter
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';
import SalesInvoiceFormView from './SalesInvoiceFormView';
import PurchaseInvoiceFormView from './PurchaseInvoiceFormView';
import PaymentEntryFormView from './PaymentEntryFormView';
import JournalEntryFormView from './JournalEntryFormView';
import SalesOrderFormView from './SalesOrderFormView';
import QuotationFormView from './QuotationFormView';
import CustomerFormView from './CustomerFormView';
import SupplierFormView from './SupplierFormView';
import PurchaseOrderFormView from './PurchaseOrderFormView';

export default function GenericFormView({ domainName, recordId, onNavigate, onShowToast }) {
  // Delegate core transactional documents to dedicated ERPNext Cloud interactive forms
  if (domainName === 'supplier') {
    return (
      <SupplierFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'purchase_order') {
    return (
      <PurchaseOrderFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'sales_invoice') {
    return (
      <SalesInvoiceFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'purchase_invoice') {
    return (
      <PurchaseInvoiceFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'payment_entry') {
    return (
      <PaymentEntryFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'journal_entry') {
    return (
      <JournalEntryFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  // Selling Module dedicated forms
  if (domainName === 'sales_order') {
    return (
      <SalesOrderFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'quotation') {
    return (
      <QuotationFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  if (domainName === 'customer') {
    return (
      <CustomerFormView
        recordId={recordId}
        onNavigate={onNavigate}
        onShowToast={onShowToast}
      />
    );
  }

  const { domains, getRecordById, addRecord, updateRecord } = useRecords();

  const domain = useMemo(() => {
    return domains.find(d => d.name === domainName) || domains[0];
  }, [domains, domainName]);

  const existingRecord = recordId ? getRecordById(domain.name, recordId) : null;
  const isEditing = !!existingRecord;

  // Search filter across all fields in complex forms
  const [fieldSearch, setFieldSearch] = useState('');

  // Track collapsed state of sections (first 2 sections open by default)
  const [openSections, setOpenSections] = useState(() => {
    const initial = {};
    (domain.sections || []).forEach((sec, idx) => {
      initial[sec.label] = idx < 2; // Open first 2 sections by default
    });
    return initial;
  });

  const toggleSection = (label) => {
    setOpenSections(prev => ({
      ...prev,
      [label]: !prev[label]
    }));
  };

  const handleExpandAll = () => {
    const all = {};
    (domain.sections || []).forEach(sec => { all[sec.label] = true; });
    setOpenSections(all);
  };

  const handleCollapseAll = () => {
    const all = {};
    (domain.sections || []).forEach(sec => { all[sec.label] = false; });
    setOpenSections(all);
  };

  // Initial Form Data
  const [formData, setFormData] = useState(() => {
    if (existingRecord) {
      return { ...existingRecord };
    }
    const initial = {};
    (domain.fields || []).forEach(field => {
      if (field.name === 'name') {
        const prefix = domain.name.split('_').map(w => w[0]).join('').toUpperCase() || 'ACC';
        initial.name = `${prefix.slice(0, 4)}-2026-${Math.floor(1000 + Math.random() * 9000)}`;
      } else if (field.type === 'select' && field.options && field.options.length > 0) {
        initial[field.name] = field.options[0];
      } else if (field.type === 'date') {
        initial[field.name] = new Date().toISOString().slice(0, 10);
      } else if (field.type === 'currency' || field.type === 'number') {
        initial[field.name] = 0;
      } else if (field.type === 'check') {
        initial[field.name] = false;
      } else {
        initial[field.name] = '';
      }
    });
    if (!initial.status) {
      initial.status = 'Draft';
    }
    return initial;
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
    if (errors[fieldName]) {
      setErrors(prev => {
        const copy = { ...prev };
        delete copy[fieldName];
        return copy;
      });
    }
  };

  const validate = () => {
    const errs = {};
    (domain.fields || []).forEach(field => {
      if (field.required) {
        const val = formData[field.name];
        if (val === undefined || val === null || val === '') {
          errs[field.name] = `${field.label} is required`;
        }
      }
    });
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) {
      onShowToast?.('Please resolve required form fields highlighted in red', 'error');
      return;
    }

    setIsSubmitting(true);

    try {
      if (isEditing) {
        updateRecord(domain.name, recordId, formData);
        onShowToast?.(`Updated ${domain.label}: ${formData.name || recordId}`);
        onNavigate({ type: 'detail', domain: domain.name, id: recordId });
      } else {
        const created = addRecord(domain.name, formData);
        onShowToast?.(`Created ${domain.label}: ${created.name || created.id}`);
        onNavigate({ type: 'detail', domain: domain.name, id: created.id });
      }
    } catch (err) {
      console.error(err);
      onShowToast?.('Failed to save record', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderFieldInput = (field) => {
    const value = formData[field.name] ?? '';
    const hasError = !!errors[field.name];

    switch (field.type) {
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          >
            {(field.options || ['Draft', 'Submitted', 'Active', 'Disabled']).map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        );

      case 'date':
        return (
          <input
            type="date"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          />
        );

      case 'datetime':
        return (
          <input
            type="datetime-local"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          />
        );

      case 'time':
        return (
          <input
            type="time"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          />
        );

      case 'currency':
        return (
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs font-semibold">
              ₹
            </span>
            <input
              type="number"
              value={value}
              onChange={(e) => handleInputChange(field.name, Number(e.target.value))}
              placeholder="0.00"
              className={`w-full pl-8 pr-3 py-2 text-[13px] font-mono bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
                hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
              }`}
            />
          </div>
        );

      case 'number':
        return (
          <input
            type="number"
            value={value}
            onChange={(e) => handleInputChange(field.name, Number(e.target.value))}
            className={`w-full px-3 py-2 text-[13px] font-mono bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          />
        );

      case 'check':
        return (
          <label className="flex items-center gap-2 cursor-pointer mt-1 py-1">
            <input
              type="checkbox"
              checked={!!value}
              onChange={(e) => handleInputChange(field.name, e.target.checked)}
              className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
            />
            <span className="text-[13px] text-slate-700 font-medium">Enabled / Active</span>
          </label>
        );

      case 'textarea':
        return (
          <textarea
            rows={3}
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={`Enter ${field.label.toLowerCase()}...`}
            className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          />
        );

      case 'link':
        return (
          <div className="relative">
            <input
              type="text"
              value={value}
              onChange={(e) => handleInputChange(field.name, e.target.value)}
              placeholder={`Link to ${field.linkTo || 'Master Document'}...`}
              className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
                hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
              }`}
            />
            {field.linkTo && (
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-mono font-medium px-1.5 py-0.5 rounded bg-slate-200/70 text-slate-600">
                {field.linkTo}
              </span>
            )}
          </div>
        );

      default:
        return (
          <input
            type="text"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={`Enter ${field.label.toLowerCase()}...`}
            className={`w-full px-3 py-2 text-[13px] bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 ${
              hasError ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200'
            }`}
          />
        );
    }
  };

  const totalFieldsCount = domain.fields ? domain.fields.length : 0;

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-16">
      {/* Form Top Navigation Bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate({ type: 'list', domain: domain.name })}
              className="p-1 -ml-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              {domain.category || 'Accounting'} • {domain.label}
            </span>
            <span className="text-slate-300">•</span>
            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700">
              {isEditing ? 'Editing' : 'New Creation'}
            </span>
            <span className="text-slate-300">•</span>
            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
              {totalFieldsCount} Fields
            </span>
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            {isEditing ? `Edit ${domain.label}: ${formData.name || recordId}` : `New ${domain.label}`}
          </h1>
          <p className="text-[12.5px] text-slate-500">
            {domain.description || `Manage and record ${domain.label} entries per ERPNext schema.`}
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'list', domain: domain.name })}
            className="flex items-center gap-1.5 px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-600 text-[13px] font-medium rounded-xl transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            <span>Cancel</span>
          </button>

          <button
            type="button"
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-5 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white text-[13px] font-semibold rounded-xl transition-all shadow-xs"
          >
            <Save className="w-4 h-4" />
            <span>{isSubmitting ? 'Saving...' : 'Save & Post'}</span>
          </button>
        </div>
      </div>

      {/* Field Search & Accordion Controls (Especially helpful for 40-100+ field domains) */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-2xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={fieldSearch}
            onChange={(e) => setFieldSearch(e.target.value)}
            placeholder={`Search across ${totalFieldsCount} fields (e.g. rate, date, tax, center)...`}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900"
          />
        </div>

        <div className="flex items-center gap-2 shrink-0 justify-end">
          <button
            type="button"
            onClick={handleExpandAll}
            className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
          >
            Expand All
          </button>
          <button
            type="button"
            onClick={handleCollapseAll}
            className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* Structured Sections Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {(domain.sections || []).map((section, sIdx) => {
          let sectionFields = (domain.fields || []).filter(f => (section.fields || []).includes(f.name));

          // Apply field search filter if user typed anything
          if (fieldSearch.trim()) {
            const query = fieldSearch.toLowerCase();
            sectionFields = sectionFields.filter(f =>
              f.name.toLowerCase().includes(query) ||
              f.label.toLowerCase().includes(query) ||
              (f.type && f.type.toLowerCase().includes(query))
            );
          }

          if (sectionFields.length === 0) return null;

          const isOpen = fieldSearch.trim() ? true : (openSections[section.label] ?? true);

          return (
            <div
              key={sIdx}
              className="bg-white border border-slate-200 rounded-2xl shadow-2xs overflow-hidden transition-all"
            >
              {/* Collapsible Section Header */}
              <button
                type="button"
                onClick={() => toggleSection(section.label)}
                className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50/70 transition-colors border-b border-slate-100"
              >
                <div className="flex items-center gap-3">
                  <div className="w-6 h-6 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-mono font-bold text-xs">
                    {sIdx + 1}
                  </div>
                  <div>
                    <h2 className="text-sm font-bold text-slate-900 tracking-wide">
                      {section.label}
                    </h2>
                    <p className="text-[11px] text-slate-400">
                      {sectionFields.length} field(s) available
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-semibold text-slate-400">
                    {isOpen ? 'Collapse' : 'Expand'}
                  </span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400" />
                  )}
                </div>
              </button>

              {/* Section Fields Grid */}
              {isOpen && (
                <div className="p-6 bg-white">
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                    {sectionFields.map((field) => (
                      <div
                        key={field.name}
                        className={`space-y-1.5 ${field.type === 'textarea' ? 'sm:col-span-2 md:col-span-3' : ''}`}
                      >
                        <div className="flex items-center justify-between">
                          <label className="block text-[12px] font-medium text-slate-700">
                            {field.label}
                            {field.required && (
                              <span className="text-rose-500 ml-1 font-bold">*</span>
                            )}
                          </label>
                          <span className="text-[10px] font-mono text-slate-400">
                            {field.type}
                          </span>
                        </div>

                        {renderFieldInput(field)}

                        {errors[field.name] && (
                          <div className="flex items-center gap-1 text-[11px] text-rose-600 font-medium mt-1">
                            <AlertCircle className="w-3 h-3" />
                            <span>{errors[field.name]}</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {/* Form Bottom Action */}
        <div className="flex items-center justify-end gap-3 pt-4">
          <button
            type="button"
            onClick={() => onNavigate({ type: 'list', domain: domain.name })}
            className="px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-600 text-[13px] font-medium rounded-xl transition-colors"
          >
            Discard
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-6 py-2.5 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white text-[13px] font-semibold rounded-xl shadow-xs transition-all"
          >
            <Save className="w-4 h-4" />
            <span>Save & Post to Ledger</span>
          </button>
        </div>
      </form>
    </div>
  );
}
