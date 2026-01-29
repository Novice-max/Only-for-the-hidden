from fastapi import FastAPI
from app.mpesa.webhook import router as mpesa_router

app = FastAPI(title="School Fees Automation")
app.include_router(mpesa_router, prefix="/mpesa")

@app.get("/")
def root():
    return {"status": "ok", "service": "school-fees-automation"}
