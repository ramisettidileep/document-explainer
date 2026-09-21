import React from 'react';
export default function ActionItems({ items = [] }) {
  return <ul>{items.map((it, i) => <li key={i}>{it.action}</li>)}</ul>;
}