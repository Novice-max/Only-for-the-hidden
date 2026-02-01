import re


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
