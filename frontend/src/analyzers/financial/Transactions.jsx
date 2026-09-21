import React from 'react';
export default function Transactions({ txs = [] }) {
  return <div>{txs.map((t, i) => <div key={i}>{t.id} - {t.amount}</div>)}</div>;
}
