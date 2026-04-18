"""
Apostille Expert Agent — Process & Requirements Knowledge

Responsible for:
- Answering questions about the apostille process
- Explaining the difference between apostille and embassy legalization
- Providing country-specific guidance
- Clarifying what documents are required and in what format
- Handling complex or unusual apostille scenarios
"""

import anthropic
from config.settings import AGENT_MODEL, COMPANY_NAME
from knowledge.apostille_info import (
    WHAT_IS_AN_APOSTILLE,
    APOSTILLE_VS_AUTHENTICATION,
    APOSTILLE_PROCESS,
    DOCUMENT_TYPES,
    COMMON_MISTAKES,
    FAQ,
    SERVICE_TIMELINE,
)
from knowledge.country_requirements import check_hague_membership

EXPERT_SYSTEM_PROMPT = f"""You are the Apostille Expert at {COMPANY_NAME}. You have deep knowledge of
the apostille process, the Hague Convention, embassy legalization, and document authentication
requirements for countries worldwide.

Your role is to:
- Explain the apostille/legalization process clearly and accurately
- Help customers understand exactly what they need based on their document type and destination country
- Proactively warn about common mistakes (e.g., wrong state, photocopy vs. certified copy)
- Provide country-specific guidance (Hague members vs. non-Hague members)
- Answer technical questions about the apostille process

KNOWLEDGE BASE:
{WHAT_IS_AN_APOSTILLE}

{APOSTILLE_VS_AUTHENTICATION}

{APOSTILLE_PROCESS}

COMMON MISTAKES TO WARN ABOUT:
{chr(10).join(f'- {m}' for m in COMMON_MISTAKES)}

FREQUENTLY ASKED QUESTIONS:
{chr(10).join(f'Q: {k}{chr(10)}A: {v}{chr(10)}' for k, v in FAQ.items())}

SERVICE TIMELINES:
{chr(10).join(f"- {v['name']}: {v['turnaround']}" for v in SERVICE_TIMELINE.values())}

Guidelines:
- Use plain, accessible language — avoid overly technical jargon
- Be precise and accurate — document authentication mistakes are costly for customers
- If you're unsure about a very specific edge case, recommend the customer call us directly
- Always position {COMPANY_NAME} as the reliable expert who will handle everything for them
"""


_CACHED_EXPERT_SYSTEM = [{"type": "text", "text": EXPERT_SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]


def answer_apostille_question(
    question: str,
    context: dict,
    client: anthropic.Anthropic,
) -> str:
    """
    Answer a specific apostille-related question with country context if available.

    Args:
        question: The customer's question
        context: Dict with keys like destination_country, document_types, etc.
        client: Anthropic client instance
    Returns:
        Expert answer as a string
    """
    country_info = ""
    if context.get("destination_country"):
        country_data = check_hague_membership(context["destination_country"])
        country_info = (
            f"\n\nCOUNTRY CONTEXT for {country_data['country']}:\n"
            f"Hague Member: {country_data['hague_member']}\n"
            f"Service Needed: {country_data['service_needed']}\n"
            f"Summary: {country_data['summary']}\n"
        )
        if country_data.get("notes"):
            country_info += f"Additional Notes: {country_data['notes']}"

    doc_context = ""
    if context.get("document_types"):
        doc_context = f"\n\nDocument Types: {', '.join(context['document_types'])}"

    full_question = f"{question}{country_info}{doc_context}"

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        system=_CACHED_EXPERT_SYSTEM,
        messages=[{"role": "user", "content": full_question}],
    )
    return response.content[0].text


def get_country_guidance(country: str, document_types: list[str], client: anthropic.Anthropic) -> str:
    """
    Provide specific guidance for a destination country and document combination.
    """
    country_data = check_hague_membership(country)

    prompt = (
        f"A customer needs to use the following documents in {country}: {', '.join(document_types)}.\n\n"
        f"Country status: {country_data['summary']}\n"
        f"Additional notes: {country_data.get('notes', 'None')}\n\n"
        "Please provide a clear, step-by-step explanation of what they need to do, "
        "what service they need from us, and any important warnings or tips specific to this country."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        system=_CACHED_EXPERT_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
