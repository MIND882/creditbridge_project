import React, { useState, useEffect, useRef } from 'react';
import {
  Search,
  X,
  Calculator,
  Layers,
  ArrowRight,
  FileText,
  LayoutDashboard,
  Check
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function CommandPaletteModal({ open, onClose, onNavigate }) {
  const { domains } = useRecords();
  const [query, setQuery] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery('');
    }
  }, [open]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'g' || e.key === 'K' || e.key === 'G')) {
        e.preventDefault();
        if (open) onClose();
        else onNavigate?.({ commandOpen: true });
      }
      if (e.key === 'Escape' && open) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose, onNavigate]);

  if (!open) return null;

  const filtered = query.trim() === ''
    ? domains.slice(0, 15)
    : domains.filter(d =>
        d.name.toLowerCase().includes(query.toLowerCase()) ||
        d.label.toLowerCase().includes(query.toLowerCase()) ||
        d.category.toLowerCase().includes(query.toLowerCase())
      ).slice(0, 25);

  const modules = [
    { name: 'Dashboard', type: 'dashboard' },
    { name: 'Accounting (191 Domains)', type: 'module_hub', module: 'Accounting' },
    { name: 'Accounts Receivable Report', type: 'receivables' },
    { name: 'Selling', type: 'module_hub', module: 'Selling' },
    { name: 'Buying', type: 'module_hub', module: 'Buying' },
    { name: 'Stock', type: 'module_hub', module: 'Stock' },
    { name: 'Manufacturing', type: 'module_hub', module: 'Manufacturing' },
    { name: 'CRM', type: 'module_hub', module: 'CRM' },
    { name: 'Settings', type: 'module_hub', module: 'Settings' }
  ].filter(m => query === '' || m.name.toLowerCase().includes(query.toLowerCase()));

  const handleSelectDomain = (domainName) => {
    const domainObj = domains.find(d => d.name === domainName);
    onNavigate({ type: 'list', domain: domainName, module: domainObj?.module || 'Accounting' });
    onClose();
  };

  const handleSelectModule = (view) => {
    onNavigate(view);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs p-4 flex items-start justify-center pt-[12vh]"
      onClick={onClose}
    >
      <div
        className="w-full max-w-xl bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[70vh] animate-in"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input Bar */}
        <div className="h-14 px-4 border-b border-slate-200 flex items-center gap-3 shrink-0">
          <Search className="w-5 h-5 text-slate-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a domain name or module (e.g. Sales Invoice, Bank, GL)..."
            className="flex-1 bg-transparent text-[14px] text-slate-900 placeholder:text-slate-400 focus:outline-none"
          />
          <kbd className="px-2 py-0.5 rounded bg-slate-100 text-slate-500 text-[11px] font-mono border border-slate-200">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-2 space-y-3">
          {/* Module matches */}
          {modules.length > 0 && (
            <div>
              <div className="px-3 py-1 text-[10.5px] font-semibold text-slate-400 uppercase tracking-wider">
                Modules & Reports
              </div>
              <div className="space-y-0.5">
                {modules.map((m, i) => (
                  <button
                    key={i}
                    onClick={() => handleSelectModule(m)}
                    className="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-slate-100 text-left text-[13px] text-slate-800 transition-colors group"
                  >
                    <div className="flex items-center gap-2.5">
                      <LayoutDashboard className="w-4 h-4 text-slate-400 group-hover:text-slate-800" />
                      <span className="font-medium">{m.name}</span>
                    </div>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-300 group-hover:text-slate-600" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Domain matches */}
          <div>
            <div className="px-3 py-1 text-[10.5px] font-semibold text-slate-400 uppercase tracking-wider flex items-center justify-between">
              <span>Accounting Domains ({filtered.length})</span>
              <span className="font-normal lowercase">out of 191</span>
            </div>

            <div className="space-y-0.5">
              {filtered.map((d) => (
                <button
                  key={d.name}
                  onClick={() => handleSelectDomain(d.name)}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-slate-100 text-left text-[13px] transition-colors group"
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <span className="text-[11px] font-mono text-slate-400 w-8">
                      #{d.index}
                    </span>
                    <div className="truncate">
                      <span className="font-semibold text-slate-900 group-hover:text-indigo-600">
                        {d.label}
                      </span>
                      <span className="text-[11.5px] text-slate-400 ml-2 font-mono">
                        {d.name}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                      {d.module || 'Accounting'}
                    </span>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                      {d.category}
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700">
                      {d.type}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="h-10 px-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-[11px] text-slate-500 shrink-0">
          <span>Use ⌘K / ⌘G to toggle anytime</span>
          <span>{domains.length} Domains Indexed (Accounting &amp; Selling)</span>
        </div>
      </div>
    </div>
  );
}
