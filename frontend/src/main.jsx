import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { DocumentProvider } from './context/DocumentContext';
import './styles/globals.css';
import './styles/components.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <DocumentProvider>
      <App />
    </DocumentProvider>
  </React.StrictMode>
);