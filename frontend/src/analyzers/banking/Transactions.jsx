import React from 'react';
export default function Transactions({ items = [] }) {
  return <div>{items.map((it, i) => <div key={i}>{it.description} - {it.amount}</div>)}</div>;
}