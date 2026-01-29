from typing import Dict, Any, List


def allocate_payment(payment: Dict[str, Any], students: List[Dict[str, Any]]):
    """Placeholder allocator that finds matching student by invoice/ref."""
    ref = payment.get("invoice")
    if not ref:
        return None
    for s in students:
        if s.get("invoice") == ref:
            # apply allocation logic here
            return {"student_id": s.get("id"), "allocated": True}
    return None
