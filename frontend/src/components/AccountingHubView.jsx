import React, { useState, useMemo, useEffect } from 'react';
import BackendInspector from './BackendInspector';
import {
  Calculator,
  Search,
  Filter,
  Layers,
  ArrowRight,
  ArrowLeft,
  Plus,
  Eye,
  FileText,
  FileBarChart,
  CheckCircle2,
  SlidersHorizontal,
  ChevronRight,
  Sparkles,
  LayoutGrid,
  List,
  Server,
  RotateCw
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function AccountingHubView({ onNavigate }) {
  const { domains, getDomainCount, getDomainRecords, fetchDomainRecords, loadingRecords } = useRecords();

  // Search, filter & view states
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedType, setSelectedType] = useState('All');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'table'

  // Domain-by-Domain Stepper (index 0 to 190)
  const [stepperIndex, setStepperIndex] = useState(0);
  const [showBackendSpecs, setShowBackendSpecs] = useState(false);

  // Auto-fetch key domains once on mount
  useEffect(() => {
    fetchDomainRecords('account');
    fetchDomainRecords('cost_center');
    fetchDomainRecords('mode_of_payment');
  }, []);

  const currentStepDomain = domains[stepperIndex] || domains[0];

  // Auto-fetch whenever stepper moves to a domain
  useEffect(() => {
    if (currentStepDomain?.name) {
      fetchDomainRecords(currentStepDomain.name);
    }
  }, [stepperIndex]);

  const categories = [
    'All',
    'Invoicing & Billing',
    'Payments & Cash',
    'Banking & Reconciliation',
    'General Ledger & Journal',
    'Chart of Accounts & Masters',
    'Taxes & Compliance',
    'Budgets & Cost Centers',
    'Point of Sale (POS)',
    'Subscriptions & Pricing',
    'Shares & Equity',
    'Dunning & Shipping',
    'Setup & Advanced'
  ];

  const types = ['All', 'Transaction', 'Master', 'Setting', 'Tool', 'Child Table'];

  // Filtered domains
  const filteredDomains = useMemo(() => {
    return domains.filter(d => {
      const matchesSearch = !searchTerm ||
        d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        d.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
        d.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        d.category.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesCat = selectedCategory === 'All' || d.category === selectedCategory;
      const matchesType = selectedType === 'All' || d.type === selectedType;

      return matchesSearch && matchesCat && matchesType;
    });
  }, [domains, searchTerm, selectedCategory, selectedType]);

  const handlePrevStep = () => {
    setStepperIndex(prev => (prev > 0 ? prev - 1 : domains.length - 1));
  };

  const handleNextStep = () => {
    setStepperIndex(prev => (prev < domains.length - 1 ? prev + 1 : 0));
  };

  const getTypeBadgeColor = (type) => {
    switch (type) {
      case 'Transaction':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'Master':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Setting':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'Tool':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Child Table':
        return 'bg-slate-100 text-slate-700 border-slate-300';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Module Hub Top Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs relative overflow-hidden">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-[11.5px] font-semibold">
              <Calculator className="w-3.5 h-3.5" />
              <span>ERPNext Core Architecture • 191 Domains Ready</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              Accounting & Financial Management
            </h1>
            <p className="text-slate-600 text-[13.5px] max-w-3xl leading-relaxed">
              Complete Double-Entry Ledger, Sales & Purchase Invoicing, Bank Reconciliation, Tax Compliance, Cost Centers, Multi-Currency, POS, Subscriptions, and Equity Tracking.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <button
              onClick={() => {
                fetchDomainRecords('account');
                fetchDomainRecords('cost_center');
                fetchDomainRecords('mode_of_payment');
              }}
              disabled={loadingRecords}
              className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-[13px] rounded-xl transition-all shadow-xs"
              title="Sync live records from PostgreSQL"
            >
              <RotateCw className={`w-4 h-4 ${loadingRecords ? 'animate-spin' : ''}`} />
              <span>{loadingRecords ? 'Syncing...' : 'Sync Live DB Data'}</span>
            </button>
            <button
              onClick={() => onNavigate({ type: 'receivables' })}
              className="flex items-center gap-2 px-4 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-medium text-[13px] rounded-xl border border-indigo-200 transition-colors shadow-2xs"
            >
              <FileBarChart className="w-4 h-4" />
              <span>Receivables Aging</span>
            </button>
            <button
              onClick={() => onNavigate({ type: 'form', domain: 'sales_invoice' })}
              className="flex items-center gap-2 px-4 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium text-[13px] rounded-xl transition-all shadow-xs"
            >
              <Plus className="w-4 h-4" />
              <span>New Sales Invoice</span>
            </button>
          </div>
        </div>

        {/* Domain Metrics Strip */}
        <div className="mt-6 pt-5 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
            <div className="text-[11px] font-medium text-slate-500 uppercase">Total Domains</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">191</div>
            <div className="text-[10.5px] text-emerald-600 font-medium">100% Configured</div>
          </div>
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
            <div className="text-[11px] font-medium text-slate-500 uppercase">Transactions</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">31</div>
            <div className="text-[10.5px] text-blue-600 font-medium">Submittable ledgers</div>
          </div>
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
            <div className="text-[11px] font-medium text-slate-500 uppercase">Masters</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">21</div>
            <div className="text-[10.5px] text-emerald-600 font-medium">Accounts, Parties</div>
          </div>
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
            <div className="text-[11px] font-medium text-slate-500 uppercase">Banking & Cash</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">17</div>
            <div className="text-[10.5px] text-indigo-600 font-medium">Reconciliation tools</div>
          </div>
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
            <div className="text-[11px] font-medium text-slate-500 uppercase">Tax & Compliance</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">16</div>
            <div className="text-[10.5px] text-purple-600 font-medium">GST, TDS, Rules</div>
          </div>
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3">
            <div className="text-[11px] font-medium text-slate-500 uppercase">Budgets & Centers</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">9</div>
            <div className="text-[10.5px] text-amber-600 font-medium">Variance control</div>
          </div>
        </div>
      </div>

      {/* ONE-BY-ONE DOMAIN EXPLORER & BUILDER TOOLBAR */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 rounded-2xl p-6 text-white shadow-md space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs border border-emerald-500/30">
              #
            </div>
            <div>
              <div className="text-[13.5px] font-bold text-white flex items-center gap-2">
                Domain-by-Domain Frontend Navigator
                <span className="text-[10.5px] font-semibold px-2 py-0.2 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                  Domain {stepperIndex + 1} of {domains.length}
                </span>
              </div>
              <div className="text-[11.5px] text-slate-300">
                Inspect, create, or edit any domain one by one across all 191 doctypes.
              </div>
            </div>
          </div>

          {/* Stepper Controls */}
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrevStep}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-[12px] font-medium transition-colors border border-white/10"
              title="Previous Domain"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Prev Domain</span>
            </button>

            {/* Direct Selector Dropdown */}
            <select
              value={stepperIndex}
              onChange={(e) => setStepperIndex(Number(e.target.value))}
              className="bg-white/10 hover:bg-white/20 text-white text-[12px] font-medium rounded-lg px-3 py-1.5 border border-white/10 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              {domains.map((d, i) => (
                <option key={d.name} value={i} className="bg-slate-900 text-white">
                  #{i + 1}: {d.label} ({d.type})
                </option>
              ))}
            </select>

            <button
              onClick={handleNextStep}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-[12px] font-medium transition-colors border border-white/10"
              title="Next Domain"
            >
              <span>Next Domain</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Current Domain Spotlight Card */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-lg font-bold text-white tracking-tight">
                #{stepperIndex + 1}. {currentStepDomain.label}
              </span>
              <code className="text-[11px] font-mono px-2 py-0.5 rounded bg-black/30 text-indigo-200">
                {currentStepDomain.name}
              </code>
              <span className={`text-[10.5px] font-semibold px-2 py-0.5 rounded-full border ${getTypeBadgeColor(currentStepDomain.type)}`}>
                {currentStepDomain.type}
              </span>
              <span className="text-[10.5px] font-medium px-2 py-0.5 rounded-full bg-white/10 text-slate-200 border border-white/10">
                {currentStepDomain.category}
              </span>
            </div>
            <p className="text-[12.5px] text-slate-200 max-w-2xl">
              {currentStepDomain.description}
            </p>
            <div className="flex items-center gap-4 text-[11px] text-slate-300 pt-1">
              <span className="font-semibold text-emerald-300">
                {getDomainCount(currentStepDomain.name)} Records in Database
              </span>
              <span>•</span>
              <span>{currentStepDomain.fields.length} Fields Configured</span>
              <span>•</span>
              <span>{currentStepDomain.sections.length} Form Sections</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 shrink-0">
            <button
              onClick={() => fetchDomainRecords(currentStepDomain.name)}
              disabled={loadingRecords}
              className="flex items-center gap-1.5 px-3 py-2 bg-white/10 hover:bg-white/20 text-white font-medium text-[12.5px] rounded-lg border border-white/10 transition-all shadow-xs"
              title="Refresh this domain's records from PostgreSQL"
            >
              <RotateCw className={`w-3.5 h-3.5 ${loadingRecords ? 'animate-spin' : ''}`} />
              <span>Sync</span>
            </button>

            <button
              onClick={() => setShowBackendSpecs(prev => !prev)}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-indigo-600/60 hover:bg-indigo-600 text-white font-semibold text-[12.5px] rounded-lg border border-indigo-400/40 transition-all shadow-xs"
              title="Inspect FastAPI Routes & SQLAlchemy Table"
            >
              <Server className="w-3.5 h-3.5" />
              <span>{showBackendSpecs ? 'Hide Backend Specs' : 'Backend API & DB'}</span>
            </button>

            <button
              onClick={() => onNavigate({ type: 'list', domain: currentStepDomain.name })}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-[12.5px] rounded-lg transition-all shadow-xs"
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Open List View</span>
            </button>

            <button
              onClick={() => onNavigate({ type: 'form', domain: currentStepDomain.name })}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-white/15 hover:bg-white/25 text-white font-medium text-[12.5px] rounded-lg border border-white/15 transition-all"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>+ New Record</span>
            </button>

            {getDomainCount(currentStepDomain.name) > 0 && (
              <button
                onClick={() => {
                  const records = getDomainRecords(currentStepDomain.name);
                  onNavigate({ type: 'detail', domain: currentStepDomain.name, id: records[0].id || records[0].name });
                }}
                className="flex items-center gap-1.5 px-3 py-2 bg-white/10 hover:bg-white/20 text-white font-medium text-[12.5px] rounded-lg border border-white/10 transition-all"
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Detail View</span>
              </button>
            )}
          </div>
        </div>

        {/* Backend Inspector Embedded */}
        {showBackendSpecs && (
          <div className="pt-2">
            <BackendInspector
              domain={currentStepDomain}
              isOpen={true}
              onToggle={() => setShowBackendSpecs(false)}
            />
          </div>
        )}
      </div>

      {/* Category Tabs */}
      <div className="space-y-4">
        <div className="flex items-center justify-between pb-1">
          <div className="text-[13px] font-semibold text-slate-900 flex items-center gap-2">
            <span>Domain Categories</span>
            <span className="text-[11px] font-normal text-slate-500">
              ({filteredDomains.length} showing of 191)
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg border text-xs ${
                viewMode === 'grid'
                  ? 'bg-slate-900 text-white border-slate-900'
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              }`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-lg border text-xs ${
                viewMode === 'table'
                  ? 'bg-slate-900 text-white border-slate-900'
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              }`}
              title="Table View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Category Pills Slider */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-2 scrollbar-none">
          {categories.map((cat) => {
            const count = cat === 'All'
              ? domains.length
              : domains.filter(d => d.category === cat).length;
            const active = selectedCategory === cat;

            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`whitespace-nowrap px-3 py-1.5 rounded-lg text-[12px] font-medium transition-colors shrink-0 flex items-center gap-1.5 border ${
                  active
                    ? 'bg-slate-900 text-white border-slate-900 shadow-2xs'
                    : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <span>{cat}</span>
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  active ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-500'
                }`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Search Bar & Type Filter */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search across all 191 domains by name, doctype, description..."
              className="w-full pl-9 pr-4 py-2 text-[13px] bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-900 placeholder:text-slate-400"
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[11px] text-slate-400 hover:text-slate-600 font-medium"
              >
                Clear
              </button>
            )}
          </div>

          <div className="flex items-center gap-1.5 overflow-x-auto">
            <span className="text-[11.5px] font-medium text-slate-400 shrink-0 mr-1">Type:</span>
            {types.map((t) => (
              <button
                key={t}
                onClick={() => setSelectedType(t)}
                className={`px-2.5 py-1.5 rounded-lg text-[11.5px] font-medium whitespace-nowrap transition-colors ${
                  selectedType === t
                    ? 'bg-indigo-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* DOMAIN DIRECTORY RENDERING */}
      {viewMode === 'grid' ? (
        /* Cards Grid View */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredDomains.map((domain) => {
            const count = getDomainCount(domain.name);
            return (
              <div
                key={domain.name}
                className="bg-white border border-slate-200 hover:border-slate-300 rounded-xl p-4 shadow-2xs hover:shadow-xs transition-all flex flex-col justify-between group"
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <span className="text-[11px] font-mono text-slate-400 font-semibold">
                        #{domain.index}
                      </span>
                      <h3
                        onClick={() => onNavigate({ type: 'list', domain: domain.name })}
                        className="text-[14px] font-bold text-slate-900 group-hover:text-indigo-600 transition-colors truncate cursor-pointer"
                        title={domain.label}
                      >
                        {domain.label}
                      </h3>
                    </div>

                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border shrink-0 ${getTypeBadgeColor(domain.type)}`}>
                      {domain.type}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <code className="text-[11px] font-mono text-slate-500 bg-slate-50 px-1.5 py-0.5 rounded border border-slate-200 truncate">
                      {domain.backend?.api_prefix || `/v1/${domain.name}`}
                    </code>
                    <span className="text-[11px] text-slate-400">•</span>
                    <span className="text-[11px] font-medium text-slate-500 truncate">
                      {domain.backend?.table_name || domain.name}
                    </span>
                  </div>

                  <p className="text-[12px] text-slate-600 line-clamp-2 leading-relaxed">
                    {domain.description}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                  <div className="text-[11.5px] font-semibold text-slate-500">
                    {count} <span className="font-normal text-slate-400">records</span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => onNavigate({ type: 'list', domain: domain.name })}
                      className="px-2.5 py-1 text-[11.5px] font-medium rounded-md bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors"
                    >
                      List View
                    </button>
                    <button
                      onClick={() => onNavigate({ type: 'form', domain: domain.name })}
                      className="px-2 py-1 text-[11.5px] font-medium rounded-md bg-indigo-50 text-indigo-700 hover:bg-indigo-100 transition-colors flex items-center gap-1"
                      title="Create New"
                    >
                      <Plus className="w-3 h-3" />
                      <span>New</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Detailed Table View */
        <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[12.5px]">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3 w-16">#</th>
                  <th className="px-4 py-3">Domain Label</th>
                  <th className="px-4 py-3">Technical DocType</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3 text-right">Records</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredDomains.map((domain) => {
                  const count = getDomainCount(domain.name);
                  return (
                    <tr key={domain.name} className="hover:bg-slate-50 transition-colors">
                      <td className="px-4 py-3 font-mono text-slate-400 font-medium">
                        {domain.index}
                      </td>
                      <td className="px-4 py-3 font-semibold text-slate-900">
                        <button
                          onClick={() => onNavigate({ type: 'list', domain: domain.name })}
                          className="hover:text-indigo-600 transition-colors text-left"
                        >
                          {domain.label}
                        </button>
                        <div className="text-[11px] text-slate-400 truncate max-w-xs font-normal">
                          {domain.description}
                        </div>
                      </td>
                      <td className="px-4 py-3 font-mono text-slate-600">
                        {domain.name}
                      </td>
                      <td className="px-4 py-3 text-slate-600 font-medium">
                        {domain.category}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${getTypeBadgeColor(domain.type)}`}>
                          {domain.type}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right font-medium text-slate-700">
                        {count}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => onNavigate({ type: 'list', domain: domain.name })}
                            className="px-2.5 py-1 text-[11px] font-medium rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700"
                          >
                            List
                          </button>
                          <button
                            onClick={() => onNavigate({ type: 'form', domain: domain.name })}
                            className="px-2 py-1 text-[11px] font-medium rounded-md bg-indigo-50 hover:bg-indigo-100 text-indigo-700 flex items-center gap-1"
                          >
                            <Plus className="w-3 h-3" />
                            <span>New</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Empty State if filter returns 0 */}
      {filteredDomains.length === 0 && (
        <div className="p-12 text-center bg-white border border-slate-200 rounded-2xl space-y-3">
          <Layers className="w-8 h-8 text-slate-400 mx-auto" />
          <div className="text-base font-semibold text-slate-800">No domains match your search</div>
          <p className="text-sm text-slate-500 max-w-sm mx-auto">
            Try adjusting your search terms or clearing the active category filters.
          </p>
          <button
            onClick={() => { setSearchTerm(''); setSelectedCategory('All'); setSelectedType('All'); }}
            className="px-4 py-2 bg-slate-900 text-white text-xs font-medium rounded-lg hover:bg-slate-800"
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}
