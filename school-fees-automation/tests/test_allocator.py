import pytest

from app.core.allocator import allocate_payment


def test_balance_first_ordering():
    students = [
        {"admission_no": "A", "balance": 100},
        {"admission_no": "B", "balance": 300},
        {"admission_no": "C", "balance": 200},
    ]
    # reference_order includes all students but in different order
    ref_order = ["A", "B", "C"]
    res = allocate_payment(students, 400, ref_order)
    # Highest balances: B(300) then C(200) then A(100)
    assert res["allocations"] == {"B": 300, "C": 100}
    assert res["remaining_credit"] == 0


def test_partial_payment_to_highest_balance():
    students = [
        {"admission_no": "X", "balance": 10000},
        {"admission_no": "Y", "balance": 5000},
    ]
    res = allocate_payment(students, 3000, ["X", "Y"])
    # Should allocate only to X (highest balance) until amount exhausted
    assert res["allocations"] == {"X": 3000}
    assert res["remaining_credit"] == 0


def test_overpayment_remaining_credit():
    students = [
        {"admission_no": "041", "balance": 10000},
        {"admission_no": "1043", "balance": 5000},
    ]
    res = allocate_payment(students, 20000, ["041", "1043"])  # overpay by 5000
    assert res["allocations"] == {"041": 10000, "1043": 5000}
    assert res["remaining_credit"] == 5000


def test_ignore_zero_or_negative_balances():
    students = [
        {"admission_no": "P1", "balance": 0},
        {"admission_no": "P2", "balance": -100},
        {"admission_no": "P3", "balance": 250},
    ]
    res = allocate_payment(students, 200, ["P1", "P2", "P3"])  # only P3 eligible
    assert res["allocations"] == {"P3": 200}
    assert res["remaining_credit"] == 0


def test_invalid_inputs_raise_value_error():
    students = [{"admission_no": "Z", "balance": 100}]
    with pytest.raises(ValueError):
        allocate_payment("not-a-list", 100, ["Z"])  # students not a list

    with pytest.raises(ValueError):
        allocate_payment(students, -1, ["Z"])  # negative amount

    with pytest.raises(ValueError):
        allocate_payment(students, 100, "not-a-list")  # reference_order not a list

    # student missing admission_no
    bad_students = [{"balance": 100}]
    with pytest.raises(ValueError):
        allocate_payment(bad_students, 50, [""])

    # student balance not int/non-negative
    bad_students = [{"admission_no": "S1", "balance": "100"}]
    with pytest.raises(ValueError):
        allocate_payment(bad_students, 50, ["S1"])