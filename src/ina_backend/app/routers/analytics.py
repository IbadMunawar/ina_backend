# --- IMPORTS ---
from ..schemas import AnalyticsLogCreate
from ..models import AnalyticsLog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..redis_client import redis_client
from src.ina_backend.app.database import get_db


router=APIRouter()

# --- NEW ENDPOINT: Week 3 Day 2 ---
@router.post("/log")
async def log_analytics(
    payload: AnalyticsLogCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Week 3 Push Model: The Orchestrator reports the final outcome.
    1. Check Redis to find which Tenant owns this session_id.
    2. Save the result to Postgres for long-term storage.
    """

    # 1. Retrieve Session Data from Redis
    redis_key = f"session:{payload.session_id}"
    session_data = await redis_client.hgetall(redis_key)

    if not session_data:
        # If Redis returns empty, the session might have expired or is invalid.
        # We can either reject it or save it as 'Unknown Tenant'. 
        # For now, let's reject it to ensure data integrity.
        raise HTTPException(status_code=404, detail="Session not found or expired")

    tenant_id = session_data.get("tenant_id")

    # 2. Create the Log Record in Postgres
    new_log = AnalyticsLog(
        session_id=payload.session_id,
        tenant_id=int(tenant_id),  # Convert string back to int
        result=payload.result,
        final_price=payload.final_price,
        transcript_summary=payload.transcript_summary
    )

    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)

    return {"status": "logged", "log_id": new_log.id}