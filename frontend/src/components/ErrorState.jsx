import React from 'react';

export default function ErrorState({ error, onRetry }) {
  return (
    <div className="card" style={{ borderColor: '#fca5a5', background: '#fef2f2' }}>
      <h3 style={{ color: '#b91c1c', fontSize: '1rem' }}>An error occurred</h3>
      <p style={{ fontSize: '0.9rem', color: '#7f1d1d', marginTop: 4 }}>{error}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          style={{ marginTop: 12, padding: '6px 12px', background: '#b91c1c', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}
        >
          Retry
        </button>
      )}
    </div>
  );
}