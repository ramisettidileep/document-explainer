import React from 'react';
export default function Obligations({ obligations = [] }) {
  return <div>{obligations.map((o, i) => <div key={i}>{o.party}: {o.duty}</div>)}</div>;
}