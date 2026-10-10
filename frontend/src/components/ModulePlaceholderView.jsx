import React from 'react';
import {
  ArrowRight,
  ArrowLeft,
  Calculator,
  Layers,
  Sparkles,
  ChevronRight,
  Plus
} from 'lucide-react';
import { OTHER_MODULES } from '../data/otherModules';

export default function ModulePlaceholderView({ moduleName, onNavigate }) {
  const modData = OTHER_MODULES[moduleName] || {
    name: moduleName,
    label: `${moduleName} Module`,
    description: `Operations and transactions management for ${moduleName}.`,
    kpis: [],
    doctypes: [],
    workflow: []
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-[11.5px] font-semibold border border-slate-200">
            <span>ERP Enterprise Module</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            {modData.label}
          </h1>
          <p className="text-slate-600 text-[13.5px] max-w-2xl leading-relaxed">
            {modData.description}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <button
            onClick={() => onNavigate({ type: 'module_hub', module: 'Accounting' })}
            className="flex items-center gap-2 px-4 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium text-[13px] rounded-xl transition-all shadow-xs"
          >
            <Calculator className="w-4 h-4" />
            <span>Go to Accounting (191 Domains)</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Module Key Metrics */}
      {modData.kpis && modData.kpis.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {modData.kpis.map((kpi, idx) => (
            <div key={idx} className="bg-white border border-slate-200 p-5 rounded-2xl shadow-2xs space-y-1">
              <span className="text-[12px] font-medium text-slate-500">{kpi.label}</span>
              <div className="text-2xl font-bold text-slate-900 tracking-tight">{kpi.value}</div>
              <div className="text-[11.5px] text-emerald-600 font-medium">{kpi.change}</div>
            </div>
          ))}
        </div>
      )}

      {/* Operational Workflow Stages */}
      {modData.workflow && modData.workflow.length > 0 && (
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider pb-2 border-b border-slate-100">
            {moduleName} Operational Workflow
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {modData.workflow.map((w, idx) => (
              <div key={idx} className="bg-slate-50 border border-slate-200/80 rounded-xl p-4 space-y-1 relative">
                <div className="text-[12.5px] font-bold text-slate-900">{w.step}</div>
                <div className="text-[12px] text-slate-500 leading-relaxed">{w.desc}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Primary DocTypes Directory */}
      {modData.doctypes && modData.doctypes.length > 0 && (
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              {moduleName} Core DocTypes & Masters
            </h2>
            <span className="text-[12px] text-slate-400 font-mono">Generic Schema Ready</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {modData.doctypes.map((dt) => (
              <div key={dt.name} className="border border-slate-200 rounded-xl p-4 space-y-2 bg-slate-50/50">
                <div className="flex items-start justify-between gap-2">
                  <div className="font-bold text-slate-900 text-[13.5px]">{dt.label}</div>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full border bg-white text-slate-700 border-slate-200">
                    {dt.type}
                  </span>
                </div>
                <p className="text-[12px] text-slate-500 line-clamp-2">{dt.desc}</p>
                <div className="pt-2 text-[11px] font-mono text-slate-400">
                  erpnext.{moduleName.toLowerCase()}.doctype.{dt.name}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
