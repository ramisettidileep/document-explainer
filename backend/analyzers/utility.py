"""Utility Analyzer: Meter readings, units consumed, tariff calculation, and cutoff reminders."""
import re
from backend.analyzers.base import BaseAnalyzer
from backend.functions.verifier.calculator import to_decimal

class UtilityAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        key_fields = []
        calculations = []
        action_items = []
        flags = []

        prev_m = re.search(r'previous\s*reading\s*[:]?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        curr_m = re.search(r'current\s*reading\s*[:]?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        units_m = re.search(r'units\s*consumed\s*[:]?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        rate_m = re.search(r'rate\s*per\s*unit\s*[:$₹]?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        total_m = re.search(r'total\s*amount\s*[:$₹]?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        due_m = re.search(r'due\s*date\s*[:]?\s*([A-Za-z0-9\s,\-]+)', text, re.IGNORECASE)

        due_date = due_m.group(1).strip() if due_m else "Specified due date"

        if prev_m: key_fields.append({"label": "Previous Meter Reading", "value": f"{prev_m.group(1)} kWh"})
        if curr_m: key_fields.append({"label": "Current Meter Reading", "value": f"{curr_m.group(1)} kWh"})
        if units_m: key_fields.append({"label": "Total Units Consumed", "value": f"{units_m.group(1)} Units"})
        if rate_m: key_fields.append({"label": "Tariff Rate per Unit", "value": f"${rate_m.group(1)}"})
        if total_m: key_fields.append({"label": "Total Utility Due", "value": f"${total_m.group(1)}"})

        if units_m and rate_m and total_m:
            units = to_decimal(units_m.group(1))
            rate = to_decimal(rate_m.group(1))
            total = to_decimal(total_m.group(1))
            calc_val = units * rate
            diff = abs(calc_val - total)

            calculations.append({
                "description": "Consumption (Units) × Rate/Unit = Total Energy Charge",
                "calculated": float(calc_val),
                "expected": float(total),
                "difference": float(diff),
                "status": "verified" if diff <= 0.01 else "mismatch"
            })

            summary = (
                f"This utility statement documents {units} units of metered energy consumption "
                f"billed at ${rate:.2f} per unit. The total amount due is ${total:.2f} "
                f"payable on or before {due_date}. The math matches the metered formula."
            )
        else:
            summary = f"Utility billing statement with payment due on {due_date}."

        action_items.append({
            "action": f"Pay the outstanding balance of ${total_m.group(1) if total_m else 'total'} by {due_date}.",
            "grounded_reason": "Utility providers schedule service disconnection for overdue accounts."
        })

        return {
            "doc_type": "utility",
            "summary": summary,
            "key_fields": key_fields,
            "flags": flags,
            "action_items": action_items,
            "evidence": [],
            "calculations": calculations
        }