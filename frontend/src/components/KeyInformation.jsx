import React from 'react';

export default function KeyInformation({ fields = [] }) {
  if (!fields.length) return null;

  return (
    <div className="card">
      <h3 style={{ fontSize: '1.1rem', marginBottom: 12 }}>Extracted Parameters & Metrics</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 14 }}>
        {fields.map((f, i) => {
          const isHigh = f.badge === 'high';
          const isLow = f.badge === 'low';
          const isAbnormal = isHigh || isLow;

          return (
            <div 
              key={i} 
              style={{ 
                padding: '14px 16px', 
                background: isAbnormal ? '#fff5f5' : '#f8fafc', 
                borderRadius: 10, 
                border: isAbnormal ? '1px solid #fecaca' : '1px solid var(--border)',
                transition: 'transform 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                  {f.label}
                </span>
                {f.badge && (
                  <span 
                    style={{
                      fontSize: '0.72rem',
                      fontWeight: 700,
                      padding: '2px 8px',
                      borderRadius: 6,
                      background: isAbnormal ? '#fee2e2' : '#dcfce7',
                      color: isAbnormal ? '#dc2626' : '#15803d',
                      textTransform: 'uppercase'
                    }}
                  >
                    {isHigh ? '▲ High' : isLow ? '▼ Low' : '✓ Normal'}
                  </span>
                )}
              </div>

              <div style={{ fontSize: '1.25rem', fontWeight: 700, marginTop: 6, color: isAbnormal ? '#b91c1c' : 'var(--text-primary)' }}>
                {f.value}
              </div>

              {f.reference_range && f.reference_range !== 'Not stated' && (
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
                  Reference Interval: <strong>{f.reference_range}</strong>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}