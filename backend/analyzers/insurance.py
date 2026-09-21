"""Insurance Analyzer: Categorizes coverage, deductibles, exclusions, and claim requirements."""
import re
from backend.analyzers.base import BaseAnalyzer
from backend.utils.extraction import extract_monetary_amount

class InsuranceAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        key_fields = []
        evidence = []
        flags = []
        action_items = []
        coverage_matrix = []

        holder_m = re.search(r'policyholder\s*[:]?\s*([A-Za-z\s\.]+)', text, re.IGNORECASE)
        policy_no_m = re.search(r'policy\s*(?:number|no\.?)\s*[:]?\s*([A-Za-z0-9\-]+)', text, re.IGNORECASE)
        sum_insured, si_raw = extract_monetary_amount(r'sum insured\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        deductible, ded_raw = extract_monetary_amount(r'deductible\s*[:$₹]?\s*([\d,]+\.?\d*)', text)
        premium, _ = extract_monetary_amount(r'premium\s*[:$₹]?\s*([\d,]+\.?\d*)', text)

        holder = holder_m.group(1).strip() if holder_m else "Insured Party"
        if policy_no_m:
            key_fields.append({"label": "Policy Number", "value": policy_no_m.group(1).strip()})
        if sum_insured is not None:
            key_fields.append({"label": "Sum Insured (Coverage Limit)", "value": f"${sum_insured:,.2f}"})
        if deductible is not None:
            key_fields.append({"label": "Out-of-Pocket Deductible", "value": f"${deductible:,.2f}"})
        if premium is not None:
            key_fields.append({"label": "Policy Premium", "value": f"${premium:,.2f}"})

        # Scan for Inclusions and Exclusions
        lines = text.split('\n')
        for line in lines:
            clean = line.strip()
            lower = clean.lower()
            if any(k in lower for k in ["is covered", "covered up to", "inpatient", "eligible"]):
                coverage_matrix.append({
                    "item": clean.replace("1.", "").replace("2.", "").strip(),
                    "status": "covered",
                    "explanation": "Explicitly included under policy protection."
                })
            elif any(k in lower for k in ["exclusion", "excluded", "not covered", "pre-existing", "cosmetic"]):
                coverage_matrix.append({
                    "item": clean.replace("3.", "").replace("Exclusions:", "").strip(),
                    "status": "excluded",
                    "explanation": "Out of pocket: Insurer will not pay for this category."
                })
                flags.append({
                    "type": "warning",
                    "message": f"Coverage Exclusion: {clean}"
                })

        sum_str = f"${sum_insured:,.2f}" if sum_insured is not None else "the stated limit"
        ded_str = f"${deductible:,.2f}" if deductible is not None else "the stated amount"

        summary = (
            f"This insurance certificate provides up to {sum_str} in coverage "
            f"for {holder}. The policy requires an out-of-pocket deductible of "
            f"{ded_str} before insurance payouts activate. "
            f"Review the coverage breakdown below to see what is paid versus excluded."
        )

        action_items.append({
            "action": f"Budget for the {ded_str} deductible in the event of a claim.",
            "grounded_reason": "Deductible must be settled by the policyholder before benefits are disbursed."
        })
        action_items.append({
            "action": "Check exclusion criteria before incurring elective or pre-existing medical costs.",
            "grounded_reason": "Policy explicitly denies reimbursement for excluded treatments."
        })

        return {
            "doc_type": "insurance",
            "summary": summary,
            "key_fields": key_fields,
            "coverage_matrix": coverage_matrix,
            "flags": flags,
            "action_items": action_items,
            "evidence": evidence,
            "calculations": []
        }