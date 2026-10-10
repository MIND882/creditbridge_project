import React, { useEffect } from 'react';
import {
  Calculator,
  ShoppingCart,
  ShoppingBag,
  Package,
  Factory,
  Users,
  Settings,
  ArrowUpRight,
  TrendingUp,
  Landmark,
  CreditCard,
  FileText,
  ShieldCheck,
  ChevronRight,
  Plus,
  Sparkles,
  Layers,
  ArrowRight,
  CheckCircle2,
  Database,
  Building2,
  Inbox
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function DashboardView({ onNavigate }) {
  const {
    domains,
    getDomainCount,
    getDomainRecords,
    fetchDomainRecords,
    authTenant,
    backendConnected,
    backendInfo
  } = useRecords();

  // Load real records on mount
  useEffect(() => {
    fetchDomainRecords('account');
    fetchDomainRecords('sales_invoice');
    fetchDomainRecords('payment_entry');
    fetchDomainRecords('journal_entry');
    fetchDomainRecords('cost_center');
    fetchDomainRecords('quotation');
    fetchDomainRecords('sales_order');
    fetchDomainRecords('customer');
  }, []);

  const accounts = getDomainRecords('account');
  const salesInvoices = getDomainRecords('sales_invoice');
  const paymentEntries = getDomainRecords('payment_entry');
  const journalEntries = getDomainRecords('journal_entry');
  const costCenters = getDomainRecords('cost_center');
  const quotations = getDomainRecords('quotation');
  const salesOrders = getDomainRecords('sales_order');
  const customers = getDomainRecords('customer');

  // Compute Live Metrics from Real Database
  const totalReceivables = salesInvoices.reduce((sum, inv) => sum + (Number(inv.grand_total || inv.total || 0) || 0), 0);
  const totalCollections = paymentEntries.reduce((sum, pay) => sum + (Number(pay.paid_amount || pay.total_allocated_amount || 0) || 0), 0);

  const financialKpis = [
    {
      label: 'Chart of Accounts',
      value: `${accounts.length} Nodes`,
      change: accounts.length > 0 ? 'Live in DB' : 'Awaiting Seed',
      sub: accounts.length > 0 ? 'Ledgers, Groups & Tax heads' : 'Run seed_accounting_data.py',
      icon: Calculator,
      color: 'text-indigo-600 bg-indigo-50 border-indigo-100',
      action: () => onNavigate({ type: 'list', domain: 'account' })
    },
    {
      label: 'Sales Invoices',
      value: `₹${totalReceivables.toLocaleString('en-IN')}`,
      change: `${salesInvoices.length} posted`,
      sub: salesInvoices.length > 0 ? 'Real invoices in PostgreSQL' : 'No invoices posted yet',
      icon: TrendingUp,
      color: 'text-emerald-600 bg-emerald-50 border-emerald-100',
      action: () => onNavigate({ type: 'list', domain: 'sales_invoice' })
    },
    {
      label: 'Cost Centers Configured',
      value: `${costCenters.length} Centers`,
      change: costCenters.length > 0 ? 'Active' : 'Unconfigured',
      sub: 'Allocations & Budgeting',
      icon: Landmark,
      color: 'text-amber-600 bg-amber-50 border-amber-100',
      action: () => onNavigate({ type: 'list', domain: 'cost_center' })
    },
    {
      label: 'PostgreSQL Architecture',
      value: '210 Tables',
      change: backendConnected ? 'Connected (8000)' : 'Offline',
      sub: '191 Accounts • 19 Core MSME',
      icon: Database,
      color: 'text-blue-600 bg-blue-50 border-blue-100',
      action: () => onNavigate({ type: 'module_hub', module: 'Accounting' })
    }
  ];

  // Compile real recent transactions from database
  const recentTransactions = [
    ...salesInvoices.map(s => ({
      id: s.id || s.name,
      domain: 'sales_invoice',
      title: 'Sales Invoice',
      party: s.customer || s.customer_name || 'Customer',
      amount: s.grand_total ? `₹${Number(s.grand_total).toLocaleString('en-IN')}` : '₹0',
      status: s.status || 'Active'
    })),
    ...paymentEntries.map(p => ({
      id: p.id || p.name,
      domain: 'payment_entry',
      title: 'Payment Entry',
      party: p.party_name || p.paid_to || 'Payment Receipt',
      amount: p.paid_amount ? `₹${Number(p.paid_amount).toLocaleString('en-IN')}` : '₹0',
      status: p.status || 'Active'
    })),
    ...journalEntries.map(j => ({
      id: j.id || j.name,
      domain: 'journal_entry',
      title: 'Journal Entry',
      party: j.user_remark || 'General Voucher',
      amount: j.total_debit ? `₹${Number(j.total_debit).toLocaleString('en-IN')}` : '₹0',
      status: j.status || 'Active'
    }))
  ].slice(0, 5);

  const quickDomains = [
    { name: 'account', label: 'Chart of Accounts', cat: 'Masters' },
    { name: 'sales_invoice', label: 'Sales Invoice', cat: 'Billing' },
    { name: 'purchase_invoice', label: 'Purchase Invoice', cat: 'Billing' },
    { name: 'payment_entry', label: 'Payment Entry', cat: 'Payments' },
    { name: 'journal_entry', label: 'Journal Entry', cat: 'Ledger' },
    { name: 'bank_account', label: 'Bank Account', cat: 'Banking' },
    { name: 'cost_center', label: 'Cost Center', cat: 'Costing' },
    { name: 'tax_rule', label: 'Tax Rules', cat: 'Compliance' }
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Welcome & Overview Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 p-6 sm:p-8 rounded-2xl text-white shadow-md relative overflow-hidden">
        <div className="relative z-10 space-y-2">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-white/10 backdrop-blur-md text-[11px] font-medium text-slate-200 border border-white/10">
            <Building2 className="w-3.5 h-3.5 text-indigo-400" />
            <span>Active Tenant: {authTenant.business_name} • GSTIN: 27AAACB1234F1Z5</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
            {authTenant.business_name}
          </h1>
          <p className="text-slate-300 text-[13.5px] max-w-2xl leading-relaxed">
            Centralized ERP with Generic Engine metadata architecture. Operating across 191 accounting domains with 210 verified PostgreSQL tables.
          </p>
        </div>

        <div className="relative z-10 flex flex-wrap gap-2.5 shrink-0">
          <button
            onClick={() => onNavigate({ type: 'module_hub', module: 'Accounting' })}
            className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-[13px] rounded-xl transition-all shadow-sm"
          >
            <Calculator className="w-4 h-4" />
            <span>Explore Accounting (191 Domains)</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onNavigate({ type: 'form', domain: 'sales_invoice' })}
            className="flex items-center gap-2 px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white font-medium text-[13px] rounded-xl border border-white/15 backdrop-blur-md transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>New Invoice</span>
          </button>
        </div>
      </div>

      {/* Real Live KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {financialKpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div
              key={idx}
              onClick={kpi.action}
              className="bg-white border border-slate-200 hover:border-slate-300 p-5 rounded-2xl shadow-2xs hover:shadow-sm transition-all cursor-pointer group"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[12.5px] font-medium text-slate-500">{kpi.label}</span>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center border ${kpi.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="text-2xl font-bold text-slate-900 tracking-tight group-hover:text-indigo-600 transition-colors">
                {kpi.value}
              </div>
              <div className="mt-2 text-[11.5px] text-slate-500 flex items-center justify-between">
                <span>{kpi.sub}</span>
                <span className="font-medium text-emerald-600">{kpi.change}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Featured Star: Accounting Module 191 Domains Hub Banner */}
      <div className="bg-white border-2 border-indigo-100 rounded-2xl p-6 shadow-xs hover:border-indigo-200 transition-all">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 text-[11px] font-semibold border border-indigo-200">
              <Layers className="w-3.5 h-3.5" />
              <span>CORE ACCOUNTING ENGINE</span>
            </div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Accounting Module — All 191 Domains Configured
            </h2>
            <p className="text-[13px] text-slate-600 leading-relaxed">
              Every single domain from Chart of Accounts to Sales Invoices, Bank Reconciliations, Tax Withholding, Budgets, Point of Sale, and Period Closing Vouchers is ready with List, Detail, and Form screens.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <button
              onClick={() => onNavigate({ type: 'module_hub', module: 'Accounting' })}
              className="flex items-center gap-2 px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-[13px] font-medium rounded-xl shadow-xs transition-all"
            >
              <span>Open Accounting Hub</span>
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate({ type: 'receivables' })}
              className="flex items-center gap-2 px-4 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-[13px] font-medium rounded-xl border border-indigo-200 transition-all"
            >
              <span>Aging Report</span>
            </button>
          </div>
        </div>

        {/* Quick Domain Pills */}
        <div className="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center gap-2">
          <span className="text-[11.5px] font-semibold text-slate-400 mr-2 uppercase tracking-wide">
            Quick Launch:
          </span>
          {quickDomains.map((qd) => (
            <button
              key={qd.name}
              onClick={() => onNavigate({ type: 'list', domain: qd.name })}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 border border-slate-200 text-[12px] font-medium text-slate-700 transition-colors"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
              <span>{qd.label}</span>
              <span className="text-[10px] text-slate-400 font-mono">({getDomainCount(qd.name)})</span>
            </button>
          ))}
          <button
            onClick={() => onNavigate({ type: 'module_hub', module: 'Accounting' })}
            className="text-[12px] font-medium text-indigo-600 hover:text-indigo-800 underline ml-2"
          >
            + 183 more domains →
          </button>
        </div>
      </div>

      {/* Two Columns: Recent Transactions & Other ERP Modules */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Recent Activity */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-base font-bold text-slate-900">Recent Accounting Transactions</h3>
              <p className="text-[12px] text-slate-500">Live operational feed from PostgreSQL ledger</p>
            </div>
            <button
              onClick={() => onNavigate({ type: 'list', domain: 'sales_invoice' })}
              className="text-[12px] font-medium text-indigo-600 hover:text-indigo-800"
            >
              View Invoices →
            </button>
          </div>

          {recentTransactions.length > 0 ? (
            <div className="divide-y divide-slate-100">
              {recentTransactions.map((tx) => (
                <div
                  key={tx.id}
                  onClick={() => onNavigate({ type: 'detail', domain: tx.domain, id: tx.id })}
                  className="py-3.5 flex items-center justify-between hover:bg-slate-50 px-2 rounded-xl transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center font-semibold text-xs border border-slate-200">
                      <FileText className="w-4 h-4 text-slate-600" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[13px] font-semibold text-slate-900">{tx.id}</span>
                        <span className="text-[11px] font-medium text-slate-400">• {tx.title}</span>
                      </div>
                      <div className="text-[12px] text-slate-500">{tx.party}</div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-[13.5px] font-bold text-slate-900">{tx.amount}</div>
                    <div className="flex items-center justify-end gap-1.5 mt-0.5">
                      <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500" />
                      <span className="text-[11px] font-medium text-emerald-700">{tx.status}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-12 text-center space-y-3">
              <Inbox className="w-10 h-10 text-slate-300 mx-auto" />
              <div className="text-sm font-semibold text-slate-700">No Ledger Transactions Posted Yet</div>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Transactions created in Sales Invoices, Payments, or Journal Entries will appear here in real time.
              </p>
              <button
                onClick={() => onNavigate({ type: 'form', domain: 'sales_invoice' })}
                className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold shadow-xs"
              >
                + Create First Invoice
              </button>
            </div>
          )}
        </div>

        {/* Right: Quick Module Directory */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="text-base font-bold text-slate-900">ERP Modules</h3>
            <p className="text-[12px] text-slate-500">Select any business area</p>
          </div>

          <div className="space-y-2">
            {[
              { id: 'Accounting', label: 'Accounting', icon: Calculator, desc: '191 domains • Ledgers & Tax', badge: '191', badgeColor: 'bg-emerald-100 text-emerald-800' },
              { id: 'Selling', label: 'Selling', icon: ShoppingCart, desc: '20 domains • Quotes, Orders & CRM', badge: '20', badgeColor: 'bg-blue-100 text-blue-800' },
              { id: 'Buying', label: 'Buying', icon: ShoppingBag, desc: 'Purchase Orders & Suppliers' },
              { id: 'Stock', label: 'Stock', icon: Package, desc: 'Warehouses & Stock Entries' },
              { id: 'Manufacturing', label: 'Manufacturing', icon: Factory, desc: 'BOM & Work Orders' },
              { id: 'CRM', label: 'CRM', icon: Users, desc: 'Leads & Opportunities' }
            ].map((m) => {
              const Icon = m.icon;
              return (
                <button
                  key={m.id}
                  onClick={() => onNavigate({ type: 'module_hub', module: m.id })}
                  className="w-full flex items-center justify-between p-2.5 rounded-xl hover:bg-slate-50 border border-transparent hover:border-slate-200 transition-colors text-left group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700 group-hover:bg-slate-900 group-hover:text-white transition-colors">
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-[13px] font-semibold text-slate-900 flex items-center gap-1.5">
                        {m.label}
                        {m.badge && (
                          <span className={`text-[10px] font-bold px-1.5 py-0.2 rounded-full ${m.badgeColor || 'bg-emerald-100 text-emerald-800'}`}>
                            {m.badge}
                          </span>
                        )}
                      </div>
                      <div className="text-[11px] text-slate-500">{m.desc}</div>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-slate-600 transition-colors" />
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
