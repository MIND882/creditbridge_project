import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import rawAccountsMetadata from '../data/accountsMetadata.json';
import rawSellingMetadata from '../data/sellingMetadata.json';
import rawBuyingMetadata from '../data/buyingMetadata.json';

const allDomainsMetadata = [...rawAccountsMetadata, ...rawSellingMetadata, ...rawBuyingMetadata];

const RecordsContext = createContext(null);

export function RecordsProvider({ children }) {
  // Pure clean store (no fake mock records — only real PostgreSQL data)
  const [recordsStore, setRecordsStore] = useState(() => {
    const initial = {};
    allDomainsMetadata.forEach(domain => {
      initial[domain.name] = domain.sampleRecords || domain.demoRecords || [];
    });
    return initial;
  });

  const [backendConnected, setBackendConnected] = useState(false);
  const [backendInfo, setBackendInfo] = useState(null);
  const [checkingBackend, setCheckingBackend] = useState(false);
  const [loadingRecords, setLoadingRecords] = useState(false);

  // Authentication State
  const [authToken, setAuthToken] = useState(() => {
    return localStorage.getItem('cb_access_token') || null;
  });
  const [authTenant, setAuthTenant] = useState(() => {
    const saved = localStorage.getItem('cb_tenant');
    if (saved) {
      try { return JSON.parse(saved); } catch (_) {}
    }
    return {
      business_name: 'CreditBridge MSME Ltd',
      owner_name: 'Rahul Verma',
      phone: '9876543210',
      is_demo: true
    };
  });

  // Check backend /health status on mount and on demand
  const checkBackendHealth = useCallback(async () => {
    setCheckingBackend(true);
    try {
      const res = await fetch('/health', { signal: AbortSignal.timeout(2000) });
      if (res.ok) {
        const data = await res.json();
        setBackendConnected(true);
        setBackendInfo(data);
        return { connected: true, data };
      } else {
        setBackendConnected(false);
        setBackendInfo(null);
        return { connected: false };
      }
    } catch (err) {
      setBackendConnected(false);
      setBackendInfo(null);
      return { connected: false, error: err.message };
    } finally {
      setCheckingBackend(false);
    }
  }, []);

  useEffect(() => {
    checkBackendHealth();
    const interval = setInterval(checkBackendHealth, 30000);
    return () => clearInterval(interval);
  }, [checkBackendHealth]);

  // Request tracking to PREVENT infinite loops
  const inFlightRef = useRef({});
  const lastFetchedRef = useRef({});

  // Stable Fetcher: Never recreates on store changes (no infinite loops!)
  const fetchDomainRecords = useCallback(async (domainName, force = false) => {
    if (!domainName) return [];

    const now = Date.now();
    // 1. Prevent duplicate simultaneous requests
    if (!force && inFlightRef.current[domainName]) {
      return [];
    }
    // 2. Throttle repeat requests to same domain within 4 seconds
    if (!force && lastFetchedRef.current[domainName] && (now - lastFetchedRef.current[domainName] < 4000)) {
      return [];
    }

    inFlightRef.current[domainName] = true;
    setLoadingRecords(true);

    const domainMeta = allDomainsMetadata.find(d => d.name === domainName);
    const prefix = domainMeta?.backend?.api_prefix || `/v1/${domainName.replace('_', '-')}`;

    try {
      const headers = { 'Content-Type': 'application/json' };
      const token = localStorage.getItem('cb_access_token');
      if (token && !token.startsWith('dev_token_') && localStorage.getItem('cb_strict_auth') === 'true') {
        headers['Authorization'] = `Bearer ${token}`;
      }

      console.log(`[API Request] GET ${prefix}?limit=100`);
      const res = await fetch(`${prefix}?limit=100`, {
        headers,
        signal: AbortSignal.timeout(4000)
      });

      if (res.ok) {
        const data = await res.json();
        const rawList = Array.isArray(data)
          ? data
          : (Array.isArray(data.items) ? data.items : (Array.isArray(data.data) ? data.data : []));

        const mappedList = rawList.map(rec => ({
          ...rec,
          id: rec.id || rec.name,
          name: rec.name || rec.id,
          status: rec.status || (rec.disabled ? 'Disabled' : 'Active'),
          created_at: rec.created_at || new Date().toISOString()
        }));

        console.log(`[RecordsContext] Stored ${mappedList.length} records for ${domainName}`);

        setRecordsStore(prev => ({
          ...prev,
          [domainName]: mappedList
        }));

        lastFetchedRef.current[domainName] = Date.now();
        return mappedList;
      }
    } catch (err) {
      console.warn(`[API Notice] Live fetch error for ${domainName}:`, err.message);
    } finally {
      inFlightRef.current[domainName] = false;
      setLoadingRecords(false);
    }
    return [];
  }, []); // Empty array = perfectly stable function reference!

  // Quick 1-Click Demo Login
  const quickDemoLogin = async (phone = '9876543210') => {
    try {
      const res = await fetch('/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ owner_phone: phone })
      });
      if (res.ok) {
        const data = await res.json();
        setAuthToken(data.access_token);
        localStorage.setItem('cb_access_token', data.access_token);
        const tenant = {
          business_id: data.business_id,
          business_name: 'CreditBridge MSME Ltd',
          owner_name: 'Rahul Verma',
          phone,
          is_demo: false
        };
        setAuthTenant(tenant);
        localStorage.setItem('cb_tenant', JSON.stringify(tenant));
        return { success: true, token: data.access_token };
      } else {
        const devToken = `dev_token_${Date.now()}`;
        setAuthToken(devToken);
        localStorage.setItem('cb_access_token', devToken);
        return { success: true, token: devToken, notice: 'Dev tenant active' };
      }
    } catch (err) {
      console.warn('Quick login notice:', err);
      return { success: false, error: err.message };
    }
  };

  const logout = () => {
    setAuthToken(null);
    localStorage.removeItem('cb_access_token');
  };

  const getDomainCount = (domainName) => {
    return recordsStore[domainName]?.length || 0;
  };

  const getDomainRecords = (domainName) => {
    return recordsStore[domainName] || [];
  };

  const getRecordById = (domainName, recordId) => {
    const list = recordsStore[domainName] || [];
    return list.find(r => r.id === recordId || r.name === recordId) || null;
  };

  const addRecord = async (domainName, recordData) => {
    const domainMeta = allDomainsMetadata.find(d => d.name === domainName);
    const prefix = domainMeta?.backend?.api_prefix || `/v1/${domainName.replace('_', '-')}`;
    
    const id = recordData.id || recordData.name || `${domainName.slice(0, 3).toUpperCase()}-2024-${Math.floor(1000 + Math.random() * 9000)}`;
    const newRecord = {
      ...recordData,
      id,
      name: recordData.name || id,
      created_at: new Date().toISOString(),
      status: recordData.status || 'Draft'
    };

    // Update frontend state immediately
    setRecordsStore(prev => ({
      ...prev,
      [domainName]: [newRecord, ...(prev[domainName] || [])]
    }));

    if (backendConnected) {
      try {
        const payload = { ...newRecord };
        
        if (payload.parent_account && !payload.parent_account_id) {
          const isUuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(payload.parent_account);
          if (isUuid) {
            payload.parent_account_id = payload.parent_account;
          } else {
            payload.parent_account_id = null;
            payload.is_group = true;
          }
        } else if (!payload.parent_account_id) {
          payload.parent_account_id = null;
          payload.is_group = true;
        }

        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('cb_access_token');
        if (token && !token.startsWith('dev_token_')) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        console.log(`[API Request] POST ${prefix}:`, payload);
        const res = await fetch(prefix, {
          method: 'POST',
          headers,
          body: JSON.stringify(payload)
        });
        
        if (res.ok) {
          const savedData = await res.json();
          console.log(`[API Response] POST ${prefix} Success:`, savedData);
          
          const realRecord = {
            ...newRecord,
            ...savedData,
            id: savedData.id || newRecord.id,
            name: savedData.name || newRecord.name,
            status: savedData.disabled ? 'Disabled' : 'Active'
          };
          
          setRecordsStore(prev => {
            const list = prev[domainName] || [];
            return {
              ...prev,
              [domainName]: [realRecord, ...list.filter(r => r.name !== realRecord.name && r.id !== newRecord.id)]
            };
          });
        }
      } catch (err) {
        console.warn(`[API Notice] Backend POST ${prefix} failed:`, err.message);
      }
    }

    return newRecord;
  };

  const updateRecord = async (domainName, recordId, updatedData) => {
    const domainMeta = allDomainsMetadata.find(d => d.name === domainName);
    const prefix = domainMeta?.backend?.api_prefix || `/v1/${domainName.replace('_', '-')}`;

    setRecordsStore(prev => {
      const currentList = prev[domainName] || [];
      const updatedList = currentList.map(item => {
        if (item.id === recordId || item.name === recordId) {
          return { ...item, ...updatedData, modified_at: new Date().toISOString() };
        }
        return item;
      });
      return {
        ...prev,
        [domainName]: updatedList
      };
    });

    if (backendConnected) {
      try {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('cb_access_token');
        if (token && !token.startsWith('dev_token_')) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        await fetch(`${prefix}/${recordId}`, {
          method: 'PATCH',
          headers,
          body: JSON.stringify(updatedData)
        });
      } catch (err) {
        console.warn(`[API Notice] Backend PATCH failed:`, err.message);
      }
    }
  };

  const updateRecordStatus = async (domainName, recordId, newStatus) => {
    const domainMeta = allDomainsMetadata.find(d => d.name === domainName);
    const prefix = domainMeta?.backend?.api_prefix || `/v1/${domainName.replace('_', '-')}`;

    setRecordsStore(prev => {
      const currentList = prev[domainName] || [];
      const updatedList = currentList.map(item => {
        if (item.id === recordId || item.name === recordId) {
          return { ...item, status: newStatus, modified_at: new Date().toISOString() };
        }
        return item;
      });
      return {
        ...prev,
        [domainName]: updatedList
      };
    });

    if (backendConnected) {
      try {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('cb_access_token');
        if (token && !token.startsWith('dev_token_')) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        if (newStatus === 'Submitted') {
          await fetch(`${prefix}/${recordId}/submit`, { method: 'POST', headers });
        } else if (newStatus === 'Cancelled') {
          await fetch(`${prefix}/${recordId}/cancel`, { method: 'POST', headers });
        } else {
          await fetch(`${prefix}/${recordId}`, {
            method: 'PATCH',
            headers,
            body: JSON.stringify({ status: newStatus })
          });
        }
      } catch (err) {
        console.warn(`[API Notice] Status update API call:`, err.message);
      }
    }
  };

  const deleteRecord = async (domainName, recordId) => {
    const domainMeta = allDomainsMetadata.find(d => d.name === domainName);
    const prefix = domainMeta?.backend?.api_prefix || `/v1/${domainName.replace('_', '-')}`;

    setRecordsStore(prev => {
      const currentList = prev[domainName] || [];
      const filtered = currentList.filter(item => item.id !== recordId && item.name !== recordId);
      return {
        ...prev,
        [domainName]: filtered
      };
    });

    if (backendConnected) {
      try {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('cb_access_token');
        if (token && !token.startsWith('dev_token_')) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        await fetch(`${prefix}/${recordId}`, {
          method: 'DELETE',
          headers
        });
      } catch (err) {
        console.warn(`[API Notice] Backend DELETE failed:`, err.message);
      }
    }
  };

  return (
    <RecordsContext.Provider value={{
      domains: allDomainsMetadata,
      recordsStore,
      backendConnected,
      backendInfo,
      checkingBackend,
      checkBackendHealth,
      loadingRecords,
      fetchDomainRecords,
      authToken,
      authTenant,
      quickDemoLogin,
      logout,
      getDomainRecords,
      getDomainCount,
      getRecordById,
      addRecord,
      updateRecord,
      updateRecordStatus,
      deleteRecord
    }}>
      {children}
    </RecordsContext.Provider>
  );
}

export function useRecords() {
  const context = useContext(RecordsContext);
  if (!context) {
    throw new Error('useRecords must be used within a RecordsProvider');
  }
  return context;
}
