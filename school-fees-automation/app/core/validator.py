from typing import Dict


def validate_payment(payment: Dict) -> bool:
    # Basic validation placeholder
    return bool(payment.get("amount") and payment.get("amount") > 0)
