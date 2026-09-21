"""Legal Analyzer: Extracts contractual obligations, terms, and translates clauses into plain English."""
import re
from backend.analyzers.base import BaseAnalyzer

COMMON_CLAUSE_TRANSLATIONS = {
    "indemnity": {
        "title": "Indemnification (Financial Protection)",
        "plain_explanation": "If one party gets sued or faces financial losses due to the other party's actions, the responsible party must cover those costs and legal fees."
    },
    "termination": {
        "title": "Termination (Ending the Agreement)",
        "plain_explanation": "Explains how and when either party can cancel the contract, including how many days in advance written notice must be given."
    },
    "confidentiality": {
        "title": "Confidentiality (Non-Disclosure)",
        "plain_explanation": "Both parties agree not to share private business secrets, client data, or proprietary information with outsiders."
    },
    "governing law": {
        "title": "Governing Law (Jurisdiction)",
        "plain_explanation": "Designates which state or country's legal system will handle disputes if the parties end up in court."
    },
    "severability": {
        "title": "Severability",
        "plain_explanation": "If a judge decides one sentence in this contract is illegal or invalid, the rest of the contract remains active and enforceable."
    },
    "force majeure": {
        "title": "Force Majeure (Unforeseen Disasters)",
        "plain_explanation": "Parties aren't penalized if major uncontrollable events (floods, wars, natural disasters) prevent them from fulfilling duties."
    }
}

class LegalAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        evidence = []
        key_fields = []
        flags = []
        action_items = []
        clauses = []

        # Extract Parties
        party_m = re.search(r'between\s+([A-Za-z0-9\s,\.]+?)\s*(?:and|\&)\s*([A-Za-z0-9\s,\.]+?)(?:\.|\n|\()', text, re.IGNORECASE)
        party_a = party_m.group(1).strip() if party_m else "Party A"
        party_b = party_m.group(2).strip() if party_m else "Party B"
        if party_m:
            key_fields.extend([
                {"label": "First Party", "value": party_a},
                {"label": "Second Party", "value": party_b}
            ])
            evidence.append({"claim": f"Agreement between {party_a} and {party_b}", "source": {"page": 1, "section": "Preamble", "text": party_m.group(0)}})

        # Extract Notice Period
        notice_m = re.search(r'(?:notice of\s*(\d+\s*days?)|(\d+\s*days?)\s*(?:prior\s*)?written notice)', text, re.IGNORECASE)
        if notice_m:
            notice_val = notice_m.group(1) or notice_m.group(2)
            key_fields.append({"label": "Termination Notice Period", "value": notice_val})
            evidence.append({"claim": f"Termination requires {notice_val} notice", "source": {"page": 1, "section": "Termination", "text": notice_m.group(0)}})
            action_items.append({
                "action": f"Set a calendar reminder for {notice_val} before any renewal date.",
                "grounded_reason": f"Contract mandates {notice_val} written notice to terminate without penalty."
            })
        else:
            flags.append({"type": "warning", "message": "No explicit termination notice period detected. Confirm exit terms before signing."})

        # Extract Governing Jurisdiction
        gov_m = re.search(r'(?:laws of|governed by)\s*(?:the state of|the province of)?\s*([A-Za-z\s]+?)(?:\.|\n|;)', text, re.IGNORECASE)
        if gov_m:
            jurisdiction = gov_m.group(1).strip()
            key_fields.append({"label": "Governing Jurisdiction", "value": jurisdiction})

        # Scan for Recognized Clauses and provide Plain English Translation
        text_lower = text.lower()
        for kw, trans in COMMON_CLAUSE_TRANSLATIONS.items():
            if kw in text_lower:
                # Find matching context snippet
                pattern = re.compile(rf'([^.\n]*?{kw}[^.\n]*?\.)', re.IGNORECASE)
                match = pattern.search(text)
                snippet = match.group(0).strip() if match else f"Clause concerning {kw} is present."

                clauses.append({
                    "title": trans["title"],
                    "plain_english": trans["plain_explanation"],
                    "document_text": snippet
                })
                evidence.append({
                    "claim": f"Document contains {trans['title']} clause.",
                    "source": {"page": 1, "section": "Contract Terms", "text": snippet}
                })

        summary = (
            f"This legal contract binds {party_a} and {party_b}. "
            f"Key operational terms include a {key_fields[-2]['value'] if len(key_fields) >= 3 else 'standard'} notice requirement. "
            f"The agreement contains {len(clauses)} standard commercial legal clauses translated below into everyday English. "
            f"This summary is for informational understanding and does not replace qualified legal counsel."
        )

        flags.append({
            "type": "notice",
            "message": "Notice: Explanations simplify contract language for understanding. Always review binding commitments with an attorney."
        })

        return {
            "doc_type": "legal",
            "summary": summary,
            "key_fields": key_fields,
            "clauses": clauses,
            "flags": flags,
            "action_items": action_items,
            "evidence": evidence,
            "calculations": []
        }