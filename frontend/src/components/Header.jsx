import React from 'react';

export default function Header({ currentTab, setTab }) {
  return (
    <header className="header-bar">
      <div>
        <span className="logo">Document Explainer</span>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>AI Document Intelligence</p>
      </div>
      <nav className="nav-links">
        <button className={currentTab === 'home' ? 'active' : ''} onClick={() => setTab('home')}>Upload</button>
        <button className={currentTab === 'results' ? 'active' : ''} onClick={() => setTab('results')}>Analysis</button>
        <button className={currentTab === 'documents' ? 'active' : ''} onClick={() => setTab('documents')}>Documents</button>
      </nav>
    </header>
  );
}