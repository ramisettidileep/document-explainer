import React from 'react';

export default function Settings() {
  return (
    <div className="card">
      <h3>System Settings</h3>
      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 8 }}>
        Cedar authorization and local Ollama endpoint configuration.
      </p>
    </div>
  );
}