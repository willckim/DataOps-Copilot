"""
LiteLLM Router Service - Intelligent Multi-Model Routing
Handles Claude, GPT-4, Gemini, and Azure OpenAI with smart fallbacks
"""

from typing import List, Dict, Any, Optional, Literal
import litellm
from litellm import completion, acompletion
import os
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Configure LiteLLM
litellm.drop_params = settings.LITELLM_DROP_PARAMS
litellm.set_verbose = settings.DEBUG


class LLMRouter:
    """Intelligent multi-model router with fallback support"""
    
    def __init__(self):
        self._setup_api_keys()
        self._configure_models()
    
    def _setup_api_keys(self):
        """Set up API keys for all providers"""
        if settings.ANTHROPIC_API_KEY:
            os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY
        if settings.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        if settings.GOOGLE_API_KEY:
            os.environ["GEMINI_API_KEY"] = settings.GOOGLE_API_KEY
        if settings.AZURE_API_KEY:
            os.environ["AZURE_API_KEY"] = settings.AZURE_API_KEY
    
    def _configure_models(self):
        """Configure model routing preferences"""
        self.model_map = {
            # Primary models
            "claude": "claude-sonnet-4-20250514",  # Claude Sonnet 4.5
            "gpt5": "gpt-5-mini",  # GPT-5 mini (latest!)
            "gemini": "gemini-2.0-flash-exp",  # Gemini 2.0 Flash
            "azure": "azure/gpt-4o-mini",  # Azure GPT-4o-mini
            
            # Task-specific routing
            "reasoning": "claude-sonnet-4-20250514",
            "speed": "gpt-5-mini",
            "vision": "gemini-2.0-flash-exp",
            "structured": "gpt-5-mini",
        }
        
        self.task_routing = {
            "data_profiling": ["claude", "gpt5"],
            "sql_generation": ["claude", "gpt5"],
            "vision_ocr": ["gemini", "gpt5"],
            "code_generation": ["gpt5", "claude"],
            "complex_reasoning": ["claude", "gpt5"],
            "simple_query": ["gpt5", "claude"],
        }
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        task_type: str = "reasoning",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Intelligent completion with automatic fallback
        
        Args:
            messages: List of message dicts with role and content
            task_type: Type of task (data_profiling, sql_generation, etc.)
            model: Specific model to use (overrides task_type routing)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the model
        
        Returns:
            Response dict with content and metadata
        """
        # Determine which models to try
        if model:
            models_to_try = [model]
        else:
            task_models = self.task_routing.get(task_type, ["claude", "gpt4"])
            models_to_try = [self.model_map.get(m, m) for m in task_models]
        
        last_error = None
        
        # Try each model with fallback
        for model_name in models_to_try:
            try:
                logger.info(f"Attempting completion with model: {model_name}")
                
                response = await acompletion(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=settings.LITELLM_TIMEOUT,
                    **kwargs
                )
                
                # Extract content
                content = response.choices[0].message.content
                
                return {
                    "content": content,
                    "model": model_name,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    },
                    "success": True
                }
                
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {str(e)}")
                last_error = e
                continue
        
        # All models failed
        logger.error(f"All models failed. Last error: {last_error}")
        raise Exception(f"All models failed. Last error: {str(last_error)}")
    
    async def complete_with_vision(
        self,
        text_prompt: str,
        image_data: str,
        image_format: str = "png",
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Complete with vision model (for dashboard OCR, etc.)
        
        Args:
            text_prompt: Text instruction
            image_data: Base64 encoded image data
            image_format: Image format (png, jpg, etc.)
            model: Specific model to use (defaults to Gemini)
        
        Returns:
            Response dict with extracted content
        """
        model_name = model or self.model_map["vision"]
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/{image_format};base64,{image_data}"
                    }
                ]
            }
        ]
        
        try:
            response = await acompletion(
                model=model_name,
                messages=messages,
                **kwargs
            )
            
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "model": model_name,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Vision completion failed: {str(e)}")
            raise
    
    async def structured_output(
        self,
        messages: List[Dict[str, str]],
        response_format: Dict[str, Any],
        task_type: str = "structured",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get structured JSON output from model
        
        Args:
            messages: List of message dicts
            response_format: JSON schema for response
            task_type: Type of task
        
        Returns:
            Structured response
        """
        return await self.complete(
            messages=messages,
            task_type=task_type,
            response_format=response_format,
            **kwargs
        )
    
    def get_cost_estimate(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a completion
        
        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Estimated cost in USD
        """
        # Pricing per 1M tokens (as of November 2025)
        pricing = {
            "claude-sonnet-4-5-20250929": {"input": 3.0, "output": 15.0},  # Claude Sonnet 4.5
            "gpt-5-mini": {"input": 0.15, "output": 0.60},  # GPT-5 mini (estimate - check OpenAI for actual)
            "gemini-1.5-pro": {"input": 0.0, "output": 0.0},  # Gemini 2.0 Flash (FREE!)
            "azure/gpt-4o-mini": {"input": 0.165, "output": 0.66},  # Azure GPT-4o-mini
        }
        
        if model in pricing:
            input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
            output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]
            return input_cost + output_cost
        
        return 0.0


# Global router instance
llm_router = LLMRouter()