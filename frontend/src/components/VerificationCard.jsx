import React from 'react';

export default function VerificationCard({ calculations = [] }) {
  return (
    <div className="card">
      <h3 style={{ fontSize: '1.1rem', marginBottom: 12 }}>Deterministic Math Verification</h3>
      {!calculations.length ? (
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>No arithmetic formulas identified in this document.</p>
      ) : (
        calculations.map((c, i) => (
          <div key={i} style={{ padding: 12, background: '#f8fafc', borderRadius: 8, marginBottom: 8, border: '1px solid var(--border)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: 600 }}>{c.description}</span>
              <span className={`status-badge ${c.status}`}>{c.status === 'verified' ? '✓ Verified' : '⚠ Mismatch'}</span>
            </div>
            <div style={{ fontSize: '0.85rem', marginTop: 6, color: 'var(--text-muted)' }}>
              Calculated: {c.calculated} | Expected: {c.expected} {c.difference > 0 && `(Diff: ${c.difference})`}
            </div>
          </div>
        ))
      )}
    </div>
  );
}