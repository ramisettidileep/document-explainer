"""Heuristic domain classifier with keyword scoring."""
import re
from typing import Dict, Any

DOMAIN_LEXICON = {
    "medical": ["hemoglobin", "mg/dl", "patient", "clinical", "lab result", "doctor", "diagnosis", "serum", "platelet"],
    "banking": ["statement", "account balance", "withdrawal", "deposit", "cheque", "closing balance", "neft", "rtgs"],
    "insurance": ["policyholder", "deductible", "claim", "coverage", "premium", "exclusions", "sum insured"],
    "legal": ["agreement", "hereby", "party", "jurisdiction", "termination", "indemnity", "warranties", "covenant"],
    "financial": ["invoice", "tax", "subtotal", "gst", "due date", "interest rate", "principal", "loan", "amortization"],
    "utility": ["kwh", "units consumed", "meter reading", "tariff", "electricity bill", "water bill", "consumer number"]
}

class DocumentClassifier:
    def classify(self, text: str) -> Dict[str, Any]:
        lower_text = text.lower()
        scores = {}
        for category, keywords in DOMAIN_LEXICON.items():
            matches = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', lower_text))
            scores[category] = matches

        best_category = max(scores, key=scores.get)
        match_count = scores[best_category]

        if match_count >= 2:
            confidence = min(0.60 + (match_count * 0.08), 0.98)
            return {
                "document_type": best_category,
                "confidence": round(confidence, 2),
                "reason": f"Matched {match_count} domain markers for {best_category}."
            }

        return {
            "document_type": "general",
            "confidence": 0.50,
            "reason": "Text does not contain strong distinguishing domain keywords."
        }