"""
Pricing Agent — Quotes & Service Options

Responsible for:
- Providing accurate pricing estimates based on service type and urgency
- Explaining what is included in each pricing tier
- Presenting multi-document discounts
- Recommending the right service tier based on the customer's needs and timeline
- Answering payment-related questions
"""

import anthropic
from config.settings import AGENT_MODEL, COMPANY_NAME
from knowledge.services_pricing import SERVICES, DISCOUNTS, PAYMENT_METHODS, get_service_summary

PRICING_SYSTEM_PROMPT = f"""You are the Pricing Specialist at {COMPANY_NAME}. You provide clear,
honest, and professional pricing information to help customers choose the right service for their needs.

You are transparent about what is included in each price, proactive about discounts they may qualify
for, and always position the value of using a professional service vs. attempting the process alone.

IMPORTANT PRICING GUIDELINES:
- Always present prices as "starting at" — exact quotes may vary by state fees and specific circumstances
- Emphasize what is INCLUDED (state fees, shipping, handling, expert review)
- If a customer seems price-sensitive, highlight the Standard tier first and explain the risks of
  attempting apostilles without expert guidance (rejected documents, wasted time, re-submission costs)
- Multi-document discount: {DISCOUNTS['multi_doc']}
- Returning client discount: {DISCOUNTS['returning_client']}
- Bundle discount: {DISCOUNTS['bundle']}

PAYMENT METHODS ACCEPTED:
{chr(10).join(f'- {p}' for p in PAYMENT_METHODS)}

SERVICES AND PRICING:
{chr(10).join(get_service_summary(k) for k in SERVICES)}

Always invite the customer to contact us for a precise quote tailored to their specific situation.
"""


def get_pricing_quote(
    service_type: str,
    quantity: int,
    urgency: str,
    context: dict,
    client: anthropic.Anthropic,
) -> str:
    """
    Generate a pricing quote for the customer's specific needs.

    Args:
        service_type: Type of service (apostille, embassy_legalization, fbi_apostille, etc.)
        quantity: Number of documents
        urgency: standard|expedited|rush|same_day
        context: Additional context
        client: Anthropic client instance
    Returns:
        Formatted pricing response
    """
    destination = context.get("destination_country", "")
    doc_types = context.get("document_types", [])

    prompt = (
        f"Customer needs a quote for:\n"
        f"- Service: {service_type}\n"
        f"- Documents: {', '.join(doc_types) if doc_types else 'Not specified'}\n"
        f"- Quantity: {quantity}\n"
        f"- Urgency/Speed: {urgency}\n"
        f"- Destination country: {destination or 'Not specified'}\n\n"
        "Please provide:\n"
        "1. A clear price estimate (using 'starting at' language)\n"
        "2. What's included in that price\n"
        "3. The expected turnaround time\n"
        "4. Any applicable discounts (multi-doc if quantity >= 3)\n"
        "5. A brief recommendation if the urgency level seems mismatched with their timeline\n"
        "Keep it friendly, professional, and easy to understand."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=768,
        system=PRICING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def recommend_service_tier(deadline_description: str, client: anthropic.Anthropic) -> str:
    """
    Recommend the appropriate service tier based on the customer's stated deadline.
    """
    prompt = (
        f"A customer says: '{deadline_description}'\n\n"
        "Based on this, recommend the most appropriate service tier (Standard, Expedited, Rush, or Same-Day). "
        "Explain why, and mention the price difference between tiers so they can make an informed decision."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=512,
        system=PRICING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
