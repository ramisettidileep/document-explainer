import React from 'react';
export default function Evidence({ evidence = [] }) {
  return <div>{evidence.map((e, i) => <div key={i}>{e.claim}</div>)}</div>;
}