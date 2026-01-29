import re
from typing import Dict, Optional

_AMT_RE = re.compile(r"(?i)(?:ksh|kes|shs)?\s*([0-9,]+(?:\.[0-9]{1,2})?)")
_INV_RE = re.compile(r"(?i)(?:inv(?:oice)?[:\s-]*|ref[:\s-]*|bill[:\s-]*)([A-Za-z0-9-]+)")
_PHONE_RE = re.compile(r"(?:\+?254|0)?7\d{8}")


def _clean_number(s: str) -> float:
    return float(s.replace(",", ""))


def parse_message(text: str) -> Dict[str, Optional[str]]:
    """Very small heuristic parser that extracts amount, invoice/ref and phone."""
    if not text:
        return {"amount": None, "invoice": None, "phone": None}

    amt_m = _AMT_RE.search(text)
    inv_m = _INV_RE.search(text)
    phone_m = _PHONE_RE.search(text)

    amount = _clean_number(amt_m.group(1)) if amt_m else None
    invoice = inv_m.group(1) if inv_m else None
    phone = phone_m.group(0) if phone_m else None

    return {"amount": amount, "invoice": invoice, "phone": phone}
