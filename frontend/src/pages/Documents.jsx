import React, { useEffect, useState } from 'react';
import { documentsService } from '../services/documents';
import { formatDate } from '../utils/formatters';

export default function Documents({ onSelectDoc }) {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    documentsService.list()
      .then((res) => setDocs(res.documents || []))
      .catch(() => setDocs([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading records...</div>;

  return (
    <div className="card">
      <h2 style={{ fontSize: '1.25rem', marginBottom: 16 }}>Authorized Documents</h2>
      {!docs.length ? (
        <p style={{ color: 'var(--text-muted)' }}>No documents stored yet.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border)' }}>
              <th style={{ padding: 8 }}>Type</th>
              <th style={{ padding: 8 }}>Summary Preview</th>
              <th style={{ padding: 8 }}>Date</th>
              <th style={{ padding: 8 }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {docs.map((d) => (
              <tr key={d.id} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: 8 }}>{d.document_type}</td>
                <td style={{ padding: 8, fontSize: '0.85rem' }}>{d.summary}</td>
                <td style={{ padding: 8, fontSize: '0.85rem' }}>{formatDate(d.created_at)}</td>
                <td style={{ padding: 8 }}>
                  <button
                    onClick={() => onSelectDoc(d.id)}
                    style={{ padding: '4px 8px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}