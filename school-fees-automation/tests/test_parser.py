from app.mpesa.parser import parse_message


def test_parse_message_basic():
    text = "Paid KSh 1,500 for INV12345 by 254700000000"
    parsed = parse_message(text)
    assert parsed["amount"] == 1500.0
    assert parsed["invoice"] == "INV12345"
    assert parsed["phone"] == "254700000000"
