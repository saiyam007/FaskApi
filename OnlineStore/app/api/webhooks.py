# app/api/webhooks.py
# OnlineStore/app/api/webhooks.py
import os
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import database, crud, schemas

router = APIRouter()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")  # from .env

@router.post("/webhooks/payment", tags=["Webhooks"], summary="Payment Webhook")
async def payment_webhook(request: Request, session: Session = Depends(database.get_session)):
    raw_body = await request.body()
    provided_sig = request.headers.get("X-Payment-Signature")
    if not provided_sig:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature")

    computed_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_sig, provided_sig):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")

    payload = await request.json()

    if payload.get("event") == "payment.succeeded":
        order_id = payload["data"]["order_id"]
        order = crud.get_order(session, order_id)
        order.status = schemas.OrderStatus.PAID
        session.add(order)
        session.commit()
        session.refresh(order)

    return {"received": True}
