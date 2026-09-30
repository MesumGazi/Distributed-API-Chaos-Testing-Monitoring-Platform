import httpx
import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.services import url_validation
from config.config import setting
from database.database import get_db
from database.models import HealthCheck
from datetime import datetime, timedelta

router = APIRouter()

urls = [setting.url] * setting.attempts

@router.get("/check")
async def is_google_up(db: Session = Depends(get_db)):
    semaphore = asyncio.Semaphore(setting.max_concurrency_limit)
    async with httpx.AsyncClient(timeout=5.0) as client:
        async def semaphore_limit(url):
            async with semaphore:
                return await url_validation(url, client)
        tasks = [semaphore_limit(url) for url in urls]
        results = await asyncio.gather(*tasks)
    healthy_count = sum(1 for r in results if r.get("status_code", 0) < 500)
    response_time = [r["elapsed_time"] for r in results if "elapsed_time" in r]
    for r in results:
        record = HealthCheck(
            url=r.get("url"),
            status_code=r.get("status_code"),
            response_time=r.get("elapsed_time"),
            is_healthy=r.get("status_code", 0) < 500,
            status_message=r.get("status_message"),
            error_message=r.get("error"),
        )
        db.add(record)
    db.commit()
    return {
        "summary": {
            "total_checks": len(results),
            "healthy_url_count": healthy_count,
            "unhealthy_url_count": len(results) - healthy_count,
            "avg_response_time": sum(response_time) / len(response_time) if response_time else 0,
            "max_response_time": max(response_time) if response_time else 0,
        },
        "results": results,
    }

@router.get("/history")
async def get_history(
    url: str = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get check history for the last N hours"""
    query = db.query(HealthCheck)
    if url:
        query = query.filter(HealthCheck.url == url)
    since = datetime.utcnow() - timedelta(hours=hours)
    query = query.filter(HealthCheck.checked_at > since)
    checks = query.order_by(HealthCheck.checked_at.desc()).limit(1000).all()
    return {
        "url_filter": url,
        "period_hours": hours,
        "total_checks": len(checks),
        "checks": [
            {
                "url": c.url,
                "status_code": c.status_code,
                "is_healthy": c.is_healthy,
                "response_time": c.response_time,
                "checked_at": c.checked_at.isoformat()
            }
            for c in checks
        ]
    }