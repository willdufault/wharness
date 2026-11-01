# TODO.md

- [ ] add core tools (pi: read, write, edit, bash)
- [ ] improve base system prompt
- [ ] use rich print? wait for tui overhaul?
- [ ] audit state obj usage + values; pass indiv params to fcns instead?
---
- [.] add model toggle (/model: commands/model.py, run(state, args), session-only slug)
- [.] add centralized command interface (run(state, args) contract, invoke+retries in src/utils/llm_utils.py)
- [.] create common state passed around (src/models/session_state.py dataclass, data-only record)
- [ ] remove unnecessary docstrings, make comments concise, debloat code
---
- [x] migrate to responses api
- [x] add try/catch for rate limit/conn error
- [x] dynamic tool discovery?
- [x] update tool layout to match skill
- [x] add demo skill (/compact: skills/<name>/SKILL.md + skill.py run() hook)
- [x] migrate skills to commands (/compact: commands/compact.py, module docstring + run() hook)
- [x] flatten tool layout (tools/read/tool.py → tools/read.py)
