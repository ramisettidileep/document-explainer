"""Upgraded Banking Analyzer with automated net-flow calculation and transactional audit."""
import re
from backend.analyzers.base import BaseAnalyzer
from backend.utils.extraction import extract_monetary_amount
from backend.functions.verifier.calculator import verify_balance, to_decimal

class BankingAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        key_fields = []
        evidence = []
        calculations = []
        flags = []
        action_items = []

        opening, op_raw = extract_monetary_amount(r'opening balance\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        closing, cl_raw = extract_monetary_amount(r'closing balance\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        deposits, dep_raw = extract_monetary_amount(r'total deposits\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        withdrawals, wd_raw = extract_monetary_amount(r'total withdrawals\s*[:$₹]?\s*([\d,]+\.?\d*)', text)

        holder_m = re.search(r'account holder\s*[:]?\s*([A-Za-z\s\.]+)', text, re.IGNORECASE)
        holder = holder_m.group(1).strip() if holder_m else "Account Holder"

        period_m = re.search(r'statement period\s*[:]?\s*([A-Za-z0-9\s,\-]+)', text, re.IGNORECASE)
        period = period_m.group(1).strip() if period_m else "the designated period"

        if opening is not None:
            key_fields.append({"label": "Opening Balance", "value": f"${opening:,.2f}"})
            evidence.append({"claim": f"Opening balance is ${opening:,.2f}", "source": {"page": 1, "section": "Summary", "text": op_raw}})
        if deposits is not None:
            key_fields.append({"label": "Total Deposits", "value": f"${deposits:,.2f}"})
        if withdrawals is not None:
            key_fields.append({"label": "Total Withdrawals", "value": f"${withdrawals:,.2f}"})
        if closing is not None:
            key_fields.append({"label": "Closing Balance", "value": f"${closing:,.2f}"})
            evidence.append({"claim": f"Closing balance is ${closing:,.2f}", "source": {"page": 1, "section": "Summary", "text": cl_raw}})

        net_flow_text = ""
        if deposits is not None and withdrawals is not None:
            net_movement = deposits - withdrawals
            if net_movement > 0:
                net_flow_text = f"positive cash flow of +${net_movement:,.2f}"
            else:
                net_flow_text = f"net outflow of -${abs(net_movement):,.2f}"
            key_fields.append({"label": "Net Cash Movement", "value": f"{'+' if net_movement > 0 else ''}${net_movement:,.2f}"})

        # Deterministic Verification
        if opening is not None and deposits is not None and withdrawals is not None and closing is not None:
            calc_res = verify_balance(opening, deposits, withdrawals, closing)
            calculations.append({
                "description": "Opening Balance + Deposits - Withdrawals = Closing Balance",
                **calc_res
            })

            if calc_res["status"] == "verified":
                summary = (
                    f"This monthly banking statement for {holder} covering {period} shows an opening balance of "
                    f"${opening:,.2f} and a closing balance of ${closing:,.2f}. During this statement cycle, the account experienced a "
                    f"{net_flow_text} (Deposits: ${deposits:,.2f}, Withdrawals: ${withdrawals:,.2f}). "
                    f"All account figures have been deterministically audited and reconcile perfectly with zero discrepancy."
                )
            else:
                summary = (
                    f"Audit Warning: This banking statement for {holder} contains an arithmetic discrepancy. "
                    f"Opening balance (${opening:,.2f}) + Deposits (${deposits:,.2f}) - Withdrawals (${withdrawals:,.2f}) "
                    f"equals ${calc_res['calculated']:,.2f}, but the stated closing balance is ${closing:,.2f} "
                    f"(Difference: ${calc_res['difference']:,.2f})."
                )
                flags.append({
                    "type": "mismatch",
                    "message": f"Arithmetic Mismatch: Statement summary numbers do not reconcile mathematically by ${calc_res['difference']:,.2f}."
                })
        else:
            summary = f"Account statement for {holder} covering {period}. Detailed balances extracted above."

        action_items.append({
            "action": "Review individual withdrawal line items against payment records.",
            "grounded_reason": "Verifying transaction receipts ensures all debits were legitimate."
        })

        return {
            "doc_type": "banking",
            "summary": summary,
            "key_fields": key_fields,
            "flags": flags,
            "action_items": action_items,
            "evidence": evidence,
            "calculations": calculations
        }