import asyncio
import os
import json
from typing import Any, List, Optional
from pathlib import Path

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from pydantic import Field

class OfflineStubChatModel(BaseChatModel):
    captured_calls: List[Any] = Field(default_factory=list)
    provider: str = "offline_stub"
    model: str = "offline_stub"

    @property
    def _llm_type(self) -> str:
        return "offline_stub"

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        raise NotImplementedError()

    async def _agenerate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        output_format = kwargs.get("output_format")
        
        # Serialize messages for offline inspection
        call_record = []
        for m in messages:
            msg_data = {"type": m.__class__.__name__}
            if isinstance(m.content, str):
                msg_data["content"] = m.content
            elif isinstance(m.content, list):
                # multi-modal content (text + images)
                parts = []
                for part in m.content:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            parts.append({"type": "text", "text": part.get("text")})
                        elif part.get("type") == "image_url":
                            # don't save entire massive base64 in log, record existence & length
                            url = part.get("image_url", {}).get("url", "")
                            parts.append({"type": "image_url", "url_length": len(url), "prefix": url[:30]})
                        else:
                            parts.append({"type": part.get("type")})
                    else:
                        parts.append(str(part))
                msg_data["content_parts"] = parts
            call_record.append(msg_data)

        self.captured_calls.append(call_record)

        # construct valid AgentOutput with "done" action
        action_dict = {"done": {"text": "Finished offline observation test"}}
        try:
            # instantiate the dynamic pydantic AgentOutput model
            completion = output_format(
                current_state={"evaluation_previous_goal": "Start", "memory": "test", "next_goal": "done"},
                action=[action_dict]
            )
        except Exception as e:
            try:
                completion = output_format(
                    next_goal="done",
                    action=[action_dict]
                )
            except Exception as e2:
                fields = output_format.model_fields
                data = {}
                if "next_goal" in fields: data["next_goal"] = "done"
                if "action" in fields: data["action"] = [action_dict]
                if "current_state" in fields:
                    data["current_state"] = {"evaluation_previous_goal": "Start", "memory": "", "next_goal": "done"}
                completion = output_format.model_validate(data)

        ai_msg = AIMessage(content="Offline stub action")
        ai_msg.completion = completion
        gen = ChatGeneration(message=ai_msg)
        gen.completion = completion
        res = ChatResult(generations=[gen])
        res.completion = completion
        return res

print("Stub model ready for integration test.")
