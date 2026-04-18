"""
Document Advisor Agent — Document Requirements & Preparation Guidance

Responsible for:
- Telling customers exactly what format their documents need to be in
- Advising on whether documents need to be notarized first
- Explaining the difference between originals and certified copies
- Guiding customers on how to obtain certified copies if they don't have them
- Listing what to include when shipping/sending documents to us
"""

import anthropic
from config.settings import AGENT_MODEL, COMPANY_NAME
from knowledge.apostille_info import DOCUMENT_TYPES


def _format_doc_types() -> str:
    lines = []
    for key, info in DOCUMENT_TYPES.items():
        lines.append(f"\n{info['name'].upper()}:")
        lines.append(f"  Examples: {', '.join(info['examples'][:4])}")
        lines.append(f"  Issuing Authority: {info['issuing_authority']}")
        lines.append(f"  Notes: {info['notes']}")
    return "\n".join(lines)


DOCUMENT_SYSTEM_PROMPT = f"""You are the Document Preparation Advisor at {COMPANY_NAME}. Your expertise
is in helping customers understand exactly what their documents need to look like and how to prepare
them for apostille processing.

You are precise, thorough, and proactive — you identify potential issues before the customer sends
their documents, saving them time and money.

DOCUMENT TYPE KNOWLEDGE:
{_format_doc_types()}

YOUR RESPONSIBILITIES:
1. Advise on whether a document needs notarization before apostille
2. Clarify the difference between originals, certified copies, and photocopies
3. Explain where to obtain certified copies (e.g., vital records office, court clerk)
4. List what the customer needs to include in their package to us
5. Warn about common document preparation mistakes
6. Advise on document condition (no tears, no alterations, legible)

DOCUMENT SUBMISSION CHECKLIST (share when relevant):
- Certified copy (NOT a photocopy) of the document
- Completed order form (we provide this)
- Copy of your government-issued photo ID
- Payment
- Prepaid return shipping label (or we can arrange shipping)
- Any state-specific cover letters (we handle this for you)

Always reassure customers that {COMPANY_NAME} handles all the paperwork and submission —
they just need to send us the right documents.
"""


_CACHED_DOC_SYSTEM = [{"type": "text", "text": DOCUMENT_SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]


def advise_on_documents(
    document_types: list[str],
    context: dict,
    client: anthropic.Anthropic,
) -> str:
    """
    Provide document preparation guidance for the specified document types.

    Args:
        document_types: List of document types the customer has
        context: Additional context (destination country, notarization needed, etc.)
        client: Anthropic client instance
    Returns:
        Document preparation advice as a string
    """
    country = context.get("destination_country", "")
    urgency = context.get("urgency", "standard")

    prompt = (
        f"The customer needs to apostille the following documents: {', '.join(document_types)}.\n"
        f"Destination country: {country or 'Not specified'}.\n"
        f"Service urgency: {urgency}.\n\n"
        "Please advise them on:\n"
        "1. Whether each document needs to be notarized first\n"
        "2. What format/condition the documents must be in\n"
        "3. Whether they need certified copies or if originals are acceptable\n"
        "4. Where to get certified copies if they don't have them\n"
        "5. What to include in their package when sending to us\n"
        "Keep the response clear, practical, and organized."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        system=_CACHED_DOC_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def check_document_readiness(document_description: str, client: anthropic.Anthropic) -> str:
    """
    Evaluate whether a customer's described documents are ready for apostille.
    """
    prompt = (
        f"A customer describes their documents as follows: {document_description}\n\n"
        "Based on this description, evaluate:\n"
        "1. Are their documents likely ready for apostille as described?\n"
        "2. What (if anything) still needs to be done before submission?\n"
        "3. Any red flags or concerns?\n"
        "Be direct and helpful."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=768,
        system=_CACHED_DOC_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
