"""
Groq LLM Backend for browser-use Agent
Part of: "The DOM Serialization Gap" Research Infrastructure

Integrates Groq's API with browser-use BaseChatModel protocol:
- Official Groq SDK (AsyncGroq / Groq) with OpenAI-compatible wire format.
- Structured JSON output parsing for AgentOutput Pydantic schema.
- Exact token usage extraction (prompt_tokens, completion_tokens, total_tokens).
- Strict secret redaction (never logs or leaks GROQ_API_KEY).
- Fail-closed error classification (Auth, RateLimit, ModelAccess, Connection).
"""

import os
import re
import json
import logging
from typing import Any, TypeVar, Type, Optional, List
from pydantic import BaseModel

import groq
from groq import AsyncGroq, Groq
from groq import (
    AuthenticationError as GroqAuthError,
    RateLimitError as GroqRateLimitError,
    BadRequestError as GroqBadRequestError,
    NotFoundError as GroqNotFoundError,
    APIConnectionError as GroqConnectionError,
    APIStatusError as GroqStatusError,
)

from browser_use.llm.base import BaseChatModel, ChatInvokeCompletion
from browser_use.llm.messages import BaseMessage, UserMessage, SystemMessage, AssistantMessage
from browser_use.llm.views import ChatInvokeUsage
from browser_use.llm.openai.serializer import OpenAIMessageSerializer
from browser_use.llm.exceptions import (
    ModelRateLimitError,
    ModelProviderError,
    ModelOutputTruncatedError,
)

logger = logging.getLogger("groq_backend")

T = TypeVar("T", bound=BaseModel)

def sanitize_secret_text(text: str) -> str:
    """Ensure no Groq API key is present in output text or error messages."""
    if not text:
        return ""
    # Redact explicit env key if present
    env_key = os.environ.get("GROQ_API_KEY", "")
    if env_key and env_key in text:
        text = text.replace(env_key, "[REDACTED_GROQ_API_KEY]")
    # Redact standard Groq key pattern (gsk_...)
    text = re.sub(r"gsk_[A-Za-z0-9_]{20,}", "[REDACTED_GROQ_API_KEY]", text)
    return text

sanitize_secret_leakage = sanitize_secret_text

def get_groq_api_key() -> str:
    """Retrieve Groq API key from environment, Windows user registry, or gitignored key file, failing closed if missing."""
    import sys
    from pathlib import Path
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as reg_key:
                val, _ = winreg.QueryValueEx(reg_key, "GROQ_API_KEY")
                if val:
                    key = str(val).strip()
                    os.environ["GROQ_API_KEY"] = key
        except Exception:
            pass
    if not key:
        candidate_paths = [
            Path(__file__).resolve().parent / "groq_key.txt",
            Path(__file__).resolve().parent / ".env",
            Path.cwd() / "groq_key.txt",
            Path.cwd() / ".env",
        ]
        for p in candidate_paths:
            if p.exists():
                try:
                    for line in p.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if line.startswith("GROQ_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
                        elif line.startswith("gsk_"):
                            key = line
                            break
                    if key and not key.startswith("PASTE_"):
                        os.environ["GROQ_API_KEY"] = key
                        break
                    else:
                        key = ""
                except Exception:
                    pass
    return key

class ChatGroq(BaseChatModel):
    """
    Groq chat model implementation adhering to browser_use.llm.base.BaseChatModel protocol.
    Provides structured action outputs required by browser-use Agent.
    """
    _verified_api_keys: bool = False

    def __init__(
        self,
        model: str = "openai/gpt-oss-120b",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        max_completion_tokens: int = 1024,
        top_p: Optional[float] = None,
        timeout: float = 60.0,
        client: Optional[AsyncGroq] = None,
        max_tokens_ceiling: int = 7500,
    ):
        self.model = model
        self.api_key = api_key if api_key is not None else get_groq_api_key()
        if not self.api_key and client is None:
            raise ValueError(
                "Groq API key must be provided or configured via GROQ_API_KEY environment variable.\n"
                "In PowerShell, configure it safely via:\n"
                '  $env:GROQ_API_KEY = Read-Host "Paste your Groq API key"'
            )
        self.temperature = temperature
        self.max_completion_tokens = max_completion_tokens
        self.top_p = top_p
        self.timeout = timeout
        self.max_tokens_ceiling = max_tokens_ceiling
        
        self._async_client = client or (AsyncGroq(api_key=self.api_key, timeout=self.timeout) if self.api_key else None)
        self._sync_client: Optional[Groq] = None

    @property
    def _client(self) -> Optional[AsyncGroq]:
        return self._async_client

    @_client.setter
    def _client(self, val: Optional[AsyncGroq]):
        self._async_client = val

    @property
    def provider(self) -> str:
        return "groq"

    @property
    def name(self) -> str:
        return f"groq/{self.model}"

    @property
    def model_name(self) -> str:
        return self.model

    def get_client(self) -> AsyncGroq:
        if self._async_client is None:
            if not self.api_key:
                raise RuntimeError(
                    "[ERROR] GROQ_API_KEY is not configured.\n"
                    "In PowerShell, configure it safely via:\n"
                    '  $env:GROQ_API_KEY = Read-Host "Paste your Groq API key"'
                )
            self._async_client = AsyncGroq(api_key=self.api_key, timeout=self.timeout)
        return self._async_client

    def _extract_usage(self, response: Any) -> ChatInvokeUsage:
        """Extract prompt and completion tokens from Groq API response."""
        p_tokens = 0
        c_tokens = 0
        t_tokens = 0
        if hasattr(response, "usage") and response.usage:
            p_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
            c_tokens = getattr(response.usage, "completion_tokens", 0) or 0
            t_tokens = getattr(response.usage, "total_tokens", 0) or (p_tokens + c_tokens)
        return ChatInvokeUsage(
            prompt_tokens=p_tokens,
            prompt_cached_tokens=None,
            prompt_cache_creation_tokens=None,
            prompt_image_tokens=None,
            completion_tokens=c_tokens,
            total_tokens=t_tokens,
        )

    def _clean_json_content(self, raw_content: str) -> str:
        """Strip markdown code blocks if the model wrapped the JSON response."""
        content = raw_content.strip()
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()
        return content

    def _check_payload_size(self, serialized_messages: List[dict]):
        """Ensure estimated prompt + max_completion_tokens does not breach TPM limit (8,000 for gpt-oss-120b)."""
        prompt_chars = sum(
            len(m.get("content", "")) if isinstance(m.get("content", ""), str) else len(json.dumps(m.get("content", "")))
            for m in serialized_messages
        )
        estimated_prompt_tokens = (prompt_chars // 4) + (len(serialized_messages) * 10)
        total_estimated_demand = estimated_prompt_tokens + self.max_completion_tokens
        if self.max_tokens_ceiling and total_estimated_demand > self.max_tokens_ceiling:
            raise ModelProviderError(
                message=(
                    f"Pre-dispatch payload size blocked: estimated {total_estimated_demand} tokens "
                    f"(prompt: ~{estimated_prompt_tokens}, max_out: {self.max_completion_tokens}) "
                    f"exceeds safe ceiling of {self.max_tokens_ceiling} tokens (Groq TPM limit is 8000). "
                    f"Failing closed before network dispatch."
                ),
                status_code=413,
                model=self.name,
            )

    async def ainvoke(
        self,
        messages: List[Any],
        output_format: Optional[Type[T]] = None,
        **kwargs: Any
    ) -> ChatInvokeCompletion[Any]:
        """
        Execute an asynchronous chat completion request against Groq.
        Supports structured JSON parsing for output_format Pydantic models.
        """
        client = self.get_client()
        clean_msgs = []
        for m in messages:
            if isinstance(m, BaseMessage):
                clean_msgs.append(m)
            elif isinstance(m, str):
                clean_msgs.append(UserMessage(content=m))
            elif isinstance(m, dict):
                role = m.get("role", "user")
                content = m.get("content", "")
                if role == "system":
                    clean_msgs.append(SystemMessage(content=content))
                elif role == "assistant":
                    clean_msgs.append(AssistantMessage(content=content))
                else:
                    clean_msgs.append(UserMessage(content=content))
            else:
                content = getattr(m, "content", str(m))
                clean_msgs.append(UserMessage(content=str(content)))
        serialized_messages = OpenAIMessageSerializer.serialize_messages(clean_msgs)

        model_params: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_completion_tokens,
        }
        if self.top_p is not None:
            model_params["top_p"] = self.top_p

        try:
            if output_format is None:
                self._check_payload_size(serialized_messages)
                # Plain unstructured text completion
                response = await client.chat.completions.create(
                    messages=serialized_messages,
                    **model_params,
                )
                choice = response.choices[0] if response.choices else None
                if not choice or not choice.message:
                    raise ModelProviderError(
                        message=f"Groq API returned empty choices for model '{self.model}'.",
                        status_code=502,
                        model=self.name,
                    )
                content = choice.message.content or ""
                stop_reason = str(choice.finish_reason) if getattr(choice, "finish_reason", None) is not None else "stop"
                return ChatInvokeCompletion(
                    completion=content,
                    usage=self._extract_usage(response),
                    stop_reason=stop_reason,
                )
            else:
                # Structured output request
                schema = output_format.model_json_schema()
                schema_json = json.dumps(schema, indent=2)

                # Inject JSON instructions into system prompt or append as system message
                schema_instruction = (
                    "\n\n[MANDATORY OUTPUT FORMAT]\n"
                    "You must output your complete response strictly as a single valid JSON object adhering to this schema:\n"
                    f"{schema_json}\n"
                    "Do NOT wrap with markdown fences. Output raw valid JSON ONLY."
                )

                has_system = False
                for msg in serialized_messages:
                    if msg.get("role") == "system":
                        msg["content"] = str(msg.get("content", "")) + schema_instruction
                        has_system = True
                        break
                if not has_system:
                    serialized_messages.insert(0, {"role": "system", "content": schema_instruction.strip()})

                # Groq natively supports response_format={"type": "json_object"}
                model_params["response_format"] = {"type": "json_object"}

                self._check_payload_size(serialized_messages)
                response = await client.chat.completions.create(
                    messages=serialized_messages,
                    **model_params,
                )
                choice = response.choices[0] if response.choices else None
                if not choice or not choice.message:
                    raise ModelProviderError(
                        message=f"Groq API returned empty choices for structured output on '{self.model}'.",
                        status_code=502,
                        model=self.name,
                    )

                if choice.finish_reason == "length":
                    raise ModelOutputTruncatedError(
                        message=f"Groq response was truncated by max_tokens ({self.max_completion_tokens}).",
                        model=self.name,
                    )

                raw_content = choice.message.content or ""
                clean_content = self._clean_json_content(raw_content)

                try:
                    parsed = output_format.model_validate_json(clean_content)
                except Exception as parse_err:
                    raise ModelProviderError(
                        message=f"Failed to validate Groq JSON response against {output_format.__name__}: {sanitize_secret_text(str(parse_err))}\nRaw: {raw_content[:300]}",
                        status_code=500,
                        model=self.name,
                    )

                stop_reason = str(choice.finish_reason) if getattr(choice, "finish_reason", None) is not None else "stop"
                return ChatInvokeCompletion(
                    completion=parsed,
                    usage=self._extract_usage(response),
                    stop_reason=stop_reason,
                )

        except GroqAuthError as e:
            raise ModelProviderError(
                message=f"Groq Authentication failed (HTTP 401). Verify GROQ_API_KEY: {sanitize_secret_text(str(e))}",
                status_code=401,
                model=self.name,
            ) from e

        except GroqRateLimitError as e:
            raise ModelRateLimitError(
                message=f"Groq rate limit or quota exceeded (HTTP 429): {sanitize_secret_text(str(e))}",
                model=self.name,
            ) from e

        except (GroqBadRequestError, GroqNotFoundError) as e:
            raise ModelProviderError(
                message=f"Groq model error for '{self.model}': {sanitize_secret_text(str(e))}",
                status_code=getattr(e, "status_code", 400),
                model=self.name,
            ) from e

        except GroqConnectionError as e:
            raise ModelProviderError(
                message=f"Groq network connection failed: {sanitize_secret_text(str(e))}",
                status_code=503,
                model=self.name,
            ) from e

        except GroqStatusError as e:
            raise ModelProviderError(
                message=f"Groq API returned HTTP {e.status_code}: {sanitize_secret_text(str(e))}",
                status_code=e.status_code,
                model=self.name,
            ) from e

        except (ModelProviderError, ModelRateLimitError, ModelOutputTruncatedError):
            raise

        except Exception as e:
            raise ModelProviderError(
                message=f"Groq request unexpected error: {sanitize_secret_text(str(e))}",
                status_code=500,
                model=self.name,
            ) from e

    def invoke(self, messages: List[Any], **kwargs: Any) -> Any:
        """Synchronous invocation fallback using asyncio event loop."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.ainvoke(messages, **kwargs))
