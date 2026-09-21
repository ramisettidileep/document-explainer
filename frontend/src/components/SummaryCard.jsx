import React from 'react';

export default function SummaryCard({ summary }) {
  return (
    <div className="card">
      <h3 style={{ fontSize: '1.1rem', marginBottom: 10 }}>Plain Language Summary</h3>
      <p style={{ lineHeight: 1.6, color: '#334155' }}>{summary}</p>
    </div>
  );
}