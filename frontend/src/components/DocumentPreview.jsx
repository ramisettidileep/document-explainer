import React from 'react';

export default function DocumentPreview({ text, fileName }) {
  return (
    <div className="card">
      <h3 style={{ fontSize: '1rem', marginBottom: 8 }}>Input Document: {fileName}</h3>
      <pre style={{ maxHeight: 160, overflowY: 'auto', background: '#f8fafc', padding: 12, borderRadius: 6, fontSize: '0.85rem' }}>
        {text}
      </pre>
    </div>
  );
}