from src.models.session_state import SessionState
from src.utils.llm_utils import invoke_llm


def run(state: SessionState, args: str) -> str:
    instructions = "Summarize the conversation so far in a compact handoff: goal, decisions, key facts, files changed, next steps. Output only the summary."
    summary = invoke_llm(state, state.messages + [{"role": "user", "content": instructions}])
    state.messages = [state.messages[0], {"role": "user", "content": f"Summary of the previous session:\n{summary}"}]
    return summary
