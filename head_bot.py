"""
CNA Head-Bot — Decision Engine
The master brain for Common Notary Apostille LLC.
Reads the rules + playbook, takes an inquiry, returns a decision.
It NEVER sends anything — it only decides and stages.
"""

import os
import json
import anthropic


def load_brain():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "routing-rules.json"), "r") as f:
        rules = f.read()
    with open(os.path.join(here, "bot-prompts.md"), "r") as f:
        playbook = f.read()
    return rules, playbook


def decide(inquiry: dict) -> dict:
    rules, playbook = load_brain()
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

    system_prompt = f"""You are the CNA Head-Bot, the master brain for Common
Notary Apostille LLC. You direct five sub-bots: Intake, Qualifier, Price,
Confirm, Dispatch.

YOUR RULES (routing-rules.json):
{rules}

YOUR PLAYBOOK (bot-prompts.md):
{playbook}

NON-NEGOTIABLE:
- You NEVER send an email or place a call. You only decide and stage.
- Never include notary commission numbers anywhere.
- Never mention AI in anything client-facing.

For the inquiry given, respond with ONLY a JSON object (no markdown, no
preamble) in exactly this shape:
{{
  "route_to": "<which sub-bot handles this next>",
  "quoted_price": <number>,
  "escalate_to_byron": <true or false>,
  "escalation_reason": "<short reason, or empty string>",
  "next_action": "<one clear sentence on what gets staged>"
}}"""

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"New inquiry:\n{json.dumps(inquiry, indent=2)}"}
        ],
    )

    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Could not parse decision", "raw": raw}


if __name__ == "__main__":
    test_inquiry = {
        "name": "Jane Smith",
        "client_type": "standard",
        "region": "DMV",
        "service": "apostille",
        "document_type": "Power of Attorney",
        "urgency": "rush",
    }

    print("Head-Bot is thinking about this inquiry:")
    print(json.dumps(test_inquiry, indent=2))
    print("-" * 50)

    decision = decide(test_inquiry)

    print("Head-Bot decision:")
    print(json.dumps(decision, indent=2))
