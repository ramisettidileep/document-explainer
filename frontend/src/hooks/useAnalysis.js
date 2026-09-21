import { useState } from 'react';
import { documentsService } from '../services/documents';

export function useAnalysis() {
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);

  const submitDocument = async (text, fileName) => {
    setProcessing(true);
    setError(null);
    try {
      const resp = await documentsService.create(text, fileName);
      return resp.id;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setProcessing(false);
    }
  };

  return { submitDocument, processing, error };
}