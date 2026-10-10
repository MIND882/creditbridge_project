import React from 'react';
import {
  LayoutDashboard,
  Calculator,
  ShoppingCart,
  ShoppingBag,
  Package,
  Factory,
  Users,
  Settings,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export default function Sidebar({ currentView, onNavigate, mobileOpen, setMobileOpen }) {
  const modules = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
      badge: null,
      view: { type: 'dashboard' }
    },
    {
      id: 'Accounting',
      label: 'Accounting',
      icon: Calculator,
      badge: '191',
      badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      view: { type: 'module_hub', module: 'Accounting' }
    },
    {
      id: 'Selling',
      label: 'Selling',
      icon: ShoppingCart,
      badge: '20',
      badgeColor: 'bg-blue-100 text-blue-800 border-blue-200',
      view: { type: 'module_hub', module: 'Selling' }
    },
    {
      id: 'Buying',
      label: 'Buying',
      icon: ShoppingBag,
      badge: '19',
      badgeColor: 'bg-amber-100 text-amber-800 border-amber-200',
      view: { type: 'module_hub', module: 'Buying' }
    },
    {
      id: 'Stock',
      label: 'Stock',
      icon: Package,
      badge: null,
      view: { type: 'module_hub', module: 'Stock' }
    },
    {
      id: 'Manufacturing',
      label: 'Manufacturing',
      icon: Factory,
      badge: null,
      view: { type: 'module_hub', module: 'Manufacturing' }
    },
    {
      id: 'CRM',
      label: 'CRM',
      icon: Users,
      badge: null,
      view: { type: 'module_hub', module: 'CRM' }
    },
    {
      id: 'Settings',
      label: 'Settings',
      icon: Settings,
      badge: null,
      view: { type: 'module_hub', module: 'Settings' }
    }
  ];

  const isModuleActive = (item) => {
    if (item.id === 'dashboard' && currentView.type === 'dashboard') return true;
    if (item.id === 'Accounting' && (currentView.module === 'Accounting' || currentView.type === 'receivables' || (currentView.domain && currentView.module !== 'Selling' && currentView.module !== 'Buying' && currentView.module !== 'Stock' && currentView.module !== 'Manufacturing' && currentView.module !== 'CRM' && currentView.module !== 'Settings'))) {
      return true;
    }
    return currentView.module === item.id;
  };

  const handleSelect = (mod) => {
    onNavigate(mod.view);
    if (setMobileOpen) setMobileOpen(false);
  };

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-xs lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside className={`
        fixed top-0 bottom-0 left-0 z-50 w-64 bg-white border-r border-slate-200 flex flex-col transition-transform duration-200 ease-in-out
        lg:static lg:translate-x-0
        ${mobileOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full'}
      `}>
        {/* Brand Header */}
        <div className="h-16 px-5 flex items-center justify-between border-b border-slate-200 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-slate-900 text-white flex items-center justify-center font-bold text-sm shadow-xs">
              CB
            </div>
            <div>
              <div className="font-semibold text-slate-900 text-[14px] leading-tight flex items-center gap-1.5">
                CreditBridge
                <span className="text-[10px] font-medium px-1.5 py-0.2 rounded bg-slate-100 text-slate-600 border border-slate-200">ERP</span>
              </div>
              <div className="text-[11px] text-slate-500 font-medium">Enterprise Engine</div>
            </div>
          </div>
        </div>

        {/* Modules Section Title */}
        <div className="px-5 pt-4 pb-2">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Modules
          </div>
        </div>

        {/* Module List - ONLY module names as requested */}
        <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
          {modules.map((item) => {
            const active = isModuleActive(item);
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                onClick={() => handleSelect(item)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-[13.5px] font-medium transition-colors group ${
                  active
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 transition-colors ${
                    active ? 'text-white' : 'text-slate-400 group-hover:text-slate-700'
                  }`} />
                  <span>{item.label}</span>
                </div>

                <div className="flex items-center gap-1.5">
                  {item.badge && (
                    <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${
                      active ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30' : item.badgeColor
                    }`}>
                      {item.badge}
                    </span>
                  )}
                  {active && (
                    <ChevronRight className="w-3.5 h-3.5 text-white/70" />
                  )}
                </div>
              </button>
            );
          })}
        </nav>

        {/* Generic Engine Info Card */}
        <div className="p-3 mx-3 mb-3 bg-slate-50 border border-slate-200 rounded-xl">
          <div className="flex items-center gap-2 mb-1.5">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span className="text-[11.5px] font-semibold text-slate-900">Generic Engine v3</span>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            230 Domains (191 Accounts, 20 Selling, 19 Buying) mapped with List, Detail, and Form screens.
          </p>
        </div>

        {/* Operator Profile Footer */}
        <div className="p-3.5 border-t border-slate-200 flex items-center gap-3 shrink-0 bg-white">
          <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-semibold">
            AD
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-[12.5px] font-semibold text-slate-800 truncate">Admin Operator</div>
            <div className="text-[11px] text-slate-500 truncate">CreditBridge Global Ltd</div>
          </div>
        </div>
      </aside>
    </>
  );
}
