import React from 'react';
import DocumentClassifier from './DocumentClassifier';
import SummaryCard from './SummaryCard';
import KeyInformation from './KeyInformation';
import VerificationCard from './VerificationCard';
import FlagsCard from './FlagsCard';
import ActionItems from './ActionItems';
import EvidencePanel from './EvidencePanel';
import DocumentChat from './DocumentChat';

export default function AnalysisDashboard({ documentData }) {
  const { id, classification, result } = documentData;
  const docType = result?.doc_type || classification?.document_type || 'general';

  return (
    <div>
      {/* Top Header & Classifier Tag */}
      <DocumentClassifier classification={classification} />

      {/* Main Executive Summary */}
      <SummaryCard summary={result.summary} />

      {/* Deterministic Math Audit (Crucial for Banking, Financial, Utility) */}
      {result.calculations && result.calculations.length > 0 && (
        <VerificationCard calculations={result.calculations} />
      )}

      {/* 1. LEGAL-SPECIFIC VIEW: Plain English Clauses Translator */}
      {docType === 'legal' && result.clauses && result.clauses.length > 0 && (
        <div className="card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <h3 style={{ fontSize: '1.15rem', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 8 }}>
            <span>⚖️</span> Plain-Language Clause Translation
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 16 }}>
            Legal jargon from the contract translated into plain English:
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {result.clauses.map((c, i) => (
              <div key={i} style={{ background: '#f8fafc', padding: 14, borderRadius: 8, border: '1px solid var(--border)' }}>
                <div style={{ fontWeight: 600, color: '#1e3a8a', fontSize: '0.95rem' }}>{c.title}</div>
                <div style={{ margin: '6px 0', fontSize: '0.9rem', color: '#1e293b' }}>
                  <strong>What this means:</strong> {c.plain_english}
                </div>
                <blockquote style={{ fontSize: '0.8rem', color: '#64748b', fontStyle: 'italic', borderLeft: '2px solid #cbd5e1', paddingLeft: 8, marginTop: 4 }}>
                  "{c.document_text}"
                </blockquote>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. INSURANCE-SPECIFIC VIEW: Covered vs. Excluded Breakdown Matrix */}
      {docType === 'insurance' && result.coverage_matrix && result.coverage_matrix.length > 0 && (
        <div className="card" style={{ borderLeft: '4px solid #10b981' }}>
          <h3 style={{ fontSize: '1.15rem', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 8 }}>
            <span>🛡️</span> Policy Coverage & Exclusion Matrix
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 14 }}>
            Detailed breakdown of what the insurance company pays for versus what you pay:
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {result.coverage_matrix.map((item, idx) => {
              const isCovered = item.status === 'covered';
              return (
                <div 
                  key={idx} 
                  style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'space-between',
                    padding: '10px 14px', 
                    background: isCovered ? '#f0fdf4' : '#fef2f2', 
                    borderRadius: 8, 
                    border: isCovered ? '1px solid #bbf7d0' : '1px solid #fecaca' 
                  }}
                >
                  <div>
                    <span style={{ fontWeight: 600, color: isCovered ? '#166534' : '#991b1b', fontSize: '0.9rem' }}>
                      {item.item}
                    </span>
                    <div style={{ fontSize: '0.8rem', color: isCovered ? '#15803d' : '#b91c1c' }}>
                      {item.explanation}
                    </div>
                  </div>
                  <span 
                    style={{ 
                      padding: '4px 10px', 
                      borderRadius: 9999, 
                      fontSize: '0.75rem', 
                      fontWeight: 700,
                      background: isCovered ? '#dcfce7' : '#fee2e2',
                      color: isCovered ? '#15803d' : '#b91c1c'
                    }}
                  >
                    {isCovered ? '✓ COVERED' : '✗ EXCLUDED'}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Key Fields Grid */}
      <KeyInformation fields={result.key_fields} />

      {/* Warnings & Risk Flags */}
      <FlagsCard flags={result.flags} />

      {/* Next Steps & Action Items */}
      <ActionItems items={result.action_items} />

      {/* Grounded Citations Panel */}
      <EvidencePanel evidence={result.evidence} />

      {/* Grounded Interactive Q&A Box */}
      <DocumentChat documentId={id} />
    </div>
  );
}