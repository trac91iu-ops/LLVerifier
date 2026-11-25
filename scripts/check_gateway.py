#!/usr/bin/env python3
"""Check that every LLVerifier strategy can reach its model through the gateway.

Sends one tiny request per distinct (provider, model) used in configs/config.yaml, or the file named by
LLVERIFIER_CONFIG, STRATEGIES, with the same sampling params LLVerifier sends (adjustLLMParams).
Usage:  [LLVERIFIER_CONFIG=config-opus.yaml] python scripts/check_gateway.py
"""
import os
import sys
import time

import yaml
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = yaml.safe_load(open(os.path.join(ROOT, "configs", os.environ.get("LLVERIFIER_CONFIG", "config.yaml"))))
providers, strategies = cfg["PROVIDERS"], cfg["STRATEGIES"]

pairs = sorted({tuple(s["provider"]) for s in strategies.values()})
failed = False
for prov_name, model in pairs:
    prov = providers.get(prov_name)
    if prov is None or model not in prov.get("models", []):
        print(f"[config] {prov_name}/{model}: not listed under PROVIDERS")
        failed = True
        continue
    client = OpenAI(base_url=prov["base_url"], api_key=prov["api_key"], timeout=300)
    t = time.time()
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a terse assistant."},
                {"role": "user", "content": "Reply with exactly: PONG"},
            ],
            temperature=0.1, top_p=0.1, max_tokens=32768,
            presence_penalty=0, frequency_penalty=0, n=1,
        )
        c = r.choices[0]
        tokens = r.usage.total_tokens if r.usage else None
        ok = c.finish_reason == "stop" and "PONG" in (c.message.content or "")
        failed |= not ok
        print(f"[{'ok' if ok else 'unexpected'}] {prov_name}/{model}: {c.message.content!r} "
              f"finish={c.finish_reason} tokens={tokens} {time.time() - t:.1f}s")
    except Exception as e:  # noqa: BLE001
        failed = True
        print(f"[error] {prov_name}/{model}: {type(e).__name__}: {e}")

sys.exit(1 if failed else 0)
