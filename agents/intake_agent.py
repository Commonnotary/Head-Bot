"""
Intake Agent — Customer Triage & Information Gathering

Responsible for:
- Greeting customers warmly and professionally
- Identifying what the customer needs
- Collecting key details: document type, destination country, urgency, quantity
- Flagging incomplete information back to the Head Bot
"""

import anthropic
from config.settings import AGENT_MODEL, COMPANY_NAME

INTAKE_SYSTEM_PROMPT = f"""You are the Intake Specialist for {COMPANY_NAME}, a professional apostille and document
authentication company. Your role is to warmly greet customers, understand their needs quickly,
and gather the essential details needed to assist them.

Always maintain a friendly, professional, and reassuring tone. Customers are often stressed about
their important documents — your job is to make them feel confident and taken care of.

When gathering information, aim to identify:
1. What document(s) the customer needs apostilled or authenticated
2. What country the documents will be used in (destination country)
3. How urgently they need the service
4. How many documents they have
5. Whether they already have certified copies or originals

Do NOT ask all questions at once. Use natural, conversational language. One or two questions at a time.
If the customer has already provided information, acknowledge it and only ask for what is missing.

Format your response as a professional customer service representative would — helpful, concise,
empathetic, and solution-oriented.
"""


_CACHED_SYSTEM = [{"type": "text", "text": INTAKE_SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]


def run_intake(conversation_history: list[dict], client: anthropic.Anthropic) -> str:
    """
    Run the intake agent with the current conversation history.
    Returns the agent's response as a string.
    """
    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        system=_CACHED_SYSTEM,
        messages=conversation_history,
    )
    return response.content[0].text


def extract_intake_summary(conversation_history: list[dict], client: anthropic.Anthropic) -> str:
    """
    Analyze the conversation so far and extract a structured summary
    of what the customer needs — used by the Head Bot for routing.
    """
    extraction_prompt = """Review the conversation and extract a JSON summary with these fields:
{
  "document_types": ["list of documents mentioned"],
  "destination_country": "country name or null",
  "urgency": "standard|expedited|rush|same_day|unknown",
  "quantity": number or null,
  "has_certified_copies": true/false/null,
  "needs_notarization": true/false/null,
  "additional_notes": "anything else relevant"
}

Only return the JSON object, nothing else."""

    messages = conversation_history + [{"role": "user", "content": extraction_prompt}]

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=512,
        system=[{"type": "text", "text": "You are a data extraction assistant. Extract structured information from conversations accurately.", "cache_control": {"type": "ephemeral"}}],
        messages=messages,
    )
    return response.content[0].text
