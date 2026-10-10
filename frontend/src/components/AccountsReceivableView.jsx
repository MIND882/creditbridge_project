import React, { useEffect, useMemo } from 'react';
import {
  FileBarChart,
  ArrowLeft,
  Download,
  Filter,
  DollarSign,
  Clock,
  AlertTriangle,
  ChevronRight,
  TrendingUp,
  Building,
  Inbox
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function AccountsReceivableView({ onNavigate }) {
  const { getDomainRecords, fetchDomainRecords } = useRecords();

  useEffect(() => {
    fetchDomainRecords('sales_invoice');
  }, []);

  const salesInvoices = getDomainRecords('sales_invoice');

  // Compute Live Aging from Real Invoices
  const { agingBuckets, totalBalance } = useMemo(() => {
    const buckets = [
      { label: '0 - 30 Days', range: 'Current', amount: 0, count: 0, color: 'text-emerald-600 bg-emerald-50 border-emerald-200' },
      { label: '31 - 60 Days', range: 'Mild Overdue', amount: 0, count: 0, color: 'text-blue-600 bg-blue-50 border-blue-200' },
      { label: '61 - 90 Days', range: 'Warning', amount: 0, count: 0, color: 'text-amber-600 bg-amber-50 border-amber-200' },
      { label: '90+ Days', range: 'Critical', amount: 0, count: 0, color: 'text-rose-600 bg-rose-50 border-rose-200' }
    ];

    let total = 0;
    const now = new Date();

    salesInvoices.forEach(inv => {
      const amt = Number(inv.outstanding_amount !== undefined && inv.outstanding_amount !== null ? inv.outstanding_amount : (inv.grand_total || inv.total || 0)) || 0;
      total += amt;
      const invDate = inv.posting_date ? new Date(inv.posting_date) : (inv.created_at ? new Date(inv.created_at) : now);
      const diffDays = Math.floor((now - invDate) / (1000 * 60 * 60 * 24));

      if (diffDays <= 30) {
        buckets[0].amount += amt;
        buckets[0].count += 1;
      } else if (diffDays <= 60) {
        buckets[1].amount += amt;
        buckets[1].count += 1;
      } else if (diffDays <= 90) {
        buckets[2].amount += amt;
        buckets[2].count += 1;
      } else {
        buckets[3].amount += amt;
        buckets[3].count += 1;
      }
    });

    return { agingBuckets: buckets, totalBalance: total };
  }, [salesInvoices]);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate({ type: 'module_hub', module: 'Accounting' })}
              className="text-xs font-semibold text-slate-500 hover:text-slate-800"
            >
              ← Accounting Module
            </button>
            <span className="text-slate-300">•</span>
            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700">
              Financial Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Accounts Receivable Aging Report
          </h1>
          <p className="text-[13px] text-slate-500 max-w-2xl">
            Customer outstanding balances grouped by age buckets for credit control and cash collection forecasting.
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            onClick={() => onNavigate({ type: 'list', domain: 'sales_invoice' })}
            className="flex items-center gap-1.5 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-[13px] font-semibold rounded-xl transition-all shadow-xs"
          >
            <span>View Sales Invoices</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Aging Buckets Summary Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {agingBuckets.map((bucket, idx) => (
          <div
            key={idx}
            className="bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs space-y-2"
          >
            <div className="flex items-center justify-between">
              <span className="text-[12px] font-bold text-slate-700">{bucket.label}</span>
              <span className={`text-[10.5px] font-semibold px-2 py-0.5 rounded-full border ${bucket.color}`}>
                {bucket.range}
              </span>
            </div>
            <div className="text-2xl font-bold text-slate-900 tracking-tight">
              ₹{bucket.amount.toLocaleString('en-IN')}
            </div>
            <div className="text-[11.5px] text-slate-500">
              {bucket.count} invoices in this bucket
            </div>
          </div>
        ))}
      </div>

      {/* Customer Aging Breakdown Table */}
      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-2xs space-y-4 p-6">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h2 className="text-base font-bold text-slate-900">Live Customer Balance Breakdown</h2>
            <p className="text-[12px] text-slate-500">Computed directly from active sales invoices in PostgreSQL</p>
          </div>
          <span className="text-sm font-bold text-slate-900">
            Total Outstanding: <span className="text-indigo-600">₹{totalBalance.toLocaleString('en-IN')}</span>
          </span>
        </div>

        {salesInvoices.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[13px]">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3">Invoice / Customer</th>
                  <th className="px-4 py-3">Date</th>
                  <th className="px-4 py-3 text-right">Invoice Amount</th>
                  <th className="px-4 py-3 text-right">Outstanding</th>
                  <th className="px-4 py-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {salesInvoices.map((inv, idx) => (
                  <tr key={idx} className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-3.5 font-semibold text-slate-900">
                      <div className="flex items-center gap-2">
                        <Building className="w-3.5 h-3.5 text-slate-400" />
                        <div>
                          <div>{inv.customer || inv.customer_name || 'Customer'}</div>
                          <div className="text-[11px] text-slate-400 font-normal">{inv.name || inv.id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-slate-600">
                      {inv.posting_date || (inv.created_at ? inv.created_at.slice(0, 10) : '—')}
                    </td>
                    <td className="px-4 py-3.5 text-right font-mono text-slate-900 font-bold">
                      ₹{Number(inv.grand_total || inv.total || 0).toLocaleString('en-IN')}
                    </td>
                    <td className="px-4 py-3.5 text-right font-mono text-indigo-700 font-bold">
                      ₹{Number(inv.outstanding_amount || inv.grand_total || 0).toLocaleString('en-IN')}
                    </td>
                    <td className="px-4 py-3.5 text-center">
                      <span className="text-[10.5px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                        {inv.status || 'Active'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-12 text-center space-y-3">
            <Inbox className="w-10 h-10 text-slate-300 mx-auto" />
            <div className="text-sm font-semibold text-slate-700">No Sales Invoices in Database Yet</div>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Once you post sales invoices in the Sales Invoice domain, live aging buckets and customer balances will compute automatically.
            </p>
            <button
              onClick={() => onNavigate({ type: 'form', domain: 'sales_invoice' })}
              className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold shadow-xs"
            >
              + Create First Sales Invoice
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
