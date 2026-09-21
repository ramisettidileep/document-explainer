import React from 'react';

export default function FlagsCard({ flags = [] }) {
  if (!flags.length) return null;
  return (
    <div className="card">
      <h3 style={{ fontSize: '1.1rem', marginBottom: 12 }}>Important Flags & Notices</h3>
      {flags.map((fl, i) => (
        <div key={i} className="status-badge notice" style={{ display: 'block', marginBottom: 8, padding: 8 }}>
          {fl.message}
        </div>
      ))}
    </div>
  );
}