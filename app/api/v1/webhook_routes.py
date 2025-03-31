"""
Webhook API Routes (v1)

This module defines the API routes for handling BlockCypher webhook callbacks.
Part of the v1 API for the payment gateway application.
"""

from app.infrastructure.providers.blockcypher.webhooks import BlockcypherWebhookHandler, simulate_webhook
from fastapi import APIRouter, Request, HTTPException
from typing import Optional

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/payment")
async def payment_webhook(request: Request):
    """
    Endpoint for receiving BlockCypher webhook callbacks for payment processing.
    
    This endpoint handles various types of blockchain events including:
    - Unconfirmed transactions
    - Transaction confirmations
    - Double-spend detections
    
    Returns:
        JSON response indicating receipt of the webhook
    """
    try:
        # Get the raw request data for signature verification
        request_data = await request.body()
        
        # Parse the JSON data
        request_json = await request.json()
        
        # Process the webhook
        result = BlockcypherWebhookHandler.handle_payment_webhook(
            request_data,
            request_json
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid webhook data: {str(e)}")

@router.get("/transactions/{tx_hash}")
async def get_transaction_status(tx_hash: str):
    """
    Get the status of a transaction that was previously received via webhook.
    
    Args:
        tx_hash: The transaction hash to look up
        
    Returns:
        Transaction details if found
    """
    result = BlockcypherWebhookHandler.get_transaction_status(tx_hash)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@router.post("/simulate")
async def simulate_payment_webhook(
    event_type: str = "unconfirmed-tx", 
    address: Optional[str] = None,
    confirmations: int = 1
):
    """
    Development-only endpoint to simulate a webhook call.
    This is useful for testing without actual blockchain transactions.
    
    Args:
        event_type: Type of event to simulate (unconfirmed-tx, tx-confirmation, double-spend-tx)
        address: Optional specific address to use in the simulation
        confirmations: Number of confirmations (for tx-confirmation events)
        
    Returns:
        Simulated webhook response
    """
    # This endpoint should be disabled in production
    result = simulate_webhook(
        event_type=event_type,
        address=address or "simulated_address",
        confirmations=confirmations
    )
    
    return result 