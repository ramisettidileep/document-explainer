import React, { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

// Configure pdfjs worker to use CDN worker matching installed version
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.mjs`;

export default function DropZone({ onTextLoaded }) {
  const [drag, setDrag] = useState(false);
  const [extracting, setExtracting] = useState(false);

  const extractTextFromPDF = async (arrayBuffer) => {
    const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
    const pdf = await loadingTask.promise;
    let fullText = '';

    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map((item) => item.str).join(' ');
      fullText += `\n--- Page ${pageNum} ---\n` + pageText + '\n';
    }

    return fullText.trim();
  };

  const handleFile = async (file) => {
    if (!file) return;

    setExtracting(true);
    const fileName = file.name;
    const lowerName = fileName.toLowerCase();

    try {
      if (lowerName.endsWith('.pdf')) {
        const arrayBuffer = await file.arrayBuffer();
        const extractedText = await extractTextFromPDF(arrayBuffer);
        if (!extractedText) {
          alert('Could not extract readable text from this PDF (it may be a scanned image).');
        } else {
          onTextLoaded(extractedText, fileName);
        }
      } else {
        // Plain text, Markdown, CSV, JSON
        const reader = new FileReader();
        reader.onload = () => {
          onTextLoaded(reader.result, fileName);
        };
        reader.readAsText(file);
      }
    } catch (err) {
      console.error('Text extraction failed:', err);
      alert(`Failed to extract text from ${fileName}: ${err.message}`);
    } finally {
      setExtracting(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDrag(false);
    if (e.dataTransfer.files?.[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div
      className={`dropzone ${drag ? 'active' : ''}`}
      onDragOver={(e) => {
        e.preventDefault();
        setDrag(true);
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={handleDrop}
      style={{
        border: drag ? '2px dashed var(--accent)' : '2px dashed #cbd5e1',
        borderRadius: '12px',
        padding: '36px 20px',
        textAlign: 'center',
        background: drag ? '#eff6ff' : '#f8fafc',
        cursor: 'pointer',
        transition: 'all 0.2s ease'
      }}
    >
      {extracting ? (
        <div style={{ color: 'var(--accent)', fontWeight: 600 }}>
          ⏳ Extracting document text and page slices...
        </div>
      ) : (
        <>
          <div style={{ fontSize: '1.8rem', marginBottom: 6 }}>📄</div>
          <p style={{ fontWeight: 600, fontSize: '1rem' }}>
            Drag & drop your PDF, TXT, or MD document here
          </p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 4 }}>
            Direct text extraction with page boundary preservation
          </p>
          <label
            style={{
              marginTop: 14,
              display: 'inline-block',
              padding: '8px 16px',
              background: '#ffffff',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.88rem',
              fontWeight: 500,
              boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
            }}
          >
            Browse File
            <input
              type="file"
              accept=".pdf,.txt,.md,.text"
              style={{ display: 'none' }}
              onChange={(e) => {
                if (e.target.files?.[0]) {
                  handleFile(e.target.files[0]);
                }
              }}
            />
          </label>
        </>
      )}
    </div>
  );
}