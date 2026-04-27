"""
Beer-delivery agent: a manual agentic loop on top of the OpenAI/OpenRouter chat completions API with native tool calling.

Starting state for the lab: one tool (`list_clients`) and a minimal prompt.
You will add more tools in Task 3 and refine the prompt in Task 4.
"""
import json

from openai import OpenAI

from api_key import load_key
from db import get_customers
from utils import tool_schema, pretty_print_message, pretty_print_response


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=load_key(),
)


# ---- Tool definitions -------------------------------------------------------

# This is the agent's 1st tool (already implemented for you).
def list_clients() -> str:
    """Return a tabulated list of all clients."""
    return get_customers()


# This is how we register tools. You will add more tools here in Task 3.
TOOL_MAPPING = {
    "list_clients": list_clients,
}
# Generate the tool schema for all registered tools
tools = [tool_schema(fn) for fn in TOOL_MAPPING.values()]


# You will refine this prompt in Task 4.
PROMPT = "You are a helpful assistant."


# ---- Agent loop -------------------------------------------------------------

MAX_TOOL_CALL_ITERATIONS = 10


def call_llm(messages: list[dict]) -> dict:
    """Send the conversation to the model and return the assistant message as a dict."""
    print(f"[llm] sending {len(messages)} messages to the llm")
    for i, message in enumerate(messages):
        print(f"[llm] message {i}: {pretty_print_message(message)}")

    response = client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        tools=tools,  # <----- This is how we pass the tool's definitions (schemas) to the model.
        messages=messages,
    )
    assistant_msg = response.choices[0].message.model_dump(exclude_none=True)
    print(f"[llm] response: {pretty_print_response(assistant_msg)}\n")
    return assistant_msg


def run_tool(tool_call: dict) -> dict:
    """Execute one tool call and return the matching `tool` message."""
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    print(f"[tool] {name}({args})")

    result = TOOL_MAPPING[name](**args)  # <----- This is how we call the tool function.
    
    print(f"[tool] --> {result}")
    return {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": str(result),
    }


def agent_loop() -> None:
    """The main agent loop."""
    messages: list[dict] = [{"role": "system", "content": PROMPT}]  # <----- This is how we set the system prompt.  
    print("Chat with the delivery agent (Ctrl-D to quit)")

    while True:
        user_input = input("\nYou: ").strip()  # <----- This is how we get the user's input.
        messages.append({"role": "user", "content": user_input})

        for _ in range(MAX_TOOL_CALL_ITERATIONS):
            print("\nCALL_LLM " + "-" * 50)
            llm_response = call_llm(messages)  # <----- This is how we call the LLM.
            messages.append(llm_response)

            print("\nTOOL_CALLS " + "-" * 50)
            tool_calls = llm_response.get("tool_calls")  # <--------- This is how we get the tool calls from the LLM response.
            if not tool_calls:
                if llm_response.get("content"):
                    print(f"\nAssistant: {llm_response['content']}")
                break

            for tc in tool_calls:
                messages.append(run_tool(tc))
        else:
            print(f"[warn] reached max iterations ({MAX_TOOL_CALL_ITERATIONS})")


if __name__ == "__main__":
    agent_loop()
