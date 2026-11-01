# wharness

A toy LLM harness: a chat loop against OpenRouter.

## Run

```sh
uv run -m src.main
```

Requires `OPENROUTER_API_KEY` in `.env`. System prompt: `system_prompt.md` (`{{TOOLS}}` rendered at startup).

## Extensions (under `src/<type>/<name>`, discovered at startup)

- **Tools** — `src/tools/<name>.py`: `run()` with parameters = args. Description = module docstring, rendered into the system prompt. Model replies `[TOOL] <name> <args>` → executed, result fed back as `[TOOL RESULT]` until a final answer.
- **Commands** — `src/commands/<name>.py`: `run(state, args) -> str | None`, dispatched on `/name <args>` (args = one string, empty if absent). `state` is `SessionState` (`src/models/session_state.py`); commands may mutate it and make their own LLM calls via `invoke_llm(state, messages)` — the harness never invokes the LLM for a command. A returned string is printed.
- **Skills** — `src/skills/<name>.md`: plain text injected as a `[SKILL]` user message on `/name <args>` (plus `Arguments: <args>` when present); the model answers in the same turn.
