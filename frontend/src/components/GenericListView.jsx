import React, { useState, useMemo, useEffect } from 'react';
import {
  Search,
  Plus,
  Filter,
  ArrowUpDown,
  Download,
  Trash2,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Eye,
  Edit,
  ArrowLeft,
  ArrowRight,
  RotateCw,
  Sparkles,
  Server
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';
import BackendInspector from './BackendInspector';

export default function GenericListView({ domainName, onNavigate, onShowToast }) {
  const {
    domains,
    recordsStore,
    getDomainRecords,
    deleteRecord,
    updateRecordStatus,
    fetchDomainRecords,
    loadingRecords,
    backendConnected
  } = useRecords();

  const domain = useMemo(() => {
    return domains.find(d => d.name === domainName) || domains[0];
  }, [domains, domainName]);

  // Automatically fetch live records from PostgreSQL / FastAPI on mount and domain change
  useEffect(() => {
    if (domain?.name) {
      fetchDomainRecords(domain.name);
    }
  }, [domain?.name]);

  const allRecords = recordsStore?.[domain.name] || getDomainRecords(domain.name) || [];

  // States
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedRowIds, setSelectedRowIds] = useState([]);
  const [showBackendSpecs, setShowBackendSpecs] = useState(false);
  const pageSize = 10;

   const currentModule = domain.module || 'Accounting';
  const moduleDomains = useMemo(() => {
    return domains.filter(d => (d.module || 'Accounting') === currentModule);
  }, [domains, currentModule]);
  const moduleTotal = moduleDomains.length || 1;
  const moduleDomainIndex = Math.max(1, moduleDomains.findIndex(d => d.name === domain.name) + 1);

  const handlePrevDomain = () => {
    const curIdx = moduleDomains.findIndex(d => d.name === domain.name);
    const prevIdx = curIdx > 0 ? curIdx - 1 : moduleDomains.length - 1;
    onNavigate({ type: 'list', domain: moduleDomains[prevIdx].name, module: currentModule });
  };
  const handleNextDomain = () => {
    const curIdx = moduleDomains.findIndex(d => d.name === domain.name);
    const nextIdx = curIdx < moduleDomains.length - 1 ? curIdx + 1 : 0;
    onNavigate({ type: 'list', domain: moduleDomains[nextIdx].name, module: currentModule });
  };

  // Determine list columns (in_list_view === true)
  const listColumns = useMemo(() => {
    const cols = domain.fields.filter(f => f.in_list_view);
    if (cols.length >= 3) return cols;
    // Fallback: take first 4 fields
    return domain.fields.slice(0, 5);
  }, [domain]);

  // Extract available statuses from domain field
  const statusOptions = useMemo(() => {
    const statusField = domain.fields.find(f => f.name === 'status');
    return statusField?.options || ['All', 'Draft', 'Submitted', 'Active', 'Cancelled'];
  }, [domain]);

  // Filter records
  const filteredRecords = useMemo(() => {
    return allRecords.filter(record => {
      const matchesSearch = !searchTerm || Object.values(record).some(val =>
        String(val).toLowerCase().includes(searchTerm.toLowerCase())
      );
      const matchesStatus = selectedStatus === 'All' || record.status === selectedStatus;
      return matchesSearch && matchesStatus;
    });
  }, [allRecords, searchTerm, selectedStatus]);

  // Pagination
  const totalPages = Math.ceil(filteredRecords.length / pageSize) || 1;
  const paginatedRecords = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredRecords.slice(start, start + pageSize);
  }, [filteredRecords, currentPage]);

  // Row selection
  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedRowIds(paginatedRecords.map(r => r.id || r.name));
    } else {
      setSelectedRowIds([]);
    }
  };

  const handleSelectRow = (id) => {
    setSelectedRowIds(prev =>
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  // Bulk actions
  const handleBulkDelete = () => {
    if (window.confirm(`Delete ${selectedRowIds.length} selected record(s)?`)) {
      selectedRowIds.forEach(id => deleteRecord(domain.name, id));
      setSelectedRowIds([]);
      onShowToast?.(`Deleted ${selectedRowIds.length} records`);
    }
  };

  const handleBulkSubmit = () => {
    selectedRowIds.forEach(id => updateRecordStatus(domain.name, id, 'Submitted'));
    setSelectedRowIds([]);
    onShowToast?.(`Submitted ${selectedRowIds.length} records`);
  };

  const handleExportCSV = () => {
    if (filteredRecords.length === 0) return;
    const headers = listColumns.map(c => c.label).join(',');
    const rows = filteredRecords.map(rec =>
      listColumns.map(c => `"${String(rec[c.name] ?? '')}"`).join(',')
    );
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers, ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${domain.name}_export.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    onShowToast?.(`Exported ${filteredRecords.length} records to CSV`);
  };

  const formatCellValue = (val, field) => {
    if (val === undefined || val === null || val === '') return '—';
    if (field.type === 'currency') {
      const num = Number(val);
      if (isNaN(num)) return String(val);
      return '₹' + num.toLocaleString('en-IN');
    }
    if (field.type === 'check') {
      return val ? (
        <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
          Yes
        </span>
      ) : (
        <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-500">
          No
        </span>
      );
    }
    if (field.name === 'status') {
      const s = String(val);
      let pillClass = 'bg-slate-100 text-slate-700 border-slate-200';
      if (['Submitted', 'Paid', 'Active', 'Enabled', 'Completed'].includes(s)) {
        pillClass = 'bg-emerald-50 text-emerald-700 border-emerald-200';
      } else if (['Draft', 'Pending', 'To Receive', 'To Bill'].includes(s)) {
        pillClass = 'bg-amber-50 text-amber-700 border-amber-200';
      } else if (['Cancelled', 'Disabled', 'Overdue', 'Lost'].includes(s)) {
        pillClass = 'bg-rose-50 text-rose-700 border-rose-200';
      }
      return (
        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border ${pillClass}`}>
          {s}
        </span>
      );
    }
    if (field.type === 'link') {
      return (
        <span className="inline-block text-indigo-600 font-medium truncate max-w-[180px]">
          {String(val)}
        </span>
      );
    }
    return String(val);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Stepper for Domain by Domain Browsing */}
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
            Domain #{moduleDomainIndex} / {moduleTotal}:
          </span>
          <span className="font-semibold text-white truncate max-w-xs sm:max-w-md">
            {domain.label}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigate({ type: 'module_hub', module: currentModule })}
            className="text-slate-300 hover:text-white underline text-[11.5px] mr-2"
          >
            All {moduleTotal} {currentModule} Domains
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

      {/* Domain Header Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-semibold text-slate-400">
              #{domain.index}
            </span>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              {domain.label}
            </h1>
            <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              {domain.type}
            </span>
            <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-indigo-50 text-indigo-700">
              {domain.category}
            </span>
          </div>
          <p className="text-[13px] text-slate-500 max-w-2xl leading-relaxed">
            {domain.description}
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            onClick={() => fetchDomainRecords(domain.name, true)}
            disabled={loadingRecords}
            className="flex items-center gap-1.5 px-3 py-2 border border-emerald-200 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 text-[12.5px] font-semibold rounded-xl transition-colors shadow-2xs"
            title="Fetch and sync live records directly from PostgreSQL database"
          >
            <RotateCw className={`w-3.5 h-3.5 text-emerald-600 ${loadingRecords ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">{loadingRecords ? 'Syncing...' : 'Sync DB'}</span>
            <span className="sm:hidden">Sync</span>
          </button>

          <button
            onClick={() => setShowBackendSpecs(prev => !prev)}
            className="flex items-center gap-1.5 px-3 py-2 border border-indigo-200 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-[12.5px] font-semibold rounded-xl transition-colors shadow-2xs"
          >
            <Server className="w-3.5 h-3.5 text-indigo-600" />
            <span className="hidden sm:inline">Backend Specs</span>
            <span className="sm:hidden">Specs</span>
          </button>

          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-3 py-2 border border-slate-200 hover:bg-slate-50 text-slate-700 text-[12.5px] font-semibold rounded-xl transition-colors shadow-2xs"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" />
            <span className="hidden sm:inline">Export</span>
          </button>

          <button
            onClick={() => onNavigate({ type: 'form', domain: domain.name })}
            className="flex items-center gap-1.5 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-[12.5px] font-semibold rounded-xl transition-all shadow-xs"
          >
            <Plus className="w-4 h-4" />
            <span>New {domain.label}</span>
          </button>
        </div>
      </div>

      {/* Backend Specs Panel */}
      {showBackendSpecs && (
        <BackendInspector
          domain={domain}
          isOpen={true}
          onToggle={() => setShowBackendSpecs(false)}
        />
      )}

      {/* Filters & Search Toolbar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); setCurrentPage(1); }}
            placeholder={`Filter ${domain.label} records...`}
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

        {/* Status Filter Buttons */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          <span className="text-[11.5px] font-medium text-slate-400 mr-1 shrink-0">Status:</span>
          {['All', ...statusOptions.filter(s => s !== 'All')].map((st) => (
            <button
              key={st}
              onClick={() => { setSelectedStatus(st); setCurrentPage(1); }}
              className={`px-2.5 py-1 rounded-md text-[11.5px] font-medium whitespace-nowrap transition-colors ${
                selectedStatus === st
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* Bulk Actions Floating Bar */}
      {selectedRowIds.length > 0 && (
        <div className="bg-indigo-900 text-white px-4 py-2.5 rounded-xl flex items-center justify-between shadow-md text-[13px]">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold">{selectedRowIds.length}</span> record(s) selected
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleBulkSubmit}
              className="px-3 py-1 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-xs"
            >
              Submit All
            </button>
            <button
              onClick={handleBulkDelete}
              className="px-3 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-medium text-xs flex items-center gap-1"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Delete</span>
            </button>
          </div>
        </div>
      )}

      {/* Records Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[13px]">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold text-[11px] uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3 w-10">
                  <input
                    type="checkbox"
                    checked={paginatedRecords.length > 0 && selectedRowIds.length === paginatedRecords.length}
                    onChange={handleSelectAll}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                </th>
                {listColumns.map((col) => (
                  <th key={col.name} className="px-4 py-3 whitespace-nowrap">
                    {col.label}
                  </th>
                ))}
                <th className="px-4 py-3 text-right w-24">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {paginatedRecords.map((record) => {
                const recId = record.id || record.name;
                const isSelected = selectedRowIds.includes(recId);

                return (
                  <tr
                    key={recId}
                    className={`hover:bg-slate-50/80 transition-colors ${
                      isSelected ? 'bg-indigo-50/50' : ''
                    }`}
                  >
                    <td className="px-4 py-3" onClick={(e) => e.stopPropagation()}>
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => handleSelectRow(recId)}
                        className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                      />
                    </td>

                    {listColumns.map((col, idx) => (
                      <td
                        key={col.name}
                        onClick={() => onNavigate({ type: 'detail', domain: domain.name, id: recId })}
                        className={`px-4 py-3 cursor-pointer ${
                          idx === 0 ? 'font-semibold text-slate-900 hover:text-indigo-600' : 'text-slate-600'
                        }`}
                      >
                        {formatCellValue(record[col.name], col)}
                      </td>
                    ))}

                    <td className="px-4 py-3 text-right" onClick={(e) => e.stopPropagation()}>
                      <div className="flex items-center justify-end gap-1">
                        <button
                          onClick={() => onNavigate({ type: 'detail', domain: domain.name, id: recId })}
                          className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                          title="View Details"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => onNavigate({ type: 'form', domain: domain.name, id: recId })}
                          className="p-1.5 rounded-lg text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
                          title="Edit Record"
                        >
                          <Edit className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => {
                            if (window.confirm(`Delete record ${recId}?`)) {
                              deleteRecord(domain.name, recId);
                              onShowToast?.(`Deleted record ${recId}`);
                            }
                          }}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Empty State */}
        {paginatedRecords.length === 0 && (
          <div className="p-12 text-center space-y-3">
            <div className="text-sm font-semibold text-slate-700">No records found</div>
            <p className="text-xs text-slate-500">
              There are no {domain.label} entries matching your criteria.
            </p>
            <button
              onClick={() => onNavigate({ type: 'form', domain: domain.name })}
              className="px-3.5 py-1.5 bg-slate-900 text-white rounded-lg text-xs font-medium hover:bg-slate-800"
            >
              + Create First Record
            </button>
          </div>
        )}

        {/* Pagination Controls */}
        <div className="px-4 py-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-[12.5px] text-slate-600">
          <div>
            Showing <span className="font-semibold text-slate-900">{filteredRecords.length > 0 ? (currentPage - 1) * pageSize + 1 : 0}</span> to{' '}
            <span className="font-semibold text-slate-900">
              {Math.min(currentPage * pageSize, filteredRecords.length)}
            </span> of{' '}
            <span className="font-semibold text-slate-900">{filteredRecords.length}</span> records
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setCurrentPage(p => Math.max(p - 1, 1))}
              disabled={currentPage === 1}
              className="p-1.5 rounded-lg border border-slate-200 bg-white text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-2 font-medium">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="p-1.5 rounded-lg border border-slate-200 bg-white text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}