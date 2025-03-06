from livekit.agents import llm
from typing import List, Optional, Dict, Any
import asyncio
from livekit.agents.llm import ChatMessage, ChatSession
import os
from llm_provider import LLMProvider

class UniversalRealtimeModel(llm.RealtimeModel):
    def __init__(
        self,
        instructions: str,
        voice: str = "default",
        temperature: float = 0.7,
        modalities: List[str] = ["text"],
        provider: str = "groq",  # Default to DeepSeek
        model_name: Optional[str] = None,
    ):
        super().__init__()
        self.instructions = instructions
        self.voice = voice
        self.temperature = temperature
        self.modalities = modalities
        
        # Initialize the provider
        self.llm_provider = LLMProvider(provider=provider)
        self.model_name = model_name or self.llm_provider.models["chat"]
        
        self.sessions = []
        
        # Create an initial session
        self._create_session()
    
    def _create_session(self):
        session = UniversalChatSession(
            self.llm_provider,
            self.model_name,
            self.instructions,
            self.temperature
        )
        self.sessions.append(session)
        return session
    
    async def process_text(self, text: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        # Find the appropriate session or create a new one
        session = self.sessions[0]  # For simplicity, using the first session
        
        # Add the user message to the conversation
        session.conversation.item.create(
            ChatMessage(role="user", content=text)
        )
        
        # Generate a response
        response = await session.generate_response()
        return response


class UniversalChatSession(ChatSession):
    def __init__(
        self,
        llm_provider: LLMProvider,
        model_name: str,
        instructions: str,
        temperature: float
    ):
        super().__init__()
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.system_prompt = instructions
        self.temperature = temperature
        self.conversation = llm.ChatConversation()
        self.response = llm.ChatResponse()
    
    async def generate_response(self):
        # Convert the conversation to the format expected by the provider
        messages = [{"role": "system", "content": self.system_prompt}]
        
        for msg in self.conversation.items:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Call the provider API
        try:
            completion = self.llm_provider.chat_completion(
                messages=messages,
                model=self.model_name,
                temperature=self.temperature
            )
            
            # Extract the response
            response_text = completion.choices[0].message.content
            
            # Update the response
            self.response.update(response_text)
            
            # Add the assistant's response to the conversation
            self.conversation.item.create(
                ChatMessage(role="assistant", content=response_text)
            )
            
            return {"text": response_text}
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return {"text": "I'm sorry, I encountered an error while processing your request."}