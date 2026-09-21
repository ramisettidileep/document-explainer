import React, { useState } from 'react';
import { chatService } from '../services/chat';

export default function DocumentChat({ documentId }) {
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);
  const [asking, setAsking] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim() || asking) return;
    const currentQ = query;
    setQuery('');
    setAsking(true);
    try {
      const res = await chatService.ask(documentId, currentQ);
      setHistory((prev) => [...prev, { q: currentQ, a: res.answer }]);
    } catch (err) {
      setHistory((prev) => [...prev, { q: currentQ, a: `Error: ${err.message}` }]);
    } finally {
      setAsking(false);
    }
  };

  return (
    <div className="card">
      <h3 style={{ fontSize: '1.1rem', marginBottom: 12 }}>Document Grounded Q&A</h3>
      <div style={{ maxHeight: 240, overflowY: 'auto', marginBottom: 12 }}>
        {history.map((h, i) => (
          <div key={i} style={{ marginBottom: 10 }}>
            <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>You: {h.q}</div>
            <div style={{ fontSize: '0.9rem', color: '#334155', marginTop: 2 }}>Explainer: {h.a}</div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          style={{ flex: 1, padding: '8px 12px', borderRadius: 6, border: '1px solid var(--border)' }}
          placeholder="Ask a question strictly grounded in this document..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          style={{ padding: '8px 16px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}
          disabled={asking}
        >
          {asking ? 'Searching...' : 'Ask'}
        </button>
      </form>
    </div>
  );
}