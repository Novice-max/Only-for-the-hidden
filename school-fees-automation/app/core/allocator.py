from typing import Dict, Any, List


def allocate_payment(
    students: List[Dict[str, Any]],
    amount: int,
    reference_order: List[str],
) -> Dict[str, Any]:
    """Allocate `amount` to students (balance-first) and return allocations.

    - `students` is a list of dicts containing at least `admission_no` (str)
      and `balance` (int >= 0).
    - `amount` is the total payment amount (int >= 0).
    - `reference_order` is a list of admission_no strings (from parse_reference).

    Rules:
    - Ignore students with balance <= 0.
    - Consider only students whose `admission_no` appears in `reference_order`.
    - Sort eligible students by highest balance first. Tie-break deterministically
      using the order in `reference_order`.
    - Allocate up to each student's balance sequentially until `amount` is
      exhausted. Do not mutate input objects.
    - Return a dict: {"allocations": {admission_no: allocated_int, ...},
      "remaining_credit": int}

    Raises ValueError for invalid inputs.
    """
    # Validation
    if not isinstance(students, list):
        raise ValueError("students must be a list of dicts")
    if not isinstance(reference_order, list):
        raise ValueError("reference_order must be a list of admission numbers")
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("amount must be a non-negative integer")

    # Build mapping of admission_no -> student (validate entries)
    student_map: Dict[str, Dict[str, Any]] = {}
    for idx, s in enumerate(students):
        if not isinstance(s, dict):
            raise ValueError(f"student at index {idx} is not a dict")
        if "admission_no" not in s:
            raise ValueError(f"student at index {idx} missing 'admission_no'")
        if "balance" not in s:
            raise ValueError(f"student at index {idx} missing 'balance'")
        adm = s["admission_no"]
        bal = s["balance"]
        if not isinstance(adm, str):
            raise ValueError(f"admission_no at index {idx} must be a string")
        if not isinstance(bal, int):
            raise ValueError(f"balance for {adm!s} must be an int")
        # keep first occurrence if duplicates in students list
        if adm not in student_map:
            student_map[adm] = {"admission_no": adm, "balance": bal}

    # Determine eligible students in reference_order without duplicates
    seen_refs = set()
    eligible = []  # list of tuples (admission_no, balance, ref_index)
    for ref_index, adm in enumerate(reference_order):
        if not isinstance(adm, str):
            raise ValueError("reference_order must contain strings")
        if adm in seen_refs:
            continue
        seen_refs.add(adm)
        stud = student_map.get(adm)
        if stud is None:
            continue
        bal = stud.get("balance", 0)
        if bal <= 0:
            continue
        eligible.append((adm, bal, ref_index))

    # Sort by highest balance first, tie-breaker: lower ref_index
    eligible.sort(key=lambda t: (-t[1], t[2]))

    remaining = amount
    allocations: Dict[str, int] = {}

    for adm, bal, _ in eligible:
        if remaining <= 0:
            break
        alloc = bal if remaining >= bal else remaining
        if alloc > 0:
            allocations[adm] = int(alloc)
            remaining -= alloc

    return {"allocations": allocations, "remaining_credit": int(remaining)}

