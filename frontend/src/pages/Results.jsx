import React from 'react';
import AnalysisDashboard from '../components/AnalysisDashboard';
import LoadingState from '../components/LoadingState';

export default function Results({ documentData }) {
  if (!documentData) {
    return <LoadingState message="No analysis selected. Upload a document to view results." />;
  }
  return <AnalysisDashboard documentData={documentData} />;
}