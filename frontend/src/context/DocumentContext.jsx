import React, { createContext, useContext, useState } from 'react';

const DocumentContext = createContext(null);

export function DocumentProvider({ children }) {
  const [activeDocId, setActiveDocId] = useState(null);
  const [userRole, setUserRole] = useState('user');

  return (
    <DocumentContext.Provider value={{ activeDocId, setActiveDocId, userRole, setUserRole }}>
      {children}
    </DocumentContext.Provider>
  );
}

export function useDocContext() {
  return useContext(DocumentContext);
}