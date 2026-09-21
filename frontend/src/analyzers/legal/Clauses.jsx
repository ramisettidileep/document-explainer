import React from 'react';
export default function Clauses({ clauses = [] }) {
  return <div>{clauses.map((c, i) => <div key={i}>{c.title}</div>)}</div>;
}