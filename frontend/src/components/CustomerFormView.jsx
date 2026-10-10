import React, { useState } from 'react';
import {
  ArrowLeft,
  Save,
  X,
  User,
  Building2,
  MapPin,
  Phone,
  Mail,
  CreditCard,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function CustomerFormView({ recordId, onNavigate, onShowToast }) {
  const { getRecordById, addRecord, updateRecord } = useRecords();
  const existingRecord = recordId ? getRecordById('customer', recordId) : null;
  const isEditing = !!existingRecord;

  const [customerName, setCustomerName] = useState(existingRecord?.customer_name || 'Acme Technologies Pvt Ltd');
  const [customerType, setCustomerType] = useState(existingRecord?.customer_type || 'Company');
  const [customerGroup, setCustomerGroup] = useState(existingRecord?.customer_group || 'Commercial');
  const [territory, setTerritory] = useState(existingRecord?.territory || 'India West - Mumbai');
  const [taxId, setTaxId] = useState(existingRecord?.tax_id || '27AABCA1234F1Z5');
  const [pan, setPan] = useState(existingRecord?.pan || 'AABCA1234F');

  const [primaryAddress, setPrimaryAddress] = useState(
    existingRecord?.primary_address || 'Plot 44, MIDC Industrial Area, Andheri East, Mumbai 400093'
  );
  const [contactPerson, setContactPerson] = useState(existingRecord?.contact_person || 'Anil Mehta');
  const [contactMobile, setContactMobile] = useState(existingRecord?.contact_mobile || '+91 98200 12345');
  const [contactEmail, setContactEmail] = useState(existingRecord?.contact_email || 'anil@acme.in');

  const [creditLimit, setCreditLimit] = useState(Number(existingRecord?.credit_limit) || 1000000);
  const [status, setStatus] = useState(existingRecord?.status || 'Active');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSave = async () => {
    if (!customerName) {
      onShowToast?.('Customer Name is required', 'error');
      return;
    }

    setIsSubmitting(true);
    const recordName = existingRecord?.name || `CUST-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    const payload = {
      name: recordName,
      customer_name: customerName,
      customer_type: customerType,
      customer_group: customerGroup,
      territory,
      tax_id: taxId,
      pan,
      primary_address: primaryAddress,
      contact_person: contactPerson,
      contact_mobile: contactMobile,
      contact_email: contactEmail,
      credit_limit: creditLimit,
      status
    };

    try {
      const res = await fetch('/api/selling/customer', {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(() => null);

      if (res && res.ok) {
        onShowToast?.(`Customer ${customerName} saved & synced to PostgreSQL!`);
      } else {
        if (isEditing) updateRecord('customer', recordId, payload);
        else addRecord('customer', payload);
        onShowToast?.(`Customer ${customerName} saved!`);
      }

      onNavigate({ type: 'list', domain: 'customer', module: 'Selling' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-16">
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex justify-between items-center">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Customer Management</span>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">{isEditing ? `Edit Customer: ${customerName}` : 'New Customer Master'}</h1>
        </div>

        <div className="flex items-center gap-2.5">
          <button type="button" onClick={() => onNavigate({ type: 'list', domain: 'customer', module: 'Selling' })} className="px-4 py-2 border border-slate-200 text-slate-600 text-xs rounded-xl">Cancel</button>
          <button type="button" onClick={handleSave} disabled={isSubmitting} className="px-5 py-2 bg-slate-900 text-white text-xs font-semibold rounded-xl">Save Customer</button>
        </div>
      </div>

      <div className="space-y-6">
        {/* Section 1: Basic Details */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900 border-b pb-2">Identification & Classification</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-medium text-slate-700">Customer Legal Name *</label>
              <input type="text" value={customerName} onChange={(e) => setCustomerName(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Customer Type</label>
              <select value={customerType} onChange={(e) => setCustomerType(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs">
                <option value="Company">Company</option>
                <option value="Individual">Individual</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Customer Group</label>
              <select value={customerGroup} onChange={(e) => setCustomerGroup(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs">
                <option value="Commercial">Commercial</option>
                <option value="Retail Chains">Retail Chains</option>
                <option value="Government">Government</option>
                <option value="Export">Export</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Territory</label>
              <input type="text" value={territory} onChange={(e) => setTerritory(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">GSTIN / Tax ID</label>
              <input type="text" value={taxId} onChange={(e) => setTaxId(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs font-mono" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">PAN</label>
              <input type="text" value={pan} onChange={(e) => setPan(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs font-mono" />
            </div>
          </div>
        </div>

        {/* Section 2: Address & Contact */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900 border-b pb-2">Primary Address & Contacts</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="sm:col-span-2">
              <label className="text-xs font-medium text-slate-700">Billing Address</label>
              <input type="text" value={primaryAddress} onChange={(e) => setPrimaryAddress(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Primary Contact Person</label>
              <input type="text" value={contactPerson} onChange={(e) => setContactPerson(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Mobile Phone</label>
              <input type="text" value={contactMobile} onChange={(e) => setContactMobile(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs font-mono" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Email Address</label>
              <input type="email" value={contactEmail} onChange={(e) => setContactEmail(e.target.value)} className="w-full p-2 border rounded-lg bg-slate-50 text-xs" />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-700">Approved Credit Limit (₹)</label>
              <input type="number" value={creditLimit} onChange={(e) => setCreditLimit(Number(e.target.value))} className="w-full p-2 border rounded-lg bg-slate-50 text-xs font-mono font-bold" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
