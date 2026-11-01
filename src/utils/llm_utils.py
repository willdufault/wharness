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

        reply_start, tool_name, *tool_args = reply.split()
        if reply_start != "[TOOL]" or tool_name not in state.tools:
            return reply
        result = state.tools[tool_name].run(" ".join(tool_args))
        print(f"Tool: {tool_name} {' '.join(tool_args)}")
        messages.append(
            {
                "role": "user",
                "content": "[TOOL RESULT] Use this to answer in your own words — don't repeat it verbatim. All results you need are here; don't call this tool again with the same arguments. Answer now:\n"
                + result,
            }
        )
