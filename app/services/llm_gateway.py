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

MODEL = "gpt-5.4-mini"
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
    learning_phase: Optional[str] = None
    messages: Optional[List[Dict[str, str]]] = None  # Full message history (overrides system_prompt + user_prompt)


def load_prompt(agent_id: str, prompt_version: str = "v2") -> str:
    """Load prompt template from prompts.json by agent_id."""
    import json
    from pathlib import Path

    prompts_path = Path(__file__).parent.parent / "prompts" / "prompts.json"
    with open(prompts_path, "r") as f:
        prompts = json.load(f)

    if agent_id not in prompts:
        raise ValueError(f"Agent ID '{agent_id}' not found in prompts.json")

    return prompts[agent_id]["content"]


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
    
    # Build messages — use full history if provided, otherwise system+user pair
    if context.messages:
        messages = context.messages
    else:
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
    extra_llm_start = {
        "provider": PROVIDER,
        "model": MODEL,
        "agent_id": context.agent_id,
        "prompt_version": context.prompt_version,
    }
    if context.learning_phase:
        extra_llm_start["learning_phase"] = context.learning_phase
    log_event(
        level="info",
        event="llm_start",
        message=f"LLM request started: {context.agent_id} v{context.prompt_version}",
        request_id=context.request_id,
        user_id=str(context.user_id) if context.user_id else None,
        extra=extra_llm_start
    )
    
    try:
        # Call OpenAI
        client = get_client()
        api_params = {
            "model": MODEL,
            "messages": messages,
            "reasoning": {"effort": "low"},
        }

        if context.return_json:
            api_params["response_format"] = {"type": "json_object"}
        if context.temperature is not None:
            api_params["temperature"] = context.temperature
        if context.max_tokens is not None:
            api_params["max_tokens"] = context.max_tokens
        
        response = client.chat.completions.create(**api_params)
        
        # Extract response — strip any reasoning tags that leak into content
        import re
        content = response.choices[0].message.content
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
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
            # gpt-5.4-mini: $0.75/$4.50 per 1M tokens (input/output)
            cost_per_1m_input = 0.75
            cost_per_1m_output = 4.50
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
        extra_llm_success = {
            "provider": PROVIDER,
            "model": MODEL,
            "agent_id": context.agent_id,
            "latency_ms": latency_ms,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "estimated_cost": estimated_cost,
            "success": True,
        }
        if context.learning_phase:
            extra_llm_success["learning_phase"] = context.learning_phase
        log_event(
            level="info",
            event="llm_success",
            message=f"LLM request completed: {latency_ms}ms",
            request_id=context.request_id,
            user_id=str(context.user_id) if context.user_id else None,
            extra=extra_llm_success
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
        extra_llm_failure = {
            "provider": PROVIDER,
            "model": MODEL,
            "agent_id": context.agent_id,
            "latency_ms": latency_ms,
            "error_code": error_code,
            "error_message": error_message,
            "success": False,
        }
        if context.learning_phase:
            extra_llm_failure["learning_phase"] = context.learning_phase
        log_event(
            level="error",
            event="llm_failure",
            message=f"LLM request failed: {error_code} - {error_message}",
            request_id=context.request_id,
            user_id=str(context.user_id) if context.user_id else None,
            extra=extra_llm_failure
        )
        
        # Re-raise exception
        raise

