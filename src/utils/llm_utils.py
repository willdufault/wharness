import time

import openai

from src.models.session_state import SessionState

MAX_INVOKE_ATTEMPTS = 3
INVOKE_RETRY_DELAY_SECONDS = 10


def invoke_llm(state: SessionState, messages: list) -> str:
    print("\nThinking...\n")
    while True:
        for attempt_number in range(1, MAX_INVOKE_ATTEMPTS + 1):
            try:
                response = state.client.responses.create(model=state.model, input=messages)
                break
            except (openai.RateLimitError, openai.APIConnectionError) as invoke_error:
                if attempt_number == MAX_INVOKE_ATTEMPTS:
                    raise
                print(f"Model invoke failed ({type(invoke_error).__name__}), retrying in {INVOKE_RETRY_DELAY_SECONDS}s (attempt {attempt_number}/{MAX_INVOKE_ATTEMPTS})...")
                time.sleep(INVOKE_RETRY_DELAY_SECONDS)
        reply = response.output_text

        reply_start, tool_name, *rest = reply.split(maxsplit=2)
        if reply_start != "[TOOL]" or tool_name not in state.tools:
            return reply
        tool_args = rest[0] if rest else ""
        result = state.tools[tool_name].run(tool_args)
        print(f"Tool: {tool_name} {tool_args}")
        messages.append({"role": "assistant", "content": reply})
        messages.append(
            {
                "role": "user",
                "content": "[TOOL RESULT] The tool ran. If the task is done, answer the user in your own words; don't repeat raw output. Don't call a tool again with the same arguments.\n"
                + result,
            }
        )
