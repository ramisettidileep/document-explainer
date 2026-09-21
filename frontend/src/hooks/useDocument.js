import { useState, useCallback } from 'react';
import { documentsService } from '../services/documents';

export function useDocument() {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDocument = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    try {
      const data = await documentsService.get(id);
      setDoc(data);
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { doc, loading, error, fetchDocument, setDoc };
}