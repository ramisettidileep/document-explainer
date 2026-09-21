import React from 'react';
export default function Exclusions({ exclusions = [] }) {
  return <div>{exclusions.map((e, i) => <div key={i}>{e.clause}</div>)}</div>;
}