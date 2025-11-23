"""
Pydantic Models for Data Endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ColumnAnalysis(BaseModel):
    """Column-level analysis"""
    name: str
    dtype: str
    null_count: int
    null_percentage: float
    unique_count: int
    unique_percentage: float
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    std: Optional[float] = None
    avg_length: Optional[float] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    sample_values: Optional[List[Any]] = None
    min_date: Optional[str] = None
    max_date: Optional[str] = None


class QualityIssue(BaseModel):
    """Data quality issue"""
    severity: str
    type: str
    column: Optional[str] = None
    description: str
    recommendation: str


class LLMInsights(BaseModel):
    """LLM-generated insights"""
    insights: str
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    error: Optional[str] = None


class BasicStats(BaseModel):
    """Basic dataset statistics"""
    row_count: int
    column_count: int
    memory_usage_mb: float
    duplicate_rows: int
    total_nulls: int
    null_percentage: float


class ProfileResponse(BaseModel):
    """Data profiling response"""
    file_name: str
    timestamp: str
    basic_stats: BasicStats
    columns: List[ColumnAnalysis]
    quality_issues: List[QualityIssue]
    llm_insights: Optional[LLMInsights] = None
    upload_id: Optional[str] = None
    file_size_mb: Optional[float] = None
    description: Optional[str] = None
    success: bool


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None