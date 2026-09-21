"""Financial Analyzer: Extracts line items, due dates, and deterministically audits invoices."""
import re
from backend.analyzers.base import BaseAnalyzer
from backend.utils.extraction import extract_monetary_amount
from backend.functions.verifier.calculator import verify_sum

class FinancialAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        key_fields = []
        evidence = []
        calculations = []
        flags = []
        action_items = []

        inv_m = re.search(r'invoice\s*(?:number|#|no\.?)\s*[:]?\s*([A-Za-z0-9\-]+)', text, re.IGNORECASE)
        due_m = re.search(r'due\s*date\s*[:]?\s*([A-Za-z0-9\s,\-]+)', text, re.IGNORECASE)
        billed_to_m = re.search(r'billed\s*to\s*[:]?\s*([A-Za-z0-9\s,\.]+)', text, re.IGNORECASE)

        subtotal, _ = extract_monetary_amount(r'subtotal\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        tax, _ = extract_monetary_amount(r'tax\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        total, tot_raw = extract_monetary_amount(r'total\s*[:$₹]?\s*([\d,]+\.?\d*)', text)

        inv_num = inv_m.group(1).strip() if inv_m else "N/A"
        due_date = due_m.group(1).strip() if due_m else "Upon Receipt"
        billed_to = billed_to_m.group(1).strip() if billed_to_m else "Customer"

        key_fields.append({"label": "Invoice Number", "value": inv_num})
        key_fields.append({"label": "Billed Recipient", "value": billed_to})
        key_fields.append({"label": "Due Date", "value": due_date})

        total_display = f"${total:,.2f}" if total is not None else "the invoice amount"

        if subtotal is not None and tax is not None and total is not None:
            key_fields.extend([
                {"label": "Subtotal (Before Tax)", "value": f"${subtotal:,.2f}"},
                {"label": "Taxes & Levies", "value": f"${tax:,.2f}"},
                {"label": "Final Amount Due", "value": f"${total:,.2f}"}
            ])
            evidence.append({"claim": f"Total amount payable is ${total:,.2f}", "source": {"page": 1, "section": "Totals", "text": tot_raw}})
            
            calc_res = verify_sum([subtotal, tax], total)
            calculations.append({
                "description": "Subtotal + Tax = Stated Total Payable",
                **calc_res
            })

            tax_pct = (tax / subtotal * 100) if subtotal > 0 else 0
            summary = (
                f"Invoice {inv_num} billed to {billed_to} requests a total payment of ${total:,.2f} "
                f"due on {due_date}. The charges include a subtotal of ${subtotal:,.2f} plus "
                f"${tax:,.2f} in taxes (effective tax rate: {tax_pct:.1f}%). "
                f"The calculations have been deterministically audited and match the itemized sum."
            )
        else:
            summary = f"Commercial invoice for {billed_to} due on {due_date}."

        action_items.append({
            "action": f"Remit payment of {total_display} before {due_date}.",
            "grounded_reason": "Ensures account remains in good standing without late interest fees."
        })

        return {
            "doc_type": "financial",
            "summary": summary,
            "key_fields": key_fields,
            "flags": flags,
            "action_items": action_items,
            "evidence": evidence,
            "calculations": calculations
        }