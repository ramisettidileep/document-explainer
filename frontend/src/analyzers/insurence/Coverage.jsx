import React from 'react';
export default function Coverage({ coverages = [] }) {
  return <div>{coverages.map((c, i) => <div key={i}>{c.item}</div>)}</div>;
}