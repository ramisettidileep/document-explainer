"""Upgraded Medical Report Analyzer with deterministic reference range comparison and clinical-neutral explanations."""
import re
from backend.analyzers.base import BaseAnalyzer

class MedicalAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        pages = normalized_doc.get("pages", [])
        evidence = []
        key_fields = []
        flags = []
        action_items = []

        # Matches: "Test Name: Value Unit (Min - Max)"
        pattern = re.compile(
            r'([A-Za-z\s/]{3,35})\s*:\s*([\d\.]+)\s*([a-zA-Z/%μ\^0-9]+)?\s*(?:\(([\d\.]+)\s*-\s*([\d\.]+)\))?'
        )

        abnormal_findings = []

        for match in pattern.finditer(text):
            name, val_str, unit, min_range, max_range = match.groups()
            name = name.strip()
            
            # Skip noise words
            if any(skip in name.lower() for skip in ["page", "date", "dr", "doctor", "phone", "gender", "age", "mrn", "id", "room"]):
                continue

            val = float(val_str)
            status = "Normal"
            badge = "normal"

            if min_range and max_range:
                low = float(min_range)
                high = float(max_range)
                ref_display = f"{min_range} - {max_range} {unit or ''}".strip()

                if val > high:
                    status = "Higher than standard reference range"
                    badge = "high"
                    abnormal_findings.append(f"{name} ({val} {unit or ''}) is above the normal limit of {high}")
                elif val < low:
                    status = "Lower than standard reference range"
                    badge = "low"
                    abnormal_findings.append(f"{name} ({val} {unit or ''}) is below the normal limit of {low}")
            else:
                ref_display = "Not stated"

            key_fields.append({
                "label": name,
                "value": f"{val_str} {unit or ''}".strip(),
                "reference_range": ref_display,
                "status": status,
                "badge": badge
            })

            evidence.append({
                "claim": f"{name} was measured at {val_str} {unit or ''} (Stated Range: {ref_display}).",
                "source": {
                    "page": 1,
                    "section": "Laboratory Observations",
                    "text": match.group(0).strip()
                }
            })

        # Generate a rich, document-grounded summary
        patient_m = re.search(r'patient(?:\s+name)?\s*:\s*([A-Za-z\s\.]+)', text, re.IGNORECASE)
        patient_name = patient_m.group(1).strip() if patient_m else "the patient"

        if abnormal_findings:
            summary = (
                f"This clinical report for {patient_name} outlines {len(key_fields)} recorded laboratory parameters. "
                f"Specifically, {len(abnormal_findings)} metric(s) deviate from the document's stated reference intervals: "
                f"{'; '.join(abnormal_findings)}. "
                f"The remaining measurements fall within normal documented ranges. "
                f"These values are physiological observations and require interpretation by a medical provider."
            )
            for finding in abnormal_findings:
                flags.append({
                    "type": "warning",
                    "message": f"Attention: {finding}."
                })
        else:
            summary = (
                f"This clinical diagnostic report for {patient_name} lists {len(key_fields)} laboratory parameters. "
                f"All tested values appear to sit comfortably within the reference ranges specified by the testing facility."
            )

        flags.append({
            "type": "notice",
            "message": "Informational Notice: Laboratory results reflect point-in-time analytical readings and do not constitute an independent medical diagnosis."
        })

        action_items.append({
            "action": "Review the highlighted out-of-range metrics with your referring physician.",
            "grounded_reason": "Out-of-range laboratory values require clinical evaluation in the context of symptoms and medical history."
        })
        action_items.append({
            "action": "Retain this copy for longitudinal comparison with future diagnostic tests.",
            "grounded_reason": "Tracking blood metrics over time helps clinicians evaluate health trends."
        })

        # Try to enhance summary with Ollama if running
        if self.ollama and self.ollama.is_available():
            llm_prompt = (
                f"Summarize this medical report in 3 clear plain-English sentences for a patient. "
                f"Mention which tests were abnormal. Do not diagnose or prescribe.\n\nReport:\n{text[:1200]}"
            )
            enhanced = self.ollama.generate(llm_prompt)
            if enhanced and len(enhanced.strip()) > 40:
                summary = enhanced.strip()

        return {
            "doc_type": "medical",
            "summary": summary,
            "key_fields": key_fields,
            "flags": flags,
            "action_items": action_items,
            "evidence": evidence,
            "calculations": []
        }