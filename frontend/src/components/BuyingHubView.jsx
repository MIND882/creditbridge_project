import React, { useState, useMemo } from 'react';
import {
  ShoppingBag,
  Truck,
  FileText,
  Package,
  Layers,
  Settings,
  Search,
  Plus,
  ArrowRight,
  TrendingDown,
  Sparkles,
  ExternalLink,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Award
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function BuyingHubView({ onNavigate }) {
  const { domains, getDomainRecords } = useRecords();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  // Filter only Buying module domains
  const buyingDomains = useMemo(() => {
    return domains.filter(d => d.module === 'Buying');
  }, [domains]);

  const categories = useMemo(() => {
    const set = new Set();
    buyingDomains.forEach(d => {
      if (d.category) set.add(d.category);
    });
    return ['All', ...Array.from(set)];
  }, [buyingDomains]);

  const filteredDomains = useMemo(() => {
    return buyingDomains.filter(d => {
      const matchCat = selectedCategory === 'All' || d.category === selectedCategory;
      const matchSearch =
        d.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (d.description && d.description.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchCat && matchSearch;
    });
  }, [buyingDomains, selectedCategory, searchQuery]);

  // Aggregate Buying metrics
  const metrics = useMemo(() => {
    const suppliers = getDomainRecords('supplier') || [];
    const purchaseOrders = getDomainRecords('purchase_order') || [];
    const rfqs = getDomainRecords('request_for_quotation') || [];

    const totalPOValue = purchaseOrders.reduce((sum, po) => sum + (Number(po.grand_total) || 0), 0);
    const pendingReceiptCount = purchaseOrders.filter(po => po.status === 'To Receive and Bill' || po.status === 'To Receive').length;

    return {
      supplierCount: suppliers.length,
      poCount: purchaseOrders.length,
      rfqCount: rfqs.length,
      totalPOValue,
      pendingReceiptCount
    };
  }, [getDomainRecords]);

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6 animate-fadeIn pb-12">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white rounded-2xl p-6 shadow-lg relative overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 px-3 py-1 bg-white/10 backdrop-blur-md rounded-full text-xs font-semibold tracking-wide uppercase text-emerald-300 mb-2">
              <ShoppingBag className="w-3.5 h-3.5" />
              <span>Procurement & Supplier Management</span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight">Buying Module Hub</h1>
            <p className="text-slate-300 text-sm mt-1 max-w-2xl">
              Manage all 19 ERPNext cloud procurement domains: Purchase Orders, RFQs, Supplier Quotations, Vendor Scorecards, and Live Database Tables.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => onNavigate?.({ type: 'form', domain: 'supplier', module: 'Buying' })}
              className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white text-sm font-semibold rounded-xl shadow-md transition flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>New Supplier</span>
            </button>
            <button
              onClick={() => onNavigate?.({ type: 'form', domain: 'purchase_order', module: 'Buying' })}
              className="px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white text-sm font-semibold rounded-xl backdrop-blur-md border border-white/20 transition flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>New Purchase Order</span>
            </button>
          </div>
        </div>

        {/* Live Procurement Metrics Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-white/10">
          <div className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <span className="text-xs text-slate-300 font-medium">Total PO Spend</span>
            <div className="text-2xl font-bold font-mono text-emerald-300 mt-1">
              ₹{metrics.totalPOValue.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
            </div>
            <span className="text-[11px] text-slate-400 mt-0.5 block">Approved procurement</span>
          </div>

          <div className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <span className="text-xs text-slate-300 font-medium">Active Suppliers</span>
            <div className="text-2xl font-bold font-mono text-white mt-1">
              {metrics.supplierCount}
            </div>
            <span className="text-[11px] text-emerald-400 mt-0.5 block">Registered vendor masters</span>
          </div>

          <div className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <span className="text-xs text-slate-300 font-medium">Pending Delivery</span>
            <div className="text-2xl font-bold font-mono text-amber-300 mt-1">
              {metrics.pendingReceiptCount}
            </div>
            <span className="text-[11px] text-slate-400 mt-0.5 block">Awaiting goods receipt</span>
          </div>

          <div className="bg-white/5 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <span className="text-xs text-slate-300 font-medium">Active RFQs</span>
            <div className="text-2xl font-bold font-mono text-teal-300 mt-1">
              {metrics.rfqCount}
            </div>
            <span className="text-[11px] text-slate-400 mt-0.5 block">Tenders in bidding</span>
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-4 rounded-xl border shadow-sm">
        <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0">
          {categories.map((cat, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                selectedCategory === cat
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search 19 buying domains..."
            className="w-full pl-9 pr-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-emerald-500 outline-none"
          />
        </div>
      </div>

      {/* Domains Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredDomains.map((domain, idx) => {
          const recs = getDomainRecords(domain.name) || [];
          const recordCount = recs.length;

          return (
            <div
              key={domain.name || idx}
              className="bg-white rounded-xl border p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full">
                    {domain.category || 'Buying'}
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    {recordCount} record{recordCount !== 1 ? 's' : ''}
                  </span>
                </div>

                <h3 className="text-base font-bold text-slate-900 group-hover:text-emerald-700 transition">
                  {domain.label}
                </h3>
                <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                  {domain.description || `Manage ${domain.label} per ERPNext cloud procurement standard.`}
                </p>

                <div className="mt-4 pt-3 border-t text-[11px] text-slate-400 flex items-center justify-between font-mono">
                  <span>{domain.fields?.length || 0} columns</span>
                  <span>{domain.backend?.table || `${domain.name}s`}</span>
                </div>
              </div>

              <div className="flex items-center space-x-2 mt-4 pt-3 border-t">
                <button
                  onClick={() => onNavigate?.({ type: 'list', domain: domain.name, module: 'Buying' })}
                  className="flex-1 py-1.5 bg-slate-50 hover:bg-slate-100 text-slate-700 font-medium text-xs rounded-lg transition flex items-center justify-center space-x-1"
                >
                  <span>View List</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => onNavigate?.({ type: 'form', domain: domain.name, module: 'Buying' })}
                  className="p-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg transition"
                  title={`New ${domain.label}`}
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
