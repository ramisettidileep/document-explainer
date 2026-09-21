import React from 'react';

export default function ActionItems({ items = [] }) {
  if (!items.length) return null;
  return (
    <div className="card">
      <h3 style={{ fontSize: '1.1rem', marginBottom: 12 }}>Recommended Next Steps</h3>
      <ul style={{ paddingLeft: 20 }}>
        {items.map((it, idx) => (
          <li key={idx} style={{ marginBottom: 8 }}>
            <strong>{it.action}</strong>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Reason: {it.grounded_reason}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}