import React from 'react';
export default function ReferenceRanges({ ranges = [] }) {
  return <div>{ranges.map((r, i) => <div key={i}>{r.test} - Range: {r.reference_range}</div>)}</div>;
}