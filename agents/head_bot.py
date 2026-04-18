"""
Head Bot — Master Orchestrator for Common Notary Apostille Customer Service

The Head Bot is the central intelligence that:
1. Receives every customer message
2. Analyzes intent and context
3. Routes to specialized sub-agents via tool calls
4. Synthesizes responses into professional, unified replies
5. Maintains conversation memory and customer context across the session
6. Escalates to human staff when appropriate (email drafts, phone calls)

Architecture:
  Customer → Head Bot → [IntakeAgent | ApostilleExpertAgent |
                          DocumentAdvisorAgent | PricingAgent | EmailDraftAgent]
                      → Unified professional response → Customer
"""

import json
import anthropic
from config.settings import HEAD_BOT_MODEL, COMPANY_NAME, COMPANY_EMAIL, COMPANY_PHONE
from agents.intake_agent import run_intake, extract_intake_summary
from agents.apostille_expert_agent import answer_apostille_question, get_country_guidance
from agents.document_advisor_agent import advise_on_documents, check_document_readiness
from agents.pricing_agent import get_pricing_quote, recommend_service_tier
from agents.email_draft_agent import draft_email, draft_custom_email

# ── Tool definitions exposed to the Head Bot ──────────────────────────────────

TOOLS: list[dict] = [
    {
        "name": "run_intake",
        "description": (
            "Use this to engage the Intake Agent when a customer is new, their needs are unclear, "
            "or you need to gather missing information (document type, destination country, urgency, quantity). "
            "The intake agent is warm and conversational — use it to greet new customers or ask follow-up questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation_history": {
                    "type": "array",
                    "description": "The full conversation history so far as a list of {role, content} dicts.",
                    "items": {"type": "object"},
                },
            },
            "required": ["conversation_history"],
        },
    },
    {
        "name": "answer_apostille_question",
        "description": (
            "Use this when the customer asks about the apostille process, what an apostille is, "
            "the difference between apostille and legalization, timelines, or any procedural question. "
            "Also use this for country-specific guidance questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The customer's specific question to answer.",
                },
                "context": {
                    "type": "object",
                    "description": "Known customer context: destination_country, document_types, urgency.",
                },
            },
            "required": ["question", "context"],
        },
    },
    {
        "name": "get_country_guidance",
        "description": (
            "Use this when you know the customer's destination country and document type(s). "
            "Returns specific apostille vs. legalization requirements and country-specific tips."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "country": {"type": "string", "description": "Destination country name."},
                "document_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of document types the customer needs apostilled.",
                },
            },
            "required": ["country", "document_types"],
        },
    },
    {
        "name": "advise_on_documents",
        "description": (
            "Use this when the customer needs to know how to prepare their documents — "
            "whether they need notarization, certified copies vs. originals, where to get certified copies, "
            "or what to include in their submission package."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "document_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of document types.",
                },
                "context": {
                    "type": "object",
                    "description": "Known context: destination_country, urgency, has_certified_copies.",
                },
            },
            "required": ["document_types", "context"],
        },
    },
    {
        "name": "check_document_readiness",
        "description": (
            "Use this when a customer describes their documents and wants to know if they are ready "
            "to be submitted for apostille."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "document_description": {
                    "type": "string",
                    "description": "Customer's description of their documents.",
                },
            },
            "required": ["document_description"],
        },
    },
    {
        "name": "get_pricing_quote",
        "description": (
            "Use this when the customer asks about pricing, costs, fees, or wants a quote. "
            "Provides pricing based on service type, quantity, and urgency."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "service_type": {
                    "type": "string",
                    "enum": [
                        "apostille",
                        "notarization",
                        "apostille_and_notarization",
                        "embassy_legalization",
                        "fbi_apostille",
                        "corporate_apostille",
                        "translation",
                    ],
                    "description": "The type of service needed.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Number of documents to process.",
                },
                "urgency": {
                    "type": "string",
                    "enum": ["standard", "expedited", "rush", "same_day"],
                    "description": "Service tier / urgency level.",
                },
                "context": {
                    "type": "object",
                    "description": "Additional context: destination_country, document_types.",
                },
            },
            "required": ["service_type", "quantity", "urgency", "context"],
        },
    },
    {
        "name": "recommend_service_tier",
        "description": (
            "Use this when the customer mentions a deadline or timeframe but hasn't selected a service tier. "
            "Returns a recommendation for Standard, Expedited, Rush, or Same-Day service."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "deadline_description": {
                    "type": "string",
                    "description": "Customer's stated deadline or urgency (e.g., 'I need it in 2 weeks').",
                },
            },
            "required": ["deadline_description"],
        },
    },
    {
        "name": "draft_email",
        "description": (
            "Use this to draft a professional email for a customer. "
            "ALWAYS present the draft to the human operator for review and approval BEFORE it is sent. "
            "Email types: initial_inquiry, quote_confirmation, document_request, "
            "status_update, completion, follow_up, thank_you."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "email_type": {
                    "type": "string",
                    "enum": [
                        "initial_inquiry",
                        "quote_confirmation",
                        "document_request",
                        "status_update",
                        "completion",
                        "follow_up",
                        "thank_you",
                    ],
                },
                "customer_name": {
                    "type": "string",
                    "description": "Customer's name, or 'Valued Customer' if unknown.",
                },
                "context": {
                    "type": "object",
                    "description": "Relevant details for the email: documents, pricing, status, etc.",
                },
            },
            "required": ["email_type", "customer_name", "context"],
        },
    },
    {
        "name": "draft_custom_email",
        "description": (
            "Use this to draft a custom email based on operator instructions. "
            "ALWAYS present the draft to the human operator for review and approval BEFORE it is sent."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "instructions": {
                    "type": "string",
                    "description": "What the email should accomplish.",
                },
                "customer_name": {
                    "type": "string",
                    "description": "Customer's name.",
                },
                "context": {
                    "type": "object",
                    "description": "Relevant context for the email.",
                },
            },
            "required": ["instructions", "customer_name", "context"],
        },
    },
]

# ── Head Bot system prompt ─────────────────────────────────────────────────────

HEAD_BOT_SYSTEM_PROMPT = f"""You are the Head Bot — the central orchestrator and customer service director for
{COMPANY_NAME}, a professional apostille and document authentication company based in the United States.

YOUR MISSION:
Deliver exceptional, knowledgeable, and professional customer service to every client.
You oversee a team of specialized agents and direct them to serve each customer's unique needs.
Every response you deliver to a customer must be polished, accurate, and reassuring.

YOUR TEAM (tools you can call):
1. Intake Agent — greets customers, gathers their information
2. Apostille Expert Agent — explains the apostille process and country requirements
3. Document Advisor Agent — guides customers on document preparation
4. Pricing Agent — provides quotes and service tier recommendations
5. Email Draft Agent — drafts professional emails (always requires your review)

OPERATING PRINCIPLES:
- ALWAYS use the appropriate agent tool to generate specialized content — do NOT guess at process
  details, pricing, or country requirements from memory
- Synthesize agent outputs into a SINGLE, unified, professional response — never expose the
  "behind the scenes" agent calls to the customer
- Maintain context throughout the conversation — remember what the customer has already told you
- Be proactive — anticipate their next question and address it before they ask
- NEVER promise specific pricing without using the Pricing Agent tool
- NEVER make up country-specific requirements — always use the Apostille Expert or Country Guidance tool
- Email drafts MUST be shown to the human operator for approval before sending

ESCALATION TO HUMAN STAFF:
Escalate to a human staff member when:
- The customer is upset or frustrated and needs empathy beyond what you can provide
- The situation is genuinely complex and requires expert judgement beyond your tools
- The customer requests to speak with a person
- A phone call is requested (always ask for operator permission before initiating)

In those cases, say: "I'm going to connect you with one of our specialists right away. You can also
reach us directly at {COMPANY_EMAIL}{(' or ' + COMPANY_PHONE) if COMPANY_PHONE else ''}."

TONE & STYLE:
- Professional, warm, and confident
- Use clear, plain English — avoid unnecessary jargon
- Structure long responses with headers or numbered lists for readability
- Keep responses focused — don't overwhelm the customer with information they didn't ask for

Remember: You represent {COMPANY_NAME}. Every interaction is an opportunity to build trust
and demonstrate our expertise.
"""


# Cached system prompt — sent once, reused across turns at no extra latency cost
_CACHED_HEAD_SYSTEM = [
    {"type": "text", "text": HEAD_BOT_SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}
]


# ── Head Bot class ────────────────────────────────────────────────────────────

class HeadBot:
    """
    The orchestrating Head Bot for Common Notary Apostille customer service.
    Manages conversation state and routes to specialized agents via tool use.
    """

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.conversation_history: list[dict] = []
        self.customer_context: dict = {
            "customer_name": None,
            "document_types": [],
            "destination_country": None,
            "urgency": "standard",
            "quantity": 1,
            "has_certified_copies": None,
            "needs_notarization": None,
        }

    def _update_context(self, updates: dict) -> None:
        """Merge new context information into the running customer context."""
        for key, value in updates.items():
            if value is not None and value != [] and value != "unknown":
                self.customer_context[key] = value

    def _dispatch_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool call and return the result as a string."""
        ctx = self.customer_context

        if tool_name == "run_intake":
            return run_intake(tool_input["conversation_history"], self.client)

        elif tool_name == "answer_apostille_question":
            merged_ctx = {**ctx, **tool_input.get("context", {})}
            return answer_apostille_question(tool_input["question"], merged_ctx, self.client)

        elif tool_name == "get_country_guidance":
            return get_country_guidance(
                tool_input["country"],
                tool_input["document_types"],
                self.client,
            )

        elif tool_name == "advise_on_documents":
            merged_ctx = {**ctx, **tool_input.get("context", {})}
            return advise_on_documents(tool_input["document_types"], merged_ctx, self.client)

        elif tool_name == "check_document_readiness":
            return check_document_readiness(tool_input["document_description"], self.client)

        elif tool_name == "get_pricing_quote":
            merged_ctx = {**ctx, **tool_input.get("context", {})}
            return get_pricing_quote(
                tool_input["service_type"],
                tool_input["quantity"],
                tool_input["urgency"],
                merged_ctx,
                self.client,
            )

        elif tool_name == "recommend_service_tier":
            return recommend_service_tier(tool_input["deadline_description"], self.client)

        elif tool_name == "draft_email":
            merged_ctx = {**ctx, **tool_input.get("context", {})}
            return draft_email(
                tool_input["email_type"],
                tool_input.get("customer_name", "Valued Customer"),
                merged_ctx,
                self.client,
            )

        elif tool_name == "draft_custom_email":
            merged_ctx = {**ctx, **tool_input.get("context", {})}
            return draft_custom_email(
                tool_input["instructions"],
                tool_input.get("customer_name", "Valued Customer"),
                merged_ctx,
                self.client,
            )

        else:
            return f"Unknown tool: {tool_name}"

    def _run_tool_use_iterations(self, messages: list[dict]) -> list[dict]:
        """
        Run all tool-use iterations (non-streaming) until the model is ready
        to give its final response.  Returns the messages list with tool results
        appended, ready for the final streaming call.
        """
        while True:
            response = self.client.messages.create(
                model=HEAD_BOT_MODEL,
                max_tokens=2048,
                system=_CACHED_HEAD_SYSTEM,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason != "tool_use":
                # Not a tool call — the model is ready to give the final answer.
                # Return messages as-is so the caller can do a streaming final call.
                return messages

            # Process all tool calls in this response
            messages = messages + [{"role": "assistant", "content": response.content}]
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._dispatch_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages = messages + [{"role": "user", "content": tool_results}]

    def chat_stream(self, user_message: str):
        """
        Generator that yields text chunks as the final response streams in.

        Workflow:
          1. Run all tool-use iterations with create() (fast, cached)
          2. Stream the final synthesis response character-by-character
        This gives customers the fastest possible time-to-first-token on the
        answer they actually see, while tool dispatch runs silently behind the scenes.
        """
        self.conversation_history.append({"role": "user", "content": user_message})
        messages = list(self.conversation_history)

        # Phase 1: resolve all tool calls silently
        messages = self._run_tool_use_iterations(messages)

        # Phase 2: stream the final answer in real time
        full_text = ""
        with self.client.messages.stream(
            model=HEAD_BOT_MODEL,
            max_tokens=2048,
            system=_CACHED_HEAD_SYSTEM,
            tools=TOOLS,
            messages=messages,
        ) as stream:
            for chunk in stream.text_stream:
                full_text += chunk
                yield chunk

        self.conversation_history.append({"role": "assistant", "content": full_text})

    def chat(self, user_message: str) -> str:
        """
        Non-streaming version of chat_stream() — collects all chunks and returns
        the full response as a single string.  Used internally and for testing.
        """
        return "".join(self.chat_stream(user_message))

    def reset(self) -> None:
        """Clear conversation history and context for a new customer session."""
        self.conversation_history = []
        self.customer_context = {
            "customer_name": None,
            "document_types": [],
            "destination_country": None,
            "urgency": "standard",
            "quantity": 1,
            "has_certified_copies": None,
            "needs_notarization": None,
        }
