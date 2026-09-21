import React from 'react';
export default function PaymentSchedule({ schedule = [] }) {
  return <div>{schedule.map((s, i) => <div key={i}>{s.date}: {s.amount}</div>)}</div>;
}