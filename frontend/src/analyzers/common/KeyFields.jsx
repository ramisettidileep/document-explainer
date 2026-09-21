import React from 'react';
export default function KeyFields({ fields = [] }) {
  return (
    <div className="card">
      <h3>Key Fields</h3>
      {fields.map((f, idx) => (
        <div key={idx}><strong>{f.label}:</strong> {f.value}</div>
      ))}
    </div>
  );
}