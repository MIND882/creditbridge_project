import React, { useState, useEffect } from 'react';
import { RecordsProvider, useRecords } from './context/RecordsContext';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DashboardView from './components/DashboardView';
import AccountingHubView from './components/AccountingHubView';
import SellingHubView from './components/SellingHubView';
import BuyingHubView from './components/BuyingHubView';
import GenericListView from './components/GenericListView';
import GenericDetailView from './components/GenericDetailView';
import GenericFormView from './components/GenericFormView';
import AccountsReceivableView from './components/AccountsReceivableView';
import ModulePlaceholderView from './components/ModulePlaceholderView';
import CommandPaletteModal from './components/CommandPaletteModal';
import PrintModal from './components/PrintModal';
import Toast from './components/Toast';

function AppContent() {
  // Navigation state:
  // type: 'dashboard' | 'module_hub' | 'list' | 'detail' | 'form' | 'receivables'
  const [currentView, setCurrentView] = useState({
    type: 'dashboard'
  });

  const [mobileOpen, setMobileOpen] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const [printModal, setPrintModal] = useState({ open: false, domain: null, record: null });
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  const handleNavigate = (view, domain, module = 'Accounting') => {
    if (typeof view === 'string') {
      setCurrentView({ type: view, domain: domain, module: module });
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    if (view && view.commandOpen !== undefined) {
      setCommandOpen(view.commandOpen);
      return;
    }
    setCurrentView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleOpenPrint = (domain, record) => {
    setPrintModal({ open: true, domain, record });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex antialiased selection:bg-indigo-500 selection:text-white">
      {/* Sidebar - ONLY module names as requested */}
      <Sidebar
        currentView={currentView}
        onNavigate={handleNavigate}
        mobileOpen={mobileOpen}
        setMobileOpen={setMobileOpen}
      />

      {/* Main Content Area */}
      <div className="flex-1 min-w-0 flex flex-col min-h-screen">
        {/* Top Header */}
        <Header
          currentView={currentView}
          onNavigate={handleNavigate}
          onOpenCommand={() => setCommandOpen(true)}
          onToggleSidebar={() => setMobileOpen(prev => !prev)}
        />

        {/* Viewport Router */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          {currentView.type === 'dashboard' && (
            <DashboardView onNavigate={handleNavigate} />
          )}

          {currentView.type === 'module_hub' && currentView.module === 'Accounting' && (
            <AccountingHubView onNavigate={handleNavigate} />
          )}

          {currentView.type === 'module_hub' && currentView.module === 'Selling' && (
            <SellingHubView onNavigate={handleNavigate} />
          )}

          {currentView.type === 'module_hub' && currentView.module === 'Buying' && (
            <BuyingHubView onNavigate={handleNavigate} />
          )}

          {currentView.type === 'module_hub' && currentView.module !== 'Accounting' && currentView.module !== 'Selling' && currentView.module !== 'Buying' && (
            <ModulePlaceholderView
              moduleName={currentView.module}
              onNavigate={handleNavigate}
            />
          )}

          {currentView.type === 'list' && (
            <GenericListView
              domainName={currentView.domain}
              onNavigate={handleNavigate}
              onShowToast={showToast}
            />
          )}

          {currentView.type === 'detail' && (
            <GenericDetailView
              domainName={currentView.domain}
              recordId={currentView.id}
              onNavigate={handleNavigate}
              onShowToast={showToast}
              onOpenPrint={handleOpenPrint}
            />
          )}

          {currentView.type === 'form' && (
            <GenericFormView
              domainName={currentView.domain}
              recordId={currentView.id}
              onNavigate={handleNavigate}
              onShowToast={showToast}
            />
          )}

          {currentView.type === 'receivables' && (
            <AccountsReceivableView onNavigate={handleNavigate} />
          )}
        </main>

        {/* Global Footer */}
        <footer className="border-t border-slate-200 bg-white px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="font-semibold text-slate-800">Generic Engine v3.0:</span>
            <span>List, Form & Detail screens • 230 Domains (191 Accounts, 20 Selling, 19 Buying) fully operational</span>
          </div>
          <div>
            <span>CreditBridge ERP • Design System & Framework Compliant</span>
          </div>
        </footer>
      </div>

      {/* Global Command Palette Modal */}
      <CommandPaletteModal
        open={commandOpen}
        onClose={() => setCommandOpen(false)}
        onNavigate={handleNavigate}
      />

      {/* Document Print Preview Modal */}
      <PrintModal
        open={printModal.open}
        onClose={() => setPrintModal({ open: false, domain: null, record: null })}
        domain={printModal.domain}
        record={printModal.record}
      />

      {/* Floating Toast Alert */}
      <Toast toast={toast} onClose={() => setToast(null)} />
    </div>
  );
}

export default function App() {
  return (
    <RecordsProvider>
      <AppContent />
    </RecordsProvider>
  );
}
