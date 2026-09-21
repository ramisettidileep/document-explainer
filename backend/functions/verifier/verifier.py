"""Verification coordinator for financial and banking documents."""
from backend.functions.verifier.calculator import verify_sum, verify_balance

class Verifier:
    @staticmethod
    def verify_document(doc_type: str, data: dict) -> list:
        checks = []
        if doc_type in ["banking", "financial"] and "opening_balance" in data and "closing_balance" in data:
            checks.append({
                "description": "Opening + Deposits - Withdrawals = Closing Balance",
                **verify_balance(
                    data.get("opening_balance"),
                    data.get("total_deposits", 0),
                    data.get("total_withdrawals", 0),
                    data.get("closing_balance")
                )
            })
        if "line_items" in data and "stated_total" in data:
            checks.append({
                "description": "Sum of line items = Total Amount",
                **verify_sum(data.get("line_items", []), data.get("stated_total"))
            })
        return checks