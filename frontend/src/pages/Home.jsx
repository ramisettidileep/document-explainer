import React from 'react';
import DocumentUpload from '../components/DocumentUpload';

export default function Home({ onUpload }) {
  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: 28 }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Understand your documents without the jargon.</h1>
        <p style={{ color: 'var(--text-muted)', marginTop: 6 }}>
          Upload any legal, banking, medical, utility, or financial document for a plain-language explanation grounded in the text.
        </p>
      </div>
      <DocumentUpload onUpload={onUpload} />
    </div>
  );
}