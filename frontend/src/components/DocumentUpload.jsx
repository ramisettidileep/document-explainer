import React, { useState } from 'react';
import DropZone from './DropZone';

export default function DocumentUpload({ onUpload }) {
  const [text, setText] = useState('');
  const [fileName, setFileName] = useState('');

  const handleFileLoaded = (loadedText, loadedName) => {
    setText(loadedText);
    setFileName(loadedName);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) {
      alert('Please select a file or paste document text first.');
      return;
    }
    onUpload(text, fileName || 'document.txt');
  };

  return (
    <div className="card">
      <h2 style={{ fontSize: '1.25rem', marginBottom: 12 }}>Upload or Paste Document</h2>
      
      <DropZone onTextLoaded={handleFileLoaded} />

      {fileName && (
        <div style={{ marginTop: 12, padding: '8px 14px', background: '#eff6ff', borderRadius: 8, display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: '0.9rem', color: '#1d4ed8' }}>
          📄 <strong>{fileName}</strong> (Ready to analyze)
        </div>
      )}

      <div style={{ marginTop: 20 }}>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: 8 }}>
          Document Content Preview:
        </p>
        <textarea
          rows={8}
          style={{ 
            width: '100%', 
            padding: 12, 
            borderRadius: 8, 
            border: '1px solid var(--border)',
            fontFamily: 'monospace',
            fontSize: '0.88rem'
          }}
          placeholder="Paste agreement text, clinical report, or bank statement entries..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        
        <div style={{ marginTop: 12, display: 'flex', gap: 10 }}>
          <button
            style={{ 
              padding: '10px 20px', 
              background: text.trim() ? 'var(--accent)' : '#94a3b8', 
              color: '#fff', 
              border: 'none', 
              borderRadius: 8, 
              cursor: text.trim() ? 'pointer' : 'not-allowed',
              fontWeight: 600
            }}
            disabled={!text.trim()}
            onClick={handleSubmit}
          >
            Analyze Document
          </button>
          
          {text && (
            <button
              style={{
                padding: '10px 16px',
                background: 'transparent',
                border: '1px solid var(--border)',
                borderRadius: 8,
                cursor: 'pointer'
              }}
              onClick={() => { setText(''); setFileName(''); }}
            >
              Clear
            </button>
          )}
        </div>
      </div>
    </div>
  );
}