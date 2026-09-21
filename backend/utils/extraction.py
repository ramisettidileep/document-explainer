"""Deterministic regex extraction helper functions."""
import re
from decimal import Decimal
from typing import Optional, Tuple

def extract_monetary_amount(pattern: str, text: str) -> Tuple[Optional[Decimal], Optional[str]]:
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        raw_val = match.group(1).replace(",", "").replace("$", "").replace("₹", "").strip()
        try:
            return Decimal(raw_val), match.group(0)
        except Exception:
            return None, None
    return None, None