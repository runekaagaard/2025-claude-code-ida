# Claude Code in Practice

A presentation about using Claude Code on large projects - building features fast without losing control.

**View the presentation:** [https://runekaagaard.github.io/claude-code/](https://runekaagaard.github.io/claude-code/)

## Topics Covered

- **MCP Servers**: Your tools become Claude's tools
- **Worktrees & Workflows**: Parallel development strategies
- **Root to Leaves**: Foundation first, details last
- **Documentation**: CLAUDE.md, LLM docs, and cross-cutting concerns
- **Planning & Exploration**: Research before coding
- **Building in Stages**: Root → Leaves workflow
- **Quality & Results**: Making it work on real projects

## About

Created by Rune Kaagaard (CTO, Prescriba) for the Copenhagen Python meetup.

Topics include practical workflows, MCP server development, documentation strategies, and real-world patterns for using Claude Code effectively on large codebases.

## Running Locally

```bash
# Install dependencies
make install

# Build and serve
make build
make serve
```

Server runs at: http://localhost:8000

## Source

Built with org-mode → HTML pipeline. Source in `thetalk.org`.
