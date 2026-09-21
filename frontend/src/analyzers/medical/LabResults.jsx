import React from 'react';
export default function LabResults({ results = [] }) {
  return <div>{results.map((r, i) => <div key={i}>{r.test}: {r.result}</div>)}</div>;
}