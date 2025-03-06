from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
# Remove OpenAI-specific imports
from dotenv import load_dotenv
import os
from api import AssistantFnc
from prompts import INSTRUCTIONS, WELCOME_MESSAGE
# Import the universal integration
from universal_integration import UniversalRealtimeModel


load_dotenv()


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    # Use the universal model with DeepSeek as the provider
    model = UniversalRealtimeModel(
        instructions=INSTRUCTIONS,
        temperature=0.8,
        modalities=["text"],  # Note: Audio may require a separate TTS service
        provider="deepseek"  # You can easily switch to "groq", "ollama", etc.
    )

    assistant_fnc = AssistantFnc()
    
    assistant = MultimodalAgent(model=model, fnc_ctx=assistant_fnc)
    
    assistant.start(ctx.room)

    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content=WELCOME_MESSAGE
        )
    )
    session.response.create()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))