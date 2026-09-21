import React, { useState } from 'react';

export default function EvidencePanel({ evidence = [] }) {
  const [expanded, setExpanded] = useState(false);
  if (!evidence.length) return null;

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ fontSize: '1.1rem' }}>Grounded Source Evidence</h3>
        <button
          onClick={() => setExpanded(!expanded)}
          style={{ background: 'transparent', border: '1px solid var(--border)', padding: '6px 12px', borderRadius: 6, cursor: 'pointer' }}
        >
          {expanded ? 'Hide Evidence' : `Show (${evidence.length}) Citations`}
        </button>
      </div>
      {expanded && (
        <div style={{ marginTop: 14 }}>
          {evidence.map((ev, i) => (
            <div key={i} className="evidence-box">
              <div style={{ fontWeight: 600 }}>"{ev.claim}"</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>
                Page {ev.source?.page} • Section: {ev.source?.section}
              </div>
              <div style={{ fontStyle: 'italic', marginTop: 4 }}>"{ev.source?.text}"</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}