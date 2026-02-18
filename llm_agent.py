import os, json
from dataclasses import replace
from os import getenv

from dotenv import load_dotenv
from groq import Groq
from system_prompt import SYSTEM_PROMPT
from tool_schemas import TOOLS

load_dotenv()

LLM_MODEL = getenv("LLM_MODEL")
MAX_MEMORY = getenv("MAX_MEMORY")

groq_client = Groq(api_key=getenv("GROQ_API_KEY"))


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

async def process_user_message(user_input: str, mcp_client) -> str:
    messages.append({
        "role": "system",
        "content": user_input
    })

    response = groq_client.chat.completions.create(
        model = LLM_MODEL,
        messages = messages,
        tools = TOOLS,
        tool_choice= "auto"
    )

    msg = response.choices[0].message
    messages.append(msg)

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            try:
                result = await mcp_client.call_tool(tool_name, args)

                if result.is_error:
                    tool_output = f"Error: {result.content}"

                else:
                    tool_output = ""
                    for item in getattr(result, "content", []):
                        tool_output += getattr(item, "text", str(item))


            except Exception as e:
                tool_output = f"Error: {str(e)}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output
            })

        final_response = groq_client.chat.completions.create(
            model = LLM_MODEL,
            messages = messages,
        )

        final_msg = final_response.choices[0].message
        messages.append(final_msg)
        reply = final_msg.content

    else:
        reply = msg.content

    if len(messages) > MAX_MEMORY:
        messages[:] = [messages[0]] + messages[-MAX_MEMORY:]

    return reply