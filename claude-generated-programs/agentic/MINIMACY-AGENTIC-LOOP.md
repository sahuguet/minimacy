# Minimacy Agentic Loop

A bare-metal agentic loop built on Minimacy: no OS, no shell, no hidden complexity.

---

## Core Idea

Minimacy already has everything needed for the skeleton of an agentic loop:
- **HTTP client** (`core.net.http.cli`) — call Claude API
- **JSON** (`core.util.json`) — parse tool_use blocks, encode results
- **Concurrency** (`await`, threads) — handle async LLM responses
- **File I/O** — persist state, read/write local data

The loop itself is straightforward:
1. Send messages + tool schemas to Claude API
2. Receive response: either a final answer or a `tool_use` block
3. Dispatch the tool call (locally or remotely)
4. Append result to message history
5. Repeat until done

---

## Why Bare Metal Is Interesting

| Property | Bare-metal Minimacy agent | OS-based agent (Python, Node…) |
|---|---|---|
| Attack surface | Minimal (no OS, no shell) | Large |
| Boot time | Near-instant | Seconds |
| Memory footprint | Minimal | Heavy runtime |
| Determinism | High | OS scheduler interferes |
| Auditability | Every tool is explicit Minimacy code | Hidden syscalls, shell escapes |

The key security property: the agent **can only do what Minimacy exposes**. No `exec`, no shell escape, no surprises.

---

## Tool Architecture: Two Tiers

### Tier 1 — Native Minimacy tools (local, lightweight)

Implemented directly as Minimacy functions and dispatched in-process:

| Tool | Notes |
|---|---|
| `read_file` / `write_file` | Native file I/O |
| `http_fetch` | Raw HTTP via `core.net.http.cli` |
| `get_time` | System clock |
| `store_memory` / `recall` | In-memory map or persisted file |
| `log` | `echoLn` to stdout |

### Tier 2 — Remote MCP servers (cloud-hosted, heavy)

Local MCPs (stdio-based) are impossible on bare metal — no OS, no process spawning.
**Remote MCPs (HTTP-based) are a natural fit.** They are just HTTP endpoints, and Minimacy already has an HTTP client.

Examples of remote tools delegated to cloud MCP servers:
- Web search (Brave, Tavily)
- Code execution (E2B, etc.)
- Database queries
- Email / calendar
- Vector search / knowledge base

---

## Dispatcher Architecture

```
[Minimacy bare-metal agent]
         │
         ▼  Claude API (messages + tool schemas)
    [Claude LLM]
         │  returns tool_use blocks
         ▼
    [Minimacy dispatcher]
       /               \
  native tools      HTTP calls
  (file, memory,    to cloud-hosted
   log, fetch)      MCP servers
```

The agent is a thin, secure orchestrator. All heavy lifting lives in the cloud.

---

## Self-Configuring via MCP Discovery

MCP servers expose a `tools/list` endpoint. At startup, the agent can:
1. Query configured MCP server(s) for their tool schemas
2. Pass those schemas to Claude in the API call
3. Route incoming `tool_use` blocks to the appropriate MCP server

This makes the agent **self-configuring**: boot it, it discovers available tools, and operates without hardcoded schemas.

---

## Use Cases

- **Smart appliance**: boots into an agent that reads local sensors, queries the web, writes local state — all orchestrated by a cloud LLM
- **Bootable AI assistant**: USB stick that boots into a Claude-powered agent on any x86 machine
- **Secure audit agent**: bare metal = provably constrained tool set, no shell escape possible
- **Edge orchestrator**: minimal footprint at the network edge, delegates compute-heavy work to cloud MCPs
- **Educational reference**: the cleanest possible implementation of an agentic loop — no framework magic, every step explicit

---

## Implementation Plan

### Phase 1 — Minimal loop
- [ ] `agent.mcy`: message history management, single call to Claude API with tool schemas
- [ ] Dispatcher: `match` on tool name, call corresponding Minimacy function
- [ ] Native tools: `log`, `read_file`, `write_file`, `http_fetch`
- [ ] Loop until Claude returns a non-tool response

### Phase 2 — Remote MCP support
- [ ] MCP HTTP client: implement `tools/list` and `tools/call` over HTTP
- [ ] Dynamic schema loading at startup
- [ ] Route unknown tool names to configured MCP server(s)

### Phase 3 — Hardening
- [ ] Timeout handling for all HTTP calls (LLM + MCP)
- [ ] Error propagation back to Claude (tool result with `is_error: true`)
- [ ] Max iterations / cost guard
- [ ] Persistent memory across runs (file-backed)

---

## Key Design Decisions (TBD)

1. **Tool schema source**: hardcoded vs. fetched from MCP at startup?
2. **MCP server config**: passed as CLI flags (`--mcp-url`, `--mcp-key`) or a local config file?
3. **Message history**: in-memory only, or persisted to file for multi-session continuity?
4. **Human-in-the-loop**: use `onPrompt` to allow interruption, or fully autonomous?
