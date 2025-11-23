"""
Data Router - File Upload and Profiling
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
import shutil
from pathlib import Path
import uuid
import logging

from app.core.config import settings
from app.services.data_profiler import data_profiler
from app.models.data_models import ProfileResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/data/upload", response_model=ProfileResponse)
async def upload_and_profile(
    file: UploadFile = File(...),
    use_llm: bool = Form(True),
    description: Optional[str] = Form(None)
):
    """
    Upload a data file and get automatic profiling with LLM insights
    
    Supported formats: CSV, Excel, JSON, Parquet
    """
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        file_path = Path(settings.UPLOAD_DIR) / f"{unique_id}_{file.filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File uploaded: {file.filename} ({file_size / 1024:.1f}KB)")
        
        # Profile the data
        profile_result = await data_profiler.profile_file(
            file_path=str(file_path),
            file_name=file.filename,
            use_llm=use_llm
        )
        
        # Add upload metadata
        profile_result["upload_id"] = unique_id
        profile_result["file_size_mb"] = file_size / 1024 / 1024
        profile_result["description"] = description
        
        return profile_result
        
    except Exception as e:
        logger.error(f"Upload/profiling failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Close file
        await file.close()


@router.get("/data/profile/{upload_id}")
async def get_profile(upload_id: str):
    """
    Get profiling results for a previously uploaded file
    """
    # This would retrieve from database in production
    # For now, return simple response
    return {
        "upload_id": upload_id,
        "status": "To be implemented - database integration needed"
    }


@router.delete("/data/{upload_id}")
async def delete_upload(upload_id: str):
    """
    Delete an uploaded file and its profile
    """
    try:
        # Find and delete file
        upload_dir = Path(settings.UPLOAD_DIR)
        files = list(upload_dir.glob(f"{upload_id}_*"))
        
        if not files:
            raise HTTPException(status_code=404, detail="Upload not found")
        
        for file_path in files:
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
        
        return {
            "success": True,
            "message": f"Upload {upload_id} deleted"
        }
        
    except Exception as e:
        logger.error(f"Delete failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))