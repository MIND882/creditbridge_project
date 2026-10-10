import React, { useState } from 'react';
import {
  Server,
  Database,
  GitBranch,
  Code2,
  Copy,
  Check,
  ChevronDown,
  ChevronRight,
  ExternalLink,
  Layers,
  Sparkles,
  Zap
} from 'lucide-react';

export default function BackendInspector({ domain, isOpen, onToggle }) {
  const [copiedEndpoint, setCopiedEndpoint] = useState(null);
  const [activeTab, setActiveTab] = useState('endpoints'); // 'endpoints' | 'database' | 'relationships'

  if (!domain || !domain.backend) return null;

  const backend = domain.backend;

  const handleCopy = (text, idx) => {
    navigator.clipboard?.writeText(text);
    setCopiedEndpoint(idx);
    setTimeout(() => setCopiedEndpoint(null), 2000);
  };

  const getMethodColor = (method) => {
    switch (method) {
      case 'GET':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'POST':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'PATCH':
      case 'PUT':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'DELETE':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl text-white">
      {/* Accordion Header */}
      <div
        onClick={onToggle}
        className="px-6 py-4 flex items-center justify-between cursor-pointer hover:bg-slate-800/60 transition-colors select-none"
      >
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30">
            <Server className="w-4 h-4" />
          </div>
          <div>
            <div className="text-[14px] font-bold text-white flex items-center gap-2">
              <span>Backend Architecture & Database Relationships</span>
              <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-indigo-500/30 text-indigo-300 border border-indigo-400/30">
                SQLAlchemy + FastAPI
              </span>
            </div>
            <div className="text-[11.5px] text-slate-400 font-mono">
              Table: <strong className="text-slate-200">{backend.table_name}</strong> • Prefix: <strong className="text-slate-200">{backend.api_prefix}</strong> • {backend.endpoints_count} API routes
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-medium hidden sm:inline">
            {isOpen ? 'Collapse Specs' : 'Inspect Endpoints & Schema'}
          </span>
          <div className={`p-1 rounded-md text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}>
            <ChevronDown className="w-4 h-4" />
          </div>
        </div>
      </div>

      {/* Expanded Content */}
      {isOpen && (
        <div className="border-t border-slate-800 p-6 space-y-5 bg-slate-950/60">
          {/* Navigation Tabs */}
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <button
              onClick={() => setActiveTab('endpoints')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                activeTab === 'endpoints'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Zap className="w-3.5 h-3.5" />
              <span>FastAPI Endpoints ({backend.endpoints_count})</span>
            </button>

            <button
              onClick={() => setActiveTab('database')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                activeTab === 'database'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Database className="w-3.5 h-3.5" />
              <span>Table Schema & Columns ({backend.columns_count})</span>
            </button>

            <button
              onClick={() => setActiveTab('relationships')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                activeTab === 'relationships'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <GitBranch className="w-3.5 h-3.5" />
              <span>Entity Relationships ({backend.relationships_count})</span>
            </button>
          </div>

          {/* TAB 1: FastAPI Endpoints */}
          {activeTab === 'endpoints' && (
            <div className="space-y-3">
              <div className="text-[12px] text-slate-400 flex items-center justify-between">
                <span>FastAPI Router: <code className="text-indigo-300 font-mono">{backend.api_prefix}</code></span>
                <span>Module: <code className="text-slate-300 font-mono">app.accounts.{backend.domain_folder}.api</code></span>
              </div>

              <div className="divide-y divide-slate-800/80 rounded-xl border border-slate-800 overflow-hidden bg-slate-900/80">
                {backend.endpoints.map((ep, idx) => (
                  <div
                    key={idx}
                    className="p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-800/40 transition-colors"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <span className={`text-[11px] font-mono font-bold px-2 py-0.5 rounded border ${getMethodColor(ep.method)}`}>
                        {ep.method}
                      </span>
                      <code className="text-[13px] font-mono text-slate-200 truncate">
                        {ep.full_path}
                      </code>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      <span className="text-[12px] text-slate-400">
                        {ep.summary}
                      </span>
                      <button
                        onClick={() => handleCopy(ep.full_path, idx)}
                        className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-700 transition-colors"
                        title="Copy endpoint"
                      >
                        {copiedEndpoint === idx ? (
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                        ) : (
                          <Copy className="w-3.5 h-3.5" />
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 2: Database Schema & Columns */}
          {activeTab === 'database' && (
            <div className="space-y-3">
              <div className="text-[12px] text-slate-400 flex items-center justify-between">
                <span>SQLAlchemy Model: <strong className="text-slate-200">{domain.label}</strong></span>
                <span>Database Table: <code className="text-emerald-400 font-mono">public.{backend.table_name}</code></span>
              </div>

              <div className="rounded-xl border border-slate-800 overflow-x-auto bg-slate-900/80">
                <table className="w-full text-left text-[12.5px]">
                  <thead className="bg-slate-950/80 text-slate-400 font-semibold text-[11px] uppercase tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="px-4 py-2.5">Column Name</th>
                      <th className="px-4 py-2.5">SQLAlchemy / Python Type</th>
                      <th className="px-4 py-2.5">Nullable</th>
                      <th className="px-4 py-2.5">Foreign Key Target</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80">
                    {backend.columns.length > 0 ? (
                      backend.columns.map((col, idx) => (
                        <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                          <td className="px-4 py-2.5 font-mono font-semibold text-slate-200">
                            {col.name}
                          </td>
                          <td className="px-4 py-2.5 font-mono text-indigo-300">
                            {col.type}
                          </td>
                          <td className="px-4 py-2.5">
                            {col.nullable ? (
                              <span className="text-[10.5px] px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                                NULL
                              </span>
                            ) : (
                              <span className="text-[10.5px] font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                                NOT NULL
                              </span>
                            )}
                          </td>
                          <td className="px-4 py-2.5 font-mono text-[12px]">
                            {col.foreign_key ? (
                              <span className="text-emerald-400 flex items-center gap-1">
                                <GitBranch className="w-3 h-3" />
                                <span>{col.foreign_key}</span>
                              </span>
                            ) : (
                              <span className="text-slate-600">—</span>
                            )}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={4} className="p-4 text-center text-slate-500 text-xs">
                          Standard TenantModel base fields active (id: UUID, business_id: UUID, created_at, modified_at)
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 3: Entity Relationships */}
          {activeTab === 'relationships' && (
            <div className="space-y-3">
              <div className="text-[12px] text-slate-400">
                Foreign Key Relationships defined on SQLAlchemy Model:
              </div>

              {backend.relationships && backend.relationships.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {backend.relationships.map((rel, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/80 space-y-1.5"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono font-bold text-indigo-300 text-[13px]">
                          {rel.name}
                        </span>
                        <span className="text-[10.5px] font-semibold px-2 py-0.5 rounded bg-white/10 text-slate-300">
                          {rel.type}
                        </span>
                      </div>
                      <div className="text-[12px] text-slate-300 flex items-center gap-2">
                        <span>Target:</span>
                        <code className="text-emerald-400 font-mono font-semibold">
                          {rel.target_model}
                        </code>
                      </div>
                      <div className="text-[11px] text-slate-500 font-mono">
                        FK Column: {rel.foreign_key}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/40 text-center text-slate-500 text-xs">
                  This domain operates as a standalone ledger or master entity scoped to tenant <code className="text-slate-300">business_id</code>.
                </div>
              )}

              {/* Service & Repository Architecture Note */}
              <div className="pt-3 border-t border-slate-800/80 text-[11.5px] text-slate-400 flex flex-col sm:flex-row justify-between gap-2">
                <span>Repository: <code className="text-slate-300 font-mono">{backend.repository_module}</code></span>
                <span>Service: <code className="text-slate-300 font-mono">{backend.service_module}</code></span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
