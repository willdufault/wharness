from src.models.session_state import SessionState


def run(state: SessionState, args: str) -> str:
    if not args:
        return f"Current model: {state.model}"
    state.model = args
    return f"Model set to: {state.model}"
