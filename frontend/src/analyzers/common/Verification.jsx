import React from 'react';
export default function Verification({ calculations = [] }) {
  return <div>{calculations.map((c, i) => <div key={i}>{c.description}</div>)}</div>;
}