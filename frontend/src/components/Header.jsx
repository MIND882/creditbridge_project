import React, { useState } from 'react';
import {
  Menu,
  Search,
  Command,
  FileBarChart,
  Layers,
  Sparkles,
  ChevronRight,
  Building2,
  KeyRound,
  CheckCircle2,
  ShieldCheck,
  LogOut
} from 'lucide-react';
import { useRecords } from '../context/RecordsContext';

export default function Header({ currentView, onNavigate, onOpenCommand, onToggleSidebar }) {
  const {
    domains,
    backendConnected,
    checkingBackend,
    checkBackendHealth,
    authToken,
    authTenant,
    quickDemoLogin,
    logout
  } = useRecords();

  const [showAuthMenu, setShowAuthMenu] = useState(false);
  const [loggingIn, setLoggingIn] = useState(false);

  const handleQuickLogin = async () => {
    setLoggingIn(true);
    await quickDemoLogin('9876543210');
    setLoggingIn(false);
    setShowAuthMenu(false);
  };

  const getBreadcrumbs = () => {
    if (currentView.type === 'dashboard') {
      return [{ label: 'Dashboard', active: true }];
    }
    if (currentView.type === 'module_hub') {
      return [
        { label: 'Modules', onClick: () => onNavigate({ type: 'dashboard' }) },
        { label: currentView.module || 'Accounting', active: true }
      ];
    }
    if (currentView.type === 'receivables') {
      return [
        { label: 'Accounting', onClick: () => onNavigate({ type: 'module_hub', module: 'Accounting' }) },
        { label: 'Accounts Receivable Aging', active: true }
      ];
    }
    if (currentView.domain) {
      const dObj = domains.find(d => d.name === currentView.domain);
      const label = dObj ? dObj.label : currentView.domain;
      const mod = dObj?.module || currentView.module || 'Accounting';
      const crumbs = [
        { label: mod, onClick: () => onNavigate({ type: 'module_hub', module: mod }) },
        {
          label: label,
          onClick: currentView.type !== 'list' ? () => onNavigate({ type: 'list', domain: currentView.domain, module: mod }) : undefined,
          active: currentView.type === 'list'
        }
      ];

      if (currentView.type === 'form') {
        crumbs.push({ label: currentView.id ? `Edit ${currentView.id}` : 'New Record', active: true });
      } else if (currentView.type === 'detail') {
        crumbs.push({ label: currentView.id, active: true });
      }
      return crumbs;
    }

    return [{ label: 'CreditBridge ERP', active: true }];
  };

  const breadcrumbs = getBreadcrumbs();

  return (
    <header className="h-16 bg-white/95 backdrop-blur-md border-b border-slate-200 sticky top-0 z-30 flex items-center justify-between px-4 sm:px-6 lg:px-8">
      {/* Left: Mobile Toggle & Breadcrumbs */}
      <div className="flex items-center gap-3 min-w-0">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
          aria-label="Toggle Navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-[13px] text-slate-500 overflow-hidden truncate">
          {breadcrumbs.map((crumb, idx) => (
            <React.Fragment key={idx}>
              {idx > 0 && <ChevronRight className="w-3.5 h-3.5 text-slate-400 shrink-0" />}
              {crumb.onClick ? (
                <button
                  onClick={crumb.onClick}
                  className="hover:text-slate-900 transition-colors truncate font-medium"
                >
                  {crumb.label}
                </button>
              ) : (
                <span className={`truncate ${crumb.active ? 'text-slate-900 font-semibold' : ''}`}>
                  {crumb.label}
                </span>
              )}
            </React.Fragment>
          ))}
        </nav>
      </div>

      {/* Right: Quick Tools, Search Bar, & Status */}
      <div className="flex items-center gap-2.5 sm:gap-3 shrink-0">
        {/* Quick Report Link */}
        <button
          onClick={() => onNavigate({ type: 'receivables' })}
          className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 text-[12px] font-medium transition-colors"
        >
          <FileBarChart className="w-3.5 h-3.5 text-indigo-600" />
          <span>Receivables Aging</span>
        </button>

        {/* Global Search / Command Trigger */}
        <button
          onClick={onOpenCommand}
          className="flex items-center gap-2 h-9 px-3 rounded-lg border border-slate-200 bg-slate-50 hover:bg-white hover:border-slate-300 text-slate-500 hover:text-slate-700 text-[12.5px] transition-all shadow-2xs group"
        >
          <Search className="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
          <span className="hidden sm:inline">Search all 230 domains...</span>
          <span className="sm:hidden">Search</span>
          <kbd className="hidden sm:inline-flex items-center gap-0.5 ml-2 px-1.5 py-0.5 rounded bg-white border border-slate-200 text-[10.5px] font-mono text-slate-500">
            <Command className="w-3 h-3" />K
          </kbd>
        </button>

        {/* Backend API Connection Status */}
        <button
          onClick={checkBackendHealth}
          disabled={checkingBackend}
          className={`hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-[11.5px] font-medium transition-colors ${
            backendConnected
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100'
              : 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200'
          }`}
          title="Click to check FastAPI Backend connection at http://localhost:8000"
        >
          <span className={`w-2 h-2 rounded-full ${
            backendConnected ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'
          }`} />
          <span>{checkingBackend ? 'Checking API...' : backendConnected ? 'Backend Live (8000)' : 'Backend Offline'}</span>
        </button>

        {/* Active Tenant / Auth Pill */}
        <div className="relative">
          <button
            onClick={() => setShowAuthMenu(!showAuthMenu)}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-indigo-200 bg-indigo-50/70 hover:bg-indigo-100/70 text-indigo-900 text-[11.5px] font-medium transition-colors"
          >
            <Building2 className="w-3.5 h-3.5 text-indigo-600" />
            <span className="max-w-[120px] truncate">{authTenant.business_name}</span>
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
          </button>

          {/* Auth Dropdown */}
          {showAuthMenu && (
            <div className="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-xl border border-slate-200 p-3 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
              <div className="flex items-center gap-2 pb-2 mb-2 border-b border-slate-100">
                <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-sm">
                  CB
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs font-semibold text-slate-800 truncate">{authTenant.business_name}</div>
                  <div className="text-[10px] text-slate-500">Phone: {authTenant.phone}</div>
                </div>
              </div>

              <div className="text-[11px] text-slate-600 mb-3 bg-slate-50 p-2 rounded-lg">
                <div className="flex items-center gap-1 text-slate-700 font-medium mb-0.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Auth Status:</span>
                </div>
                <p className="text-[10.5px] text-slate-500">
                  {authToken ? '✓ Authenticated Bearer JWT' : '⚡ Auto-Tenant Dev Mode Active (No 401s)'}
                </p>
              </div>

              <div className="flex flex-col gap-1.5">
                <button
                  onClick={handleQuickLogin}
                  disabled={loggingIn}
                  className="w-full flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-medium transition-colors"
                >
                  <KeyRound className="w-3.5 h-3.5" />
                  <span>{loggingIn ? 'Authenticating...' : '1-Click Demo Login (JWT)'}</span>
                </button>

                {authToken && (
                  <button
                    onClick={() => { logout(); setShowAuthMenu(false); }}
                    className="w-full flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600 text-xs transition-colors"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    <span>Clear Token (Use Auto-Dev Mode)</span>
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
