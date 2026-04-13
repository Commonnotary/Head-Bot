"""
Service offerings and pricing structure for Common Notary Apostille.
Agents use this to provide accurate quotes and service descriptions.

NOTE: These are base prices. Actual quotes depend on document type,
state, quantity, and urgency. Always invite customers to confirm
pricing by contacting us directly.
"""

SERVICES = {
    "apostille": {
        "name": "Apostille Service",
        "description": (
            "Full apostille processing for documents issued in any U.S. state or federal agency. "
            "Includes document review, submission to the appropriate Secretary of State, "
            "and return shipping."
        ),
        "tiers": {
            "standard": {
                "label": "Standard",
                "turnaround": "5–10 business days",
                "base_price_per_doc": 150,
                "notes": "Includes state fees and standard tracked return shipping.",
            },
            "expedited": {
                "label": "Expedited",
                "turnaround": "2–3 business days",
                "base_price_per_doc": 225,
                "notes": "Includes state fees and overnight return shipping.",
            },
            "rush": {
                "label": "Rush",
                "turnaround": "24–48 hours",
                "base_price_per_doc": 325,
                "notes": "Subject to state office availability. Includes state fees and overnight shipping.",
            },
        },
    },
    "notarization": {
        "name": "Mobile Notary Service",
        "description": (
            "A licensed notary comes to your location to notarize documents. "
            "Required for diplomas, affidavits, powers of attorney, and other documents "
            "before they can receive an apostille."
        ),
        "tiers": {
            "standard": {
                "label": "Standard",
                "turnaround": "Same day or next day appointment",
                "base_price_per_doc": 75,
                "notes": "Travel fee may apply depending on location.",
            },
        },
    },
    "apostille_and_notarization": {
        "name": "Notarization + Apostille Bundle",
        "description": (
            "Complete end-to-end service: we notarize your document and process the apostille. "
            "Best value for diplomas, affidavits, and powers of attorney."
        ),
        "tiers": {
            "standard": {
                "label": "Standard Bundle",
                "turnaround": "7–12 business days",
                "base_price_per_doc": 200,
                "notes": "Includes notarization, state fees, and standard return shipping.",
            },
            "expedited": {
                "label": "Expedited Bundle",
                "turnaround": "3–5 business days",
                "base_price_per_doc": 275,
                "notes": "Includes notarization, state fees, and overnight return shipping.",
            },
        },
    },
    "embassy_legalization": {
        "name": "Embassy Legalization (Non-Hague Countries)",
        "description": (
            "Full legalization chain for countries not in the Hague Convention (e.g., China, UAE, Saudi Arabia). "
            "Includes notarization, Secretary of State certification, U.S. Dept. of State authentication, "
            "and embassy/consulate legalization."
        ),
        "tiers": {
            "standard": {
                "label": "Standard",
                "turnaround": "3–5 weeks",
                "base_price_per_doc": 450,
                "notes": "Includes all government fees and tracked shipping. Embassy fees vary by country.",
            },
            "expedited": {
                "label": "Expedited",
                "turnaround": "2–3 weeks",
                "base_price_per_doc": 650,
                "notes": "Rush processing at each agency level where available.",
            },
        },
    },
    "fbi_apostille": {
        "name": "FBI Background Check Apostille",
        "description": (
            "End-to-end FBI Identity History Summary (background check) service including "
            "fingerprint processing, FBI submission, and U.S. Dept. of State apostille. "
            "Required for immigration and work permits in many countries."
        ),
        "tiers": {
            "standard": {
                "label": "Standard",
                "turnaround": "6–8 weeks",
                "base_price_per_doc": 195,
                "notes": "Includes FBI fee, Dept. of State fee, and return shipping.",
            },
            "expedited": {
                "label": "Expedited",
                "turnaround": "4–6 weeks",
                "base_price_per_doc": 295,
                "notes": "Expedited FBI processing + priority Dept. of State submission.",
            },
        },
    },
    "corporate_apostille": {
        "name": "Corporate Document Apostille",
        "description": (
            "Apostille services for business documents: Articles of Incorporation, "
            "Certificate of Good Standing, corporate resolutions, operating agreements, etc."
        ),
        "tiers": {
            "standard": {
                "label": "Standard",
                "turnaround": "5–10 business days",
                "base_price_per_doc": 175,
                "notes": "Includes obtaining certified copies (if needed), state fees, and return shipping.",
            },
            "expedited": {
                "label": "Expedited",
                "turnaround": "2–3 business days",
                "base_price_per_doc": 250,
                "notes": "Rush processing with overnight return shipping.",
            },
        },
    },
    "translation": {
        "name": "Certified Translation",
        "description": (
            "Certified translation of documents by ATA-certified translators. "
            "Available for apostilled documents that require translation for the destination country."
        ),
        "tiers": {
            "standard": {
                "label": "Standard",
                "turnaround": "2–5 business days",
                "base_price_per_doc": 125,
                "notes": "Price per document page. Complex legal/technical documents may cost more.",
            },
        },
    },
}

DISCOUNTS = {
    "multi_doc": "10% discount when processing 3 or more documents at the same time.",
    "returning_client": "5% loyalty discount for returning clients.",
    "bundle": "Notarization + Apostille bundles already include a combined discount.",
}

PAYMENT_METHODS = [
    "Credit card (Visa, Mastercard, American Express)",
    "Debit card",
    "PayPal",
    "Zelle",
    "Check (for local clients)",
    "Wire transfer (for corporate clients)",
]

def get_service_summary(service_key: str, tier: str = "standard") -> str:
    """Return a formatted pricing summary for a given service and tier."""
    if service_key not in SERVICES:
        return f"Service '{service_key}' not found."
    svc = SERVICES[service_key]
    if tier not in svc["tiers"]:
        tier = list(svc["tiers"].keys())[0]
    t = svc["tiers"][tier]
    return (
        f"**{svc['name']} — {t['label']}**\n"
        f"Turnaround: {t['turnaround']}\n"
        f"Starting at: ${t['base_price_per_doc']} per document\n"
        f"Notes: {t['notes']}\n\n"
        f"{svc['description']}"
    )
