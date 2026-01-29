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


def parse_reference(raw: str) -> list[str]:
    """Parse a PayBill reference string into a list of numeric parts.

    Rules:
    - Accept separators '|' and ',' (either or both).
    - Strip whitespace around parts.
    - All parts must be numeric (digits only).
    - Reject empty input or empty parts.
    - Reject duplicates.
    - Raise ValueError with a clear message on invalid input.
    """
    if raw is None:
        raise ValueError("Reference string is None")

    s = raw.strip()
    if not s:
        raise ValueError("Empty reference string")

    # Disallow any characters other than digits, whitespace, '|' and ','
    invalid_chars = sorted(set(re.findall(r"[^0-9\|,\s]", s)))
    if invalid_chars:
        chars = "".join(invalid_chars)
        raise ValueError(f"Invalid character(s) in reference string: {chars}")

    parts = [p.strip() for p in re.split(r"[|,]", s)]

    if any(p == "" for p in parts):
        raise ValueError("Empty reference part found")

    for p in parts:
        if not p.isdigit():
            raise ValueError(f"Non-numeric reference part: '{p}'")

    # Detect duplicates
    seen = set()
    dupes = []
    for p in parts:
        if p in seen:
            if p not in dupes:
                dupes.append(p)
        else:
            seen.add(p)
    if dupes:
        raise ValueError(f"Duplicate references found: {', '.join(dupes)}")

    return parts
