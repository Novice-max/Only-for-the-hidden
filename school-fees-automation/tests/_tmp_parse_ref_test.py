from app.mpesa.parser import parse_reference

cases = [
    "041|1043",
    "041,1043",
    "041 & 1043",
    "",
    "041|041",
    "041|  1043 ,205"
]
for c in cases:
    try:
        print(f"{c!r} -> {parse_reference(c)}")
    except Exception as e:
        print(f"{c!r} -> ERROR: {type(e).__name__}: {e}")
