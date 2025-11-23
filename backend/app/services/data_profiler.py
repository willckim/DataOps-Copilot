"""
Data Profiling Service
Analyzes uploaded data and generates quality reports using LLM
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import polars as pl
import duckdb
from pathlib import Path
import logging
from datetime import datetime

from app.services.llm_router import llm_router

logger = logging.getLogger(__name__)


class DataProfiler:
    """Intelligent data profiling with LLM-powered insights"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.parquet']
    
    async def profile_file(
        self,
        file_path: str,
        file_name: str,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        Profile a data file and generate comprehensive report
        
        Args:
            file_path: Path to uploaded file
            file_name: Original filename
            use_llm: Whether to use LLM for insights (default: True)
        
        Returns:
            Comprehensive profiling report
        """
        try:
            # Load data
            df = self._load_data(file_path, file_name)
            
            # Basic profiling
            basic_stats = self._generate_basic_stats(df)
            
            # Column-level analysis
            column_analysis = self._analyze_columns(df)
            
            # Data quality issues
            quality_issues = self._detect_quality_issues(df)
            
            # LLM-powered insights
            llm_insights = None
            if use_llm:
                llm_insights = await self._generate_llm_insights(
                    basic_stats=basic_stats,
                    column_analysis=column_analysis,
                    quality_issues=quality_issues,
                    sample_data=df.head(5).to_dict(orient='records')
                )
            
            return {
                "file_name": file_name,
                "timestamp": datetime.now().isoformat(),
                "basic_stats": basic_stats,
                "columns": column_analysis,
                "quality_issues": quality_issues,
                "llm_insights": llm_insights,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Profiling failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _load_data(self, file_path: str, file_name: str) -> pd.DataFrame:
        """Load data from various formats"""
        suffix = Path(file_name).suffix.lower()
        
        if suffix == '.csv':
            return pd.read_csv(file_path)
        elif suffix in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif suffix == '.json':
            return pd.read_json(file_path)
        elif suffix == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def _generate_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate basic statistics about the dataset"""
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "duplicate_rows": df.duplicated().sum(),
            "total_nulls": df.isnull().sum().sum(),
            "null_percentage": (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100),
        }
    
    def _analyze_columns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze each column in detail"""
        columns = []
        
        for col in df.columns:
            col_data = df[col]
            
            analysis = {
                "name": col,
                "dtype": str(col_data.dtype),
                "null_count": int(col_data.isnull().sum()),
                "null_percentage": float(col_data.isnull().sum() / len(df) * 100),
                "unique_count": int(col_data.nunique()),
                "unique_percentage": float(col_data.nunique() / len(df) * 100),
            }
            
            # Numeric columns
            if pd.api.types.is_numeric_dtype(col_data):
                analysis.update({
                    "min": float(col_data.min()) if not col_data.isnull().all() else None,
                    "max": float(col_data.max()) if not col_data.isnull().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isnull().all() else None,
                    "median": float(col_data.median()) if not col_data.isnull().all() else None,
                    "std": float(col_data.std()) if not col_data.isnull().all() else None,
                })
            
            # String columns
            elif pd.api.types.is_string_dtype(col_data) or col_data.dtype == 'object':
                non_null = col_data.dropna()
                if len(non_null) > 0:
                    analysis.update({
                        "avg_length": float(non_null.astype(str).str.len().mean()),
                        "max_length": int(non_null.astype(str).str.len().max()),
                        "min_length": int(non_null.astype(str).str.len().min()),
                        "sample_values": non_null.head(3).tolist(),
                    })
            
            # Datetime columns
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                analysis.update({
                    "min_date": str(col_data.min()) if not col_data.isnull().all() else None,
                    "max_date": str(col_data.max()) if not col_data.isnull().all() else None,
                })
            
            columns.append(analysis)
        
        return columns
    
    def _detect_quality_issues(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect data quality issues"""
        issues = []
        
        # High null percentage
        for col in df.columns:
            null_pct = df[col].isnull().sum() / len(df) * 100
            if null_pct > 20:
                issues.append({
                    "severity": "high" if null_pct > 50 else "medium",
                    "type": "high_null_percentage",
                    "column": col,
                    "description": f"Column '{col}' has {null_pct:.1f}% null values",
                    "recommendation": f"Consider dropping this column or imputing values"
                })
        
        # Duplicate rows
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            issues.append({
                "severity": "medium",
                "type": "duplicate_rows",
                "description": f"Found {dup_count} duplicate rows ({dup_count/len(df)*100:.1f}%)",
                "recommendation": "Review and remove duplicate entries"
            })
        
        # Low cardinality in string columns
        for col in df.select_dtypes(include=['object']).columns:
            unique_pct = df[col].nunique() / len(df) * 100
            if unique_pct < 1 and df[col].nunique() > 1:
                issues.append({
                    "severity": "low",
                    "type": "low_cardinality",
                    "column": col,
                    "description": f"Column '{col}' has very few unique values ({df[col].nunique()})",
                    "recommendation": "Consider converting to categorical type"
                })
        
        # Potential ID columns (high cardinality)
        for col in df.columns:
            if df[col].nunique() / len(df) > 0.95:
                issues.append({
                    "severity": "info",
                    "type": "potential_id_column",
                    "column": col,
                    "description": f"Column '{col}' appears to be an ID column (high uniqueness)",
                    "recommendation": "Use as primary key or index"
                })
        
        return issues
    
    async def _generate_llm_insights(
        self,
        basic_stats: Dict,
        column_analysis: List[Dict],
        quality_issues: List[Dict],
        sample_data: List[Dict]
    ) -> Dict[str, Any]:
        """Generate LLM-powered insights and recommendations"""
        
        prompt = f"""You are a data analytics expert. Analyze this dataset profile and provide insights.

DATASET OVERVIEW:
- Rows: {basic_stats['row_count']:,}
- Columns: {basic_stats['column_count']}
- Duplicate rows: {basic_stats['duplicate_rows']}
- Total nulls: {basic_stats['total_nulls']} ({basic_stats['null_percentage']:.1f}%)

COLUMN SUMMARY:
{self._format_columns_for_llm(column_analysis)}

QUALITY ISSUES:
{self._format_issues_for_llm(quality_issues)}

SAMPLE DATA (first 3 rows):
{sample_data[:3]}

Provide:
1. **Business Context**: What kind of data is this? What business domain does it belong to?
2. **Data Quality Assessment**: Overall quality rating (1-10) and key concerns
3. **Recommended Cleaning Steps**: Specific actions to improve data quality
4. **Potential Use Cases**: What analyses or insights could this data support?
5. **Schema Recommendations**: Suggested data types, indexes, or relationships

Be concise but specific. Focus on actionable insights."""

        try:
            response = await llm_router.complete(
                messages=[{"role": "user", "content": prompt}],
                task_type="data_profiling",
                temperature=0.3,
                max_tokens=2000
            )
            
            return {
                "insights": response["content"],
                "model_used": response["model"],
                "tokens_used": response["usage"]["total_tokens"]
            }
            
        except Exception as e:
            logger.error(f"LLM insights generation failed: {str(e)}")
            return {
                "insights": "LLM insights unavailable",
                "error": str(e)
            }
    
    def _format_columns_for_llm(self, columns: List[Dict]) -> str:
        """Format column analysis for LLM"""
        lines = []
        for col in columns[:10]:  # Limit to first 10 columns
            line = f"- {col['name']} ({col['dtype']}): {col['unique_count']} unique, {col['null_percentage']:.1f}% null"
            lines.append(line)
        
        if len(columns) > 10:
            lines.append(f"... and {len(columns) - 10} more columns")
        
        return "\n".join(lines)
    
    def _format_issues_for_llm(self, issues: List[Dict]) -> str:
        """Format quality issues for LLM"""
        if not issues:
            return "No major quality issues detected"
        
        lines = []
        for issue in issues[:5]:  # Limit to top 5 issues
            lines.append(f"- [{issue['severity'].upper()}] {issue['description']}")
        
        if len(issues) > 5:
            lines.append(f"... and {len(issues) - 5} more issues")
        
        return "\n".join(lines)


# Global profiler instance
data_profiler = DataProfiler()