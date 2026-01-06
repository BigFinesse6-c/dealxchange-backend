import stripe
from fastapi import APIRouter
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter()

@router.post("/payments/intro-fee")
async def create_intro_fee_session(payload: dict):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Deal Introduction Fee"
                },
                "unit_amount": 1999
            },
            "quantity": 1
        }],
        success_url=f"{settings.FRONTEND_URL}/deal-success?deal_id={payload['deal_id']}",
        cancel_url=f"{settings.FRONTEND_URL}/buyer-feed"
    )

    return {"url": session.url}
