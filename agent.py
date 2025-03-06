from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from groq_integration import GroqRealtimeModel
from dotenv import load_dotenv
import os
from livekit.plugins.openai import stt
from api import AssistantFnc
from prompts import INSTRUCTIONS, WELCOME_MESSAGE


load_dotenv()


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    # model = openai.realtime.RealtimeModel(
    #     instructions=INSTRUCTIONS,
    #     voice="coral",
    #     temperature=0.8,
    #     modalities=["audio", "text"]
    # )

    model = GroqRealtimeModel(
        instructions=INSTRUCTIONS,
        voice="default",  # Adjust based on available voices in your TTS implementation
        temperature=0.8,
        modalities=["audio", "text"]
    )

    assistant_fnc = AssistantFnc()
    
    assistant = MultimodalAgent(model=model,fnc_ctx=assistant_fnc)
    
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

    