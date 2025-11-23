"""
Health Check Router
"""

from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/models")
async def list_models():
    """List available LLM models"""
    return {
        "available_models": {
            "claude": "claude-sonnet-4-20250514",
            "gpt4": "gpt-4o",
            "gemini": "gemini-1.5-pro",
            "azure": "azure/gpt-4o",
        },
        "default_model": settings.DEFAULT_MODEL,
        "vision_model": settings.VISION_MODEL,
    }