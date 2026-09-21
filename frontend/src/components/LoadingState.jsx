import React from 'react';

export default function LoadingState({ message = 'Loading...' }) {
  return <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>{message}</div>;
}