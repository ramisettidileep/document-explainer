import React from 'react';
import { DOMAIN_LABELS } from '../utils/constants';

export default function DocumentClassifier({ classification }) {
  if (!classification) return null;
  const label = DOMAIN_LABELS[classification.document_type] || classification.document_type;

  return (
    <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 16 }}>
      <span className="status-badge verified">{label}</span>
      <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        Confidence: {(classification.confidence * 100).toFixed(0)}%
      </span>
    </div>
  );
}