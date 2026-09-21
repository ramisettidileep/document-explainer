import React from 'react';

export default function ProcessingStatus() {
  return (
    <div className="card" style={{ textAlign: 'center', padding: 32 }}>
      <p style={{ fontWeight: 600 }}>Analyzing Document Grounding...</p>
      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 8 }}>
        Parsing sections, evaluating deterministic verification, and constructing plain explanation.
      </p>
    </div>
  );
}