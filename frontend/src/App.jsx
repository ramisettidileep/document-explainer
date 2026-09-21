import React, { useState } from 'react';
import Header from './components/Header';
import SecurityStatus from './components/SecurityStatus';
import ErrorState from './components/ErrorState';
import Home from './pages/Home';
import Results from './pages/Results';
import Documents from './pages/Documents';
import { useAnalysis } from './hooks/useAnalysis';
import { useDocument } from './hooks/useDocument';

export default function App() {
  const [tab, setTab] = useState('home');
  const [customError, setCustomError] = useState(null);
  const { submitDocument, processing, error: submitError } = useAnalysis();
  const { doc, fetchDocument, error: docError } = useDocument();

  const handleUpload = async (text, name) => {
    setCustomError(null);
    try {
      const docId = await submitDocument(text, name);
      if (docId) {
        const fetched = await fetchDocument(docId);
        if (fetched) {
          setTab('results');
        } else {
          setCustomError('Document was processed, but unable to retrieve results.');
        }
      } else {
        setCustomError('Backend failed to return a document ID. Make sure the backend server is running on http://localhost:3000.');
      }
    } catch (err) {
      setCustomError(err.message || 'Failed to connect to API server.');
    }
  };

  const handleSelectDoc = async (id) => {
    setCustomError(null);
    const fetched = await fetchDocument(id);
    if (fetched) {
      setTab('results');
    }
  };

  const currentError = customError || submitError || docError;

  return (
    <div>
      <Header currentTab={tab} setTab={setTab} />
      <main className="container">
        <SecurityStatus />

        {currentError && (
          <ErrorState 
            error={currentError} 
            onRetry={() => setCustomError(null)} 
          />
        )}

        {processing ? (
          <div className="card" style={{ textAlign: 'center', padding: '48px 24px' }}>
            <div style={{ fontSize: '1.2rem', fontWeight: 600, color: 'var(--accent)' }}>
              Analyzing Document Grounding...
            </div>
            <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginTop: 8 }}>
              Extracting text slices → Identifying document type → Verifying calculations
            </div>
            <div style={{ marginTop: 20, display: 'inline-block', width: 36, height: 36, border: '3px solid #e2e8f0', borderTopColor: 'var(--accent)', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
          </div>
        ) : (
          <>
            {tab === 'home' && <Home onUpload={handleUpload} />}
            {tab === 'results' && <Results documentData={doc} />}
            {tab === 'documents' && <Documents onSelectDoc={handleSelectDoc} />}
          </>
        )}
      </main>
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}