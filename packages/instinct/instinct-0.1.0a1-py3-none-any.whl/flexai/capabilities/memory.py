import json
import os
from dataclasses import dataclass, field
from typing import List, Dict
from pydantic import BaseModel

from flexai.capability import Capability
from flexai.message import Message, UserMessage, AIMessage
from flexai.llm.anthropic_client import AnthropicClient

class Memory(BaseModel):
    content: str
    context: str

@dataclass(frozen=True)
class ConversationMemory(Capability):
    """A capability that learns from conversations and provides relevant context using LLM."""

    memories_dir: str
    llm_client: AnthropicClient = AnthropicClient()
    max_memories: int = 1000
    memories: List[Memory] = field(default_factory=list)

    def __post_init__(self):
        os.makedirs(self.memories_dir, exist_ok=True)
        self._load_memories()

    def _load_memories(self):
        memory_file = os.path.join(self.memories_dir, "memories.json")
        if os.path.exists(memory_file):
            with open(memory_file, "r") as f:
                loaded_memories = json.load(f)
                object.__setattr__(self, "memories", [Memory(**m) for m in loaded_memories])

    def _save_memories(self):
        memory_file = os.path.join(self.memories_dir, "memories.json")
        with open(memory_file, "w") as f:
            json.dump([m.dict() for m in self.memories], f)

    async def modify_prompt(self, prompt: str, messages: List[Message]) -> List[Message]:
        """Add relevant memories to the conversation context."""
        relevant_memories = await self._find_relevant_memories(messages)
        if relevant_memories:
            context_message = "Relevant past information:\n" + "\n".join(relevant_memories)
            prompt += "\n" + context_message
        return prompt

    async def modify_response(self, messages: List[Message], response: AIMessage) -> AIMessage:
        """Learn from the conversation by saving relevant information."""
        await self._update_memories(messages + [response])
        return response

    async def _find_relevant_memories(self, messages: List[Message]) -> List[str]:
        query = " ".join([m.content for m in messages[-3:]])  # Use last 3 messages as context
        
        class RelevantMemories(BaseModel):
            memories: List[str]

        prompt = f"""Given the following conversation context and a list of memories, 
        select up to 3 most relevant memories that could provide useful context for the conversation.
        
        Conversation context: {query}
        
        Memories:
        {json.dumps([m.dict() for m in self.memories])}
        
        Return only the content of the relevant memories, not their context."""

        result = await self.llm_client.get_structured_response(
            messages=[UserMessage(content=prompt)],
            model=RelevantMemories
        )
        
        return result[0].memories if result else []

    async def _update_memories(self, messages: List[Message]):
        conversation = " ".join([m.content for m in messages])
        
        class NewMemories(BaseModel):
            memories: List[Memory]

        prompt = f"""Given the following conversation, extract key information that should be remembered for future context.
        Create new memory entries with the extracted information and provide a brief context for each memory.
        
        Conversation:
        {conversation}
        
        Return a list of new memories, each containing 'content' (the key information) and 'context' (a brief explanation of why this information is important)."""

        result = await self.llm_client.get_structured_response(
            messages=[UserMessage(content=prompt)],
            model=NewMemories
        )
        
        if result:
            new_memories = result[0].memories
            self.memories.extend(new_memories)
            
            if len(self.memories) > self.max_memories:
                self.memories = self.memories[-self.max_memories:]
            
            self._save_memories()