"""
Email Draft Agent — Professional Client Communications

Responsible for:
- Drafting professional follow-up emails to customers
- Writing quote confirmation emails
- Creating onboarding/welcome emails with next steps
- Drafting status update emails
- All emails REQUIRE human review and approval before sending
"""

import anthropic
from config.settings import AGENT_MODEL, COMPANY_NAME, COMPANY_EMAIL, COMPANY_PHONE, COMPANY_WEBSITE

EMAIL_SYSTEM_PROMPT = f"""You are the Communications Specialist for {COMPANY_NAME}. You draft
professional, warm, and informative emails on behalf of the company. Your writing style is:

- Professional yet approachable (never stiff or overly formal)
- Clear and concise — customers should understand exactly what they need to do
- Reassuring — customers are often anxious about important documents
- Action-oriented — every email has a clear next step for the customer

COMPANY SIGNATURE BLOCK:
---
{COMPANY_NAME}
Email: {COMPANY_EMAIL}
Phone: {COMPANY_PHONE if COMPANY_PHONE else "[Phone Number]"}
Website: {COMPANY_WEBSITE}
---

IMPORTANT: Always note at the top of your draft "[DRAFT — REQUIRES HUMAN REVIEW BEFORE SENDING]"

Email types you handle:
1. INITIAL INQUIRY RESPONSE — Respond to a new customer inquiry with a warm introduction and next steps
2. QUOTE CONFIRMATION — Confirm a customer's order details and pricing
3. DOCUMENT REQUEST — Ask the customer to send specific documents
4. STATUS UPDATE — Inform the customer about the status of their apostille
5. COMPLETION NOTIFICATION — Let the customer know their apostilled documents are ready/shipped
6. FOLLOW-UP — Follow up on a customer who has not responded
7. THANK YOU — Thank a client after service completion and invite referrals

Always include:
- A warm, personalized greeting (use customer's name if provided)
- The purpose of the email clearly stated upfront
- Specific, numbered next steps (when applicable)
- Contact information for questions
- Professional closing
"""

EMAIL_TEMPLATES = {
    "initial_inquiry": {
        "subject": "Re: Your Apostille Inquiry — {COMPANY_NAME}",
        "purpose": "Respond to a new customer inquiry, introduce the company, summarize what they need, and outline next steps.",
    },
    "quote_confirmation": {
        "subject": "Your Apostille Quote — {COMPANY_NAME}",
        "purpose": "Confirm the customer's quote, list documents, pricing, and turnaround time, and explain how to proceed.",
    },
    "document_request": {
        "subject": "Documents Needed to Process Your Apostille — {COMPANY_NAME}",
        "purpose": "Request specific documents from the customer with clear instructions on how to send them.",
    },
    "status_update": {
        "subject": "Update on Your Apostille Order — {COMPANY_NAME}",
        "purpose": "Inform the customer of the current status of their order.",
    },
    "completion": {
        "subject": "Your Apostilled Documents Are Ready — {COMPANY_NAME}",
        "purpose": "Notify the customer that their documents are apostilled and being shipped/ready for pickup.",
    },
    "follow_up": {
        "subject": "Following Up on Your Apostille Inquiry — {COMPANY_NAME}",
        "purpose": "Friendly follow-up to a customer who has not responded to a previous communication.",
    },
    "thank_you": {
        "subject": "Thank You for Choosing {COMPANY_NAME}",
        "purpose": "Thank the customer, invite them to leave a review, and encourage referrals.",
    },
}


def draft_email(
    email_type: str,
    customer_name: str,
    context: dict,
    client: anthropic.Anthropic,
) -> str:
    """
    Draft a professional email for the given scenario.

    Args:
        email_type: One of the keys in EMAIL_TEMPLATES
        customer_name: Customer's name (or 'Valued Customer' if unknown)
        context: Dict with relevant details (documents, pricing, status, etc.)
        client: Anthropic client instance
    Returns:
        Draft email as a string (marked as requiring human review)
    """
    template = EMAIL_TEMPLATES.get(email_type, EMAIL_TEMPLATES["initial_inquiry"])
    subject = template["subject"].replace("{COMPANY_NAME}", COMPANY_NAME)
    purpose = template["purpose"]

    context_str = "\n".join(f"- {k}: {v}" for k, v in context.items() if v)

    prompt = (
        f"Please draft a {email_type.replace('_', ' ')} email.\n\n"
        f"Customer name: {customer_name}\n"
        f"Email purpose: {purpose}\n"
        f"Suggested subject line: {subject}\n\n"
        f"Context/Details:\n{context_str}\n\n"
        "Write a complete, ready-to-review email draft."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        system=EMAIL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def draft_custom_email(
    instructions: str,
    customer_name: str,
    context: dict,
    client: anthropic.Anthropic,
) -> str:
    """
    Draft a custom email based on free-form instructions from the operator.
    Requires human approval before sending.

    Args:
        instructions: What the email should accomplish
        customer_name: Customer's name
        context: Relevant context
        client: Anthropic client instance
    Returns:
        Draft email as a string
    """
    context_str = "\n".join(f"- {k}: {v}" for k, v in context.items() if v)

    prompt = (
        f"Draft a professional email for a customer named {customer_name}.\n\n"
        f"Instructions: {instructions}\n\n"
        f"Context:\n{context_str}\n\n"
        "Write a complete, professional email draft."
    )

    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        system=EMAIL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
