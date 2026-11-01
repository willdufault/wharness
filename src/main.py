import inspect
import os
from importlib import util as importlib_util
from pathlib import Path
from types import ModuleType

from dotenv import load_dotenv
from openai import OpenAI

from src.models.session_state import SessionState
from src.utils.llm_utils import invoke_llm

MODEL = "nvidia/nemotron-3.5-lightning:free"
BASE_URL = "https://openrouter.ai/api/v1"
EXIT_COMMANDS = ("exit", "quit", ":q")


def source_dir(name: str) -> Path:
    return Path(__file__).resolve().parent / name


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib_util.spec_from_file_location(name, path)
    module = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_tools() -> dict:
    tools = {}
    for tool_file in source_dir("tools").glob("*.py"):
        tool_name = tool_file.stem
        tools[tool_name] = load_module(tool_file, f"wharness_tool_{tool_name}")
    return tools


def load_commands() -> dict:
    commands = {}
    for command_file in source_dir("commands").glob("*.py"):
        command_name = command_file.stem
        commands[command_name] = load_module(command_file, f"wharness_command_{command_name}")
    return commands


def load_skills() -> dict:
    return {path.stem: path.read_text() for path in source_dir("skills").glob("*.md")}


def render_system_prompt(tools: dict) -> str:
    tool_list = []
    for tool_name, tool_module in sorted(tools.items()):
        params = ", ".join(
            param.name
            for param in inspect.signature(tool_module.run).parameters.values()
        )
        tool_list.append(
            f"- {tool_name}({params}): {inspect.getdoc(tool_module).splitlines()[0]}"
        )
    return (
        (Path(__file__).resolve().parent.parent / "system_prompt.md").read_text().replace("{{TOOLS}}", "\n".join(tool_list))
    )


def handle_command(user_input: str, state: SessionState, commands: dict, skills: dict):
    command_name, *command_args = user_input.lstrip("/").split(maxsplit=1)
    command_arg = command_args[0] if command_args else ""
    if command_name in commands:
        print(f"Command: {command_name}")
        output = commands[command_name].run(state, command_arg)
        if output:
            print(f"{output}\n")
    elif command_name in skills:
        skill_message = f"[SKILL] '{command_name}' skill — the text below is context for this and future turns:\n\n{skills[command_name]}"
        if command_arg:
            skill_message += f"\n\nArguments: {command_arg}"
        print(f"Skill: {command_name}")
        state.messages.append({"role": "user", "content": skill_message})
        reply = invoke_llm(state, state.messages)
        state.messages.append({"role": "assistant", "content": reply})
        print(f"Agent: {reply}\n")
    else:
        print(f"Unknown command: {command_name}\n")


def main():
    load_dotenv()
    client = OpenAI(base_url=BASE_URL, api_key=os.environ["OPENROUTER_API_KEY"])

    tools = load_tools()
    commands = load_commands()
    skills = load_skills()
    state = SessionState(model=MODEL, client=client, tools=tools, messages=[{"role": "system", "content": render_system_prompt(tools)}])

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip() in EXIT_COMMANDS:
            break

        if user_input.startswith("/"):
            handle_command(user_input, state, commands, skills)
        else:
            state.messages.append({"role": "user", "content": user_input})
            reply = invoke_llm(state, state.messages)
            state.messages.append({"role": "assistant", "content": reply})
            print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()
