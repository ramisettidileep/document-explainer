"""Deterministic calculator engine. Floating point math is never delegated to the LLM."""
from decimal import Decimal, ROUND_HALF_UP

def to_decimal(val) -> Decimal:
    if val is None:
        return Decimal('0')
    if isinstance(val, (int, float, Decimal)):
        return Decimal(str(val))
    cleaned = str(val).replace(",", "").replace("$", "").replace("₹", "").strip()
    return Decimal(cleaned)

def verify_sum(items: list, stated_total) -> dict:
    try:
        calculated = sum([to_decimal(x) for x in items], Decimal('0'))
        expected = to_decimal(stated_total)
        diff = abs(calculated - expected)
        is_match = diff <= Decimal('0.01')
        return {
            "status": "verified" if is_match else "mismatch",
            "calculated": float(calculated.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            "expected": float(expected.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            "difference": float(diff.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        }
    except Exception as e:
        return {"status": "unable_to_verify", "reason": str(e)}

def verify_balance(opening, deposits, withdrawals, stated_closing) -> dict:
    try:
        op = to_decimal(opening)
        dep = to_decimal(deposits)
        wd = to_decimal(withdrawals)
        expected = to_decimal(stated_closing)
        calculated = op + dep - wd
        diff = abs(calculated - expected)
        is_match = diff <= Decimal('0.01')
        return {
            "status": "verified" if is_match else "mismatch",
            "calculated": float(calculated.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            "expected": float(expected.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            "difference": float(diff.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        }
    except Exception as e:
        return {"status": "unable_to_verify", "reason": str(e)}