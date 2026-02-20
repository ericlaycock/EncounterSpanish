"""LLM Gateway for chat completions with logging and replay"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import time
import uuid
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models import LLMRequest
from app.core.logger import log_event
from app.config import settings
import os

MODEL = "gpt-4o-mini"  # Updated model name
PROVIDER = "openai"
AGENT_ID = "conversation_agent"

# Lazy initialization
_client = None

def get_client() -> OpenAI:
    """Get or create OpenAI client"""
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


@dataclass
class ConversationContext:
    """Context for LLM conversation generation"""
    request_id: str
    user_id: Optional[str]
    system_prompt: str
    user_prompt: str
    agent_id: str = AGENT_ID
    prompt_version: str = "v1"
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    return_json: bool = False


def load_prompt(agent_id: str, prompt_version: str) -> str:
    """Load prompt from prompts.json by agent_id and version"""
    import json
    from pathlib import Path
    
    prompts_path = Path(__file__).parent.parent / "prompts" / "prompts.json"
    with open(prompts_path, "r") as f:
        prompts = json.load(f)
    
    if agent_id not in prompts:
        raise ValueError(f"Agent ID '{agent_id}' not found in prompts.json")
    
    agent_prompt = prompts[agent_id]
    if agent_prompt.get("prompt_version") != prompt_version:
        raise ValueError(
            f"Prompt version mismatch: requested '{prompt_version}', "
            f"found '{agent_prompt.get('prompt_version')}'"
        )
    
    return agent_prompt["content"]


async def generate_conversation(
    context: ConversationContext,
    db: Session
) -> Dict[str, Any]:
    """
    Generate conversation response using LLM with full logging.
    
    Returns:
        Dict with 'content' (str or dict) and metadata
    """
    start_time = time.time()
    llm_request_id = uuid.uuid4()
    
    # Build messages
    messages = [
        {"role": "system", "content": context.system_prompt},
        {"role": "user", "content": context.user_prompt}
    ]
    
    # Convert user_id to UUID if string
    user_id_uuid = None
    if context.user_id:
        if isinstance(context.user_id, str):
            user_id_uuid = uuid.UUID(context.user_id)
        else:
            user_id_uuid = context.user_id
    
    # Insert initial record (success=false)
    llm_record = LLMRequest(
        id=llm_request_id,
        request_id=context.request_id,
        user_id=user_id_uuid,
        provider=PROVIDER,
        model=MODEL,
        prompt_version=context.prompt_version,
        agent_id=context.agent_id,
        messages_json=messages,
        temperature=context.temperature,
        max_tokens=context.max_tokens,
        success=False
    )
    db.add(llm_record)
    db.commit()
    db.refresh(llm_record)
    
    # Log start event
    log_event(
        level="info",
        event="llm_start",
        message=f"LLM request started: {context.agent_id} v{context.prompt_version}",
        request_id=context.request_id,
        user_id=str(context.user_id) if context.user_id else None,
        extra={
            "provider": PROVIDER,
            "model": MODEL,
            "agent_id": context.agent_id,
            "prompt_version": context.prompt_version,
        }
    )
    
    try:
        # Call OpenAI
        client = get_client()
        api_params = {
            "model": MODEL,
            "messages": messages,
        }
        
        if context.return_json:
            api_params["response_format"] = {"type": "json_object"}
        if context.temperature is not None:
            api_params["temperature"] = context.temperature
        if context.max_tokens is not None:
            api_params["max_tokens"] = context.max_tokens
        
        response = client.chat.completions.create(**api_params)
        
        # Extract response
        content = response.choices[0].message.content
        if context.return_json:
            content = json.loads(content)
        
        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Extract token usage
        usage = response.usage
        tokens_in = usage.prompt_tokens if usage else None
        tokens_out = usage.completion_tokens if usage else None
        
        # Estimate cost (rough estimates for gpt-4o-mini)
        estimated_cost = None
        if tokens_in and tokens_out:
            # gpt-4o-mini: $0.15/$0.60 per 1M tokens (input/output)
            cost_per_1m_input = 0.15
            cost_per_1m_output = 0.60
            estimated_cost = (
                (tokens_in / 1_000_000) * cost_per_1m_input +
                (tokens_out / 1_000_000) * cost_per_1m_output
            )
        
        # Update record with success
        llm_record.success = True
        llm_record.response_json = {"content": content} if isinstance(content, dict) else {"text": content}
        llm_record.latency_ms = latency_ms
        llm_record.tokens_in = tokens_in
        llm_record.tokens_out = tokens_out
        llm_record.estimated_cost = estimated_cost
        db.commit()
        
        # Log success event
        log_event(
            level="info",
            event="llm_success",
            message=f"LLM request completed: {latency_ms}ms",
            request_id=context.request_id,
            user_id=str(context.user_id) if context.user_id else None,
            extra={
                "provider": PROVIDER,
                "model": MODEL,
                "agent_id": context.agent_id,
                "latency_ms": latency_ms,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "estimated_cost": estimated_cost,
                "success": True,
            }
        )
        
        return {
            "content": content,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "latency_ms": latency_ms,
            "estimated_cost": estimated_cost,
        }
        
    except Exception as e:
        # Calculate latency even on error
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Determine error code
        error_code = type(e).__name__
        error_message = str(e)
        
        # Update record with failure
        llm_record.success = False
        llm_record.latency_ms = latency_ms
        llm_record.error_code = error_code
        llm_record.error_message = error_message
        db.commit()
        
        # Log failure event
        log_event(
            level="error",
            event="llm_failure",
            message=f"LLM request failed: {error_code} - {error_message}",
            request_id=context.request_id,
            user_id=str(context.user_id) if context.user_id else None,
            extra={
                "provider": PROVIDER,
                "model": MODEL,
                "agent_id": context.agent_id,
                "latency_ms": latency_ms,
                "error_code": error_code,
                "error_message": error_message,
                "success": False,
            }
        )
        
        # Re-raise exception
        raise

