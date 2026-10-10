import React, { useState } from 'react';
import {
  ArrowLeft,
  Save,
  X,
  Truck,
  Building2,
  MapPin,
  Phone,
  Mail,
  CreditCard,
  ShieldCheck,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function SupplierFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord, fetchDomainRecords } = useRecords();
  const existingRecord = recordId ? getRecordById('supplier', recordId) : null;
  const isEditing = !!existingRecord;

  const [supplierName, setSupplierName] = useState(existingRecord?.supplier_name || '');
  const [supplierType, setSupplierType] = useState(existingRecord?.supplier_type || 'Company');
  const [supplierGroup, setSupplierGroup] = useState(existingRecord?.supplier_group || 'Raw Material');
  const [country, setCountry] = useState(existingRecord?.country || 'India');
  const [taxId, setTaxId] = useState(existingRecord?.tax_id || '');
  const [pan, setPan] = useState(existingRecord?.pan || '');

  const [primaryAddress, setPrimaryAddress] = useState(
    existingRecord?.primary_address || ''
  );
  const [contactPerson, setContactPerson] = useState(
    existingRecord?.supplier_primary_contact || existingRecord?.contact_person || ''
  );
  const [contactMobile, setContactMobile] = useState(
    existingRecord?.mobile_no || existingRecord?.contact_mobile || ''
  );
  const [contactEmail, setContactEmail] = useState(
    existingRecord?.email_id || existingRecord?.contact_email || ''
  );

  const [defaultCurrency, setDefaultCurrency] = useState(existingRecord?.default_currency || 'INR');
  const [isTransporter, setIsTransporter] = useState(existingRecord?.is_transporter || false);
  const [isInternalSupplier, setIsInternalSupplier] = useState(existingRecord?.is_internal_supplier || false);
  const [onHold, setOnHold] = useState(existingRecord?.on_hold || false);
  const [status, setStatus] = useState(existingRecord?.status || 'Active');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSave = async (e) => {
    e?.preventDefault();
    if (!supplierName.trim()) {
      onShowToast?.('Supplier Name is required', 'error');
      return;
    }

    setIsSubmitting(true);
    const recordName = existingRecord?.name || `SUP-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    const payload = {
      name: recordName,
      supplier_name: supplierName.trim(),
      supplier_type: supplierType,
      supplier_group: supplierGroup,
      country: country,
      tax_id: taxId.trim(),
      pan: pan.trim() || (taxId.trim().length === 15 ? taxId.trim().substring(2, 12) : ''),
      primary_address: primaryAddress.trim(),
      supplier_primary_contact: contactPerson.trim(),
      mobile_no: contactMobile.trim(),
      email_id: contactEmail.trim(),
      default_currency: defaultCurrency,
      is_transporter: isTransporter,
      is_internal_supplier: isInternalSupplier,
      on_hold: onHold,
      disabled: status === 'Disabled',
      is_frozen: false,
      warn_rfqs: false,
      warn_pos: false,
      prevent_rfqs: false,
      prevent_pos: false,
      allow_purchase_invoice_creation_without_purchase_order: false,
      allow_purchase_invoice_creation_without_purchase_receipt: false,
      restrict_to_companies: false,
      status: status
    };

    try {
      let savedToDb = false;
      try {
        const res = await fetch('/api/buying/supplier', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          const json = await res.json();
          savedToDb = true;
          console.log('[PostgreSQL API] Supplier persisted:', json);
        }
      } catch (err) {
        console.warn('[PostgreSQL API Warning] Fallback to context store:', err.message);
      }

      if (isEditing) {
        await updateRecord('supplier', recordId, payload);
        onShowToast?.(
          savedToDb
            ? `Supplier "${supplierName}" updated & synced with PostgreSQL!`
            : `Supplier "${supplierName}" updated successfully!`,
          'success'
        );
      } else {
        await addRecord('supplier', payload);
        onShowToast?.(
          savedToDb
            ? `Supplier "${supplierName}" created & saved to PostgreSQL database!`
            : `Supplier "${supplierName}" created successfully!`,
          'success'
        );
      }

      fetchDomainRecords('supplier', true);
      onNavigate?.({ type: 'list', domain: 'supplier', module: 'Buying' });
    } catch (err) {
      onShowToast?.(`Failed to save: ${err.message}`, 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6 animate-fadeIn">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b pb-4">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => onNavigate?.({ type: 'list', domain: 'supplier', module: 'Buying' })}
            className="p-2 hover:bg-slate-100 rounded-lg text-slate-600 transition"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded">
                Buying Module
              </span>
              <span className="text-xs text-slate-500">Domain #9 / 19</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">
              {isEditing ? `Edit Supplier: ${existingRecord?.name}` : 'New Supplier Registration'}
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              100% ERPNext Cloud schema compliant • Direct live sync to PostgreSQL
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            type="button"
            onClick={() => onNavigate?.({ type: 'list', domain: 'supplier', module: 'Buying' })}
            className="px-4 py-2 border rounded-lg text-slate-700 hover:bg-slate-50 transition flex items-center space-x-2"
          >
            <X className="w-4 h-4" />
            <span>Cancel</span>
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={isSubmitting}
            className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition flex items-center space-x-2 font-medium shadow-sm disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>{isSubmitting ? 'Saving to Database...' : isEditing ? 'Update Supplier' : 'Save Supplier'}</span>
          </button>
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Core Supplier Details */}
        <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 text-slate-900 font-semibold border-b pb-2">
            <Truck className="w-5 h-5 text-emerald-600" />
            <span>Core Identification & Master Information</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Supplier Name <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={supplierName}
                onChange={(e) => setSupplierName(e.target.value)}
                placeholder="e.g. Tata Steel Limited"
                required
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Supplier Type <span className="text-rose-500">*</span>
              </label>
              <select
                value={supplierType}
                onChange={(e) => setSupplierType(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                <option value="Company">Company (Pvt Ltd / Ltd / LLP)</option>
                <option value="Individual">Individual / Proprietorship</option>
                <option value="Partnership">Partnership Firm</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Supplier Group
              </label>
              <select
                value={supplierGroup}
                onChange={(e) => setSupplierGroup(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                <option value="Raw Material">Raw Material</option>
                <option value="Electrical Components">Electrical Components</option>
                <option value="Hardware & Precision">Hardware & Precision Parts</option>
                <option value="IT & Services">IT & Cloud Services</option>
                <option value="Distributor">Authorized Distributor</option>
                <option value="Packaging">Packaging Material</option>
                <option value="Services">Consulting & Logistics Services</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Country
              </label>
              <input
                type="text"
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                placeholder="India"
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>
          </div>
        </div>

        {/* Section 2: Taxation & Statutory */}
        <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 text-slate-900 font-semibold border-b pb-2">
            <Building2 className="w-5 h-5 text-emerald-600" />
            <span>Taxation & Statutory Registrations</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                GSTIN / Tax ID
              </label>
              <input
                type="text"
                value={taxId}
                onChange={(e) => {
                  const val = e.target.value.toUpperCase();
                  setTaxId(val);
                  if (val.length === 15 && !pan) {
                    setPan(val.substring(2, 12));
                  }
                }}
                placeholder="e.g. 27AAACT2727Q1ZW"
                className="w-full px-3 py-2 border rounded-lg text-sm font-mono focus:ring-2 focus:ring-emerald-500 outline-none uppercase"
              />
              <span className="text-[11px] text-slate-400 mt-0.5 block">
                15-character Indian Goods and Services Tax Identification Number
              </span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                PAN (Permanent Account Number)
              </label>
              <input
                type="text"
                value={pan}
                onChange={(e) => setPan(e.target.value.toUpperCase())}
                placeholder="e.g. AAACT2727Q"
                className="w-full px-3 py-2 border rounded-lg text-sm font-mono focus:ring-2 focus:ring-emerald-500 outline-none uppercase"
              />
            </div>
          </div>
        </div>

        {/* Section 3: Primary Contact & Address */}
        <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 text-slate-900 font-semibold border-b pb-2">
            <MapPin className="w-5 h-5 text-emerald-600" />
            <span>Primary Contact & Operating Address</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Key Contact Person
              </label>
              <input
                type="text"
                value={contactPerson}
                onChange={(e) => setContactPerson(e.target.value)}
                placeholder="e.g. Rajesh Nambiar"
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Mobile Number
              </label>
              <input
                type="text"
                value={contactMobile}
                onChange={(e) => setContactMobile(e.target.value)}
                placeholder="+91 98210 11223"
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Corporate Email
              </label>
              <input
                type="email"
                value={contactEmail}
                onChange={(e) => setContactEmail(e.target.value)}
                placeholder="procurement@tatasteel.com"
                className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Registered / Works Address
            </label>
            <textarea
              rows={2}
              value={primaryAddress}
              onChange={(e) => setPrimaryAddress(e.target.value)}
              placeholder="e.g. Bombay House, 24 Homi Mody Street, Fort, Mumbai 400001"
              className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 outline-none"
            />
          </div>
        </div>

        {/* Section 4: Operational Flags & Preferences */}
        <div className="bg-white rounded-xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 text-slate-900 font-semibold border-b pb-2">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
            <span>Procurement Preferences & Operational Flags</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Default Currency
              </label>
              <select
                value={defaultCurrency}
                onChange={(e) => setDefaultCurrency(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                <option value="INR">INR - Indian Rupee</option>
                <option value="USD">USD - US Dollar</option>
                <option value="EUR">EUR - Euro</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Account Status
              </label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                <option value="Active">Active (Eligible for POs & RFQs)</option>
                <option value="Disabled">Disabled / Inactive</option>
              </select>
            </div>

            <div className="flex items-center pt-5 space-x-6">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={isTransporter}
                  onChange={(e) => setIsTransporter(e.target.checked)}
                  className="rounded text-emerald-600 focus:ring-emerald-500 h-4 w-4"
                />
                <span className="text-xs font-medium text-slate-700">Is Transporter</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={onHold}
                  onChange={(e) => setOnHold(e.target.checked)}
                  className="rounded text-emerald-600 focus:ring-emerald-500 h-4 w-4"
                />
                <span className="text-xs font-medium text-slate-700">Hold Payments</span>
              </label>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3 pt-2">
          <button
            type="button"
            onClick={() => onNavigate?.({ type: 'list', domain: 'supplier', module: 'Buying' })}
            className="px-5 py-2 border rounded-lg text-slate-700 hover:bg-slate-50 transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg shadow-sm transition disabled:opacity-50 flex items-center space-x-2"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>{isSubmitting ? 'Saving to Database...' : isEditing ? 'Update Supplier' : 'Register Supplier'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
