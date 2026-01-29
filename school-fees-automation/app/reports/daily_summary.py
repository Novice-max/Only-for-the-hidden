from typing import List, Dict


def generate_summary(payments: List[Dict]) -> Dict:
    total = sum(p.get("amount", 0) for p in payments if p.get("amount"))
    count = len(payments)
    return {"total": total, "count": count}
