import React from 'react';
import { X, Printer, Download, CheckCircle2 } from 'lucide-react';

export default function PrintModal({ open, onClose, domain, record }) {
  if (!open || !domain || !record) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs p-4 flex items-center justify-center overflow-y-auto"
      onClick={onClose}
    >
      <div
        className="w-full max-w-3xl bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden my-8"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="h-14 px-6 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2">
            <Printer className="w-4 h-4 text-slate-600" />
            <span className="font-semibold text-slate-900 text-sm">
              Document Print Preview • {domain.label}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print Document</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200/50"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Printable Document Body */}
        <div className="p-8 sm:p-12 space-y-8 bg-white print:p-0 print:m-0 text-slate-900">
          {/* Letterhead */}
          <div className="flex items-start justify-between border-b-2 border-slate-900 pb-6">
            <div className="space-y-1">
              <h1 className="text-xl font-bold tracking-tight text-slate-900">
                CREDITBRIDGE GLOBAL ENTERPRISE LTD.
              </h1>
              <p className="text-xs text-slate-500">
                Plot 42, Bandra-Kurla Complex (BKC), Mumbai, Maharashtra 400051
              </p>
              <p className="text-xs text-slate-500 font-mono">
                GSTIN: 27AABCC1234D1Z8 • PAN: AABCC1234D • CIN: U72900MH2024PTC123456
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-black uppercase text-slate-900 tracking-wider">
                {domain.label}
              </div>
              <div className="text-sm font-mono font-bold text-indigo-700 mt-1">
                {record.name || record.id}
              </div>
              <div className="text-xs text-slate-500 mt-1">
                Date: {record.posting_date || record.date || new Date().toISOString().slice(0, 10)}
              </div>
            </div>
          </div>

          {/* Record Key Info Grid */}
          <div className="grid grid-cols-2 gap-6 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs">
            <div>
              <span className="font-semibold text-slate-500 uppercase tracking-wider block">
                Party / Reference:
              </span>
              <span className="font-bold text-slate-900 text-sm mt-0.5 block">
                {record.customer || record.supplier || record.party || record.account || 'Standard Ledger Account'}
              </span>
              <span className="text-slate-500 mt-1 block">
                Status: <strong className="text-emerald-700">{record.status || 'Submitted'}</strong>
              </span>
            </div>
            <div className="text-right">
              <span className="font-semibold text-slate-500 uppercase tracking-wider block">
                Transaction Value:
              </span>
              <span className="font-extrabold text-slate-900 text-lg mt-0.5 block font-mono">
                {record.grand_total || record.paid_amount || record.total_debit ?
                  `₹${Number(record.grand_total || record.paid_amount || record.total_debit).toLocaleString('en-IN')}` :
                  '₹1,25,000.00'}
              </span>
              <span className="text-slate-500 mt-1 block font-mono">
                Currency: INR (₹)
              </span>
            </div>
          </div>

          {/* Line Items Table */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Details & Line Item Allocation
            </h3>
            <table className="w-full text-left text-xs border border-slate-200">
              <thead className="bg-slate-100 border-b border-slate-200 font-semibold text-slate-700">
                <tr>
                  <th className="p-2.5">Description</th>
                  <th className="p-2.5 text-right">Qty</th>
                  <th className="p-2.5 text-right">Unit Rate (₹)</th>
                  <th className="p-2.5 text-right">Total (₹)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                <tr>
                  <td className="p-2.5 font-medium">Standard Operational Item - Financial Service Fulfillment</td>
                  <td className="p-2.5 text-right font-mono">1.00</td>
                  <td className="p-2.5 text-right font-mono">
                    {record.grand_total ? (record.grand_total * 0.85).toLocaleString('en-IN') : '1,05,932.00'}
                  </td>
                  <td className="p-2.5 text-right font-mono font-bold">
                    {record.grand_total ? (record.grand_total * 0.85).toLocaleString('en-IN') : '1,05,932.00'}
                  </td>
                </tr>
                <tr>
                  <td className="p-2.5 font-medium">Integrated Goods and Services Tax (IGST 18%)</td>
                  <td className="p-2.5 text-right font-mono">—</td>
                  <td className="p-2.5 text-right font-mono">18.00%</td>
                  <td className="p-2.5 text-right font-mono font-bold">
                    {record.grand_total ? (record.grand_total * 0.15).toLocaleString('en-IN') : '19,068.00'}
                  </td>
                </tr>
              </tbody>
              <tfoot className="bg-slate-50 font-bold border-t-2 border-slate-900">
                <tr>
                  <td colSpan={3} className="p-2.5 text-right">Grand Total:</td>
                  <td className="p-2.5 text-right font-mono text-sm">
                    {record.grand_total || record.paid_amount || record.total_debit ?
                      `₹${Number(record.grand_total || record.paid_amount || record.total_debit).toLocaleString('en-IN')}` :
                      '₹1,25,000.00'}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>

          {/* Signatures */}
          <div className="pt-12 grid grid-cols-2 gap-8 text-xs text-slate-500">
            <div>
              <div className="border-t border-slate-300 pt-2 font-medium">
                Prepared By: Finance Team (Admin)
              </div>
            </div>
            <div className="text-right">
              <div className="border-t border-slate-300 pt-2 font-medium">
                Authorized Signatory for CreditBridge Global Ltd
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
