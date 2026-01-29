from fastapi import APIRouter, Request
from app.mpesa import parser

router = APIRouter()

@router.post("/webhook")
async def mpesa_webhook(request: Request):
    payload = await request.json()
    # Expecting either raw text under 'text' or entire message in 'message'
    text = payload.get("text") or payload.get("message") or str(payload)
    parsed = parser.parse_message(text)
    # In a real app you'd enqueue or persist the parsed payment here
    return {"status": "received", "parsed": parsed}
