#!/bin/bash
# Start the LiteLLM gateway that LLVerifier's "codex" provider talks to.
# Chain: LLVerifier -> LiteLLM (127.0.0.1:4001) -> OpenCodex (127.0.0.1:10100) -> ChatGPT/Codex login.
set -euo pipefail
dir="$(cd "$(dirname "$0")/.." && pwd)"

if ! curl -fsS -m 3 http://127.0.0.1:10100/healthz >/dev/null 2>&1; then
  echo "OpenCodex is not reachable on 127.0.0.1:10100. Start it first: ocx start  (or: ocx service start)" >&2
  exit 1
fi

# Bind to loopback only; LiteLLM listens on 0.0.0.0 by default.
exec litellm --config "$dir/configs/litellm.yaml" --host 127.0.0.1 --port 4001
