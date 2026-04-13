"""
Core apostille knowledge base for Common Notary Apostille agents.
All agents draw from this shared knowledge to ensure consistent,
accurate responses.
"""

WHAT_IS_AN_APOSTILLE = """
An Apostille is an official certification that authenticates the origin of a public
document so that it is legally recognized in foreign countries. It is governed by
the Hague Convention of October 5, 1961 (the "Apostille Convention"), which has
been adopted by over 120 member countries worldwide.

The apostille verifies the authenticity of:
  - The signature on the document
  - The capacity in which the person who signed the document acted
  - The identity of any stamp or seal on the document

Important: An apostille does NOT certify the content of the document — only
its origin and the authenticity of the signatures/seals.
"""

APOSTILLE_VS_AUTHENTICATION = """
Apostille vs. Authentication/Legalization:
- APOSTILLE: Used when the destination country is a member of the Hague Apostille
  Convention. This is a single-step process.
- AUTHENTICATION + LEGALIZATION (also called "Embassy Legalization"): Used when
  the destination country is NOT a member of the Hague Convention (e.g., China,
  UAE, Qatar, Saudi Arabia, Kuwait). This is a multi-step process:
    1. Notarization (if needed)
    2. State-level certification (Secretary of State)
    3. U.S. Department of State authentication
    4. Embassy/Consulate legalization of the destination country
"""

DOCUMENT_TYPES = {
    "personal": {
        "name": "Personal Documents",
        "examples": [
            "Birth certificate",
            "Death certificate",
            "Marriage certificate",
            "Divorce decree / divorce certificate",
            "Adoption records",
            "Name change document",
            "Driver's license (for use abroad)",
        ],
        "issuing_authority": "Vital Records office or county/state clerk",
        "notes": "Must be certified copies, not photocopies. Original certified copies from the issuing authority are required.",
    },
    "educational": {
        "name": "Educational Documents",
        "examples": [
            "Diploma (high school, college, university)",
            "Academic transcripts",
            "Degree certificate",
            "Professional certifications",
        ],
        "issuing_authority": "Educational institution, then notarized",
        "notes": "Diplomas and transcripts must be notarized by a notary public first, then the notary's signature is apostilled.",
    },
    "background_checks": {
        "name": "Background Check Documents",
        "examples": [
            "FBI background check / Identity History Summary",
            "State police background check",
            "Criminal record / no criminal record letter",
        ],
        "issuing_authority": "FBI (federal), State Police (state-level)",
        "notes": (
            "FBI background check apostilles are issued by the U.S. Department of State, NOT the Secretary of State. "
            "State background checks are apostilled by the Secretary of State of the issuing state."
        ),
    },
    "corporate": {
        "name": "Corporate / Business Documents",
        "examples": [
            "Articles of Incorporation",
            "Certificate of Good Standing",
            "Certificate of Formation (LLC)",
            "Corporate bylaws",
            "Board resolution",
            "Power of attorney (corporate)",
            "Registered agent certificate",
            "Operating agreement",
        ],
        "issuing_authority": "Secretary of State (business division)",
        "notes": "Must be certified copies from the Secretary of State. Some documents require notarization before apostille.",
    },
    "legal": {
        "name": "Legal Documents",
        "examples": [
            "Power of attorney",
            "Affidavits",
            "Court documents",
            "Judgments",
            "Contracts (notarized)",
            "Sworn statements",
        ],
        "issuing_authority": "Courts, notary public",
        "notes": "Legal documents typically must be signed before a notary public before being submitted for apostille.",
    },
    "federal": {
        "name": "Federal Documents",
        "examples": [
            "Naturalization certificate",
            "Certificate of citizenship",
            "Patent documents",
            "FDA letters",
            "Social Security Administration letters",
        ],
        "issuing_authority": "U.S. Department of State",
        "notes": "Federal documents are apostilled by the U.S. Department of State, not the individual state Secretary of State.",
    },
}

APOSTILLE_PROCESS = """
Standard Apostille Process (State Documents):

Step 1 — PREPARE THE DOCUMENT
  • Obtain a certified copy of your document from the issuing authority.
  • For notarizable documents (diplomas, affidavits, etc.), have them signed
    before a licensed notary public first.

Step 2 — SUBMIT TO SECRETARY OF STATE
  • Submit the certified/notarized document to the Secretary of State of the
    state where the document was issued (NOT where you live).
  • The Secretary of State attaches the Apostille certificate.

Step 3 — TRANSLATION (if required by destination country)
  • Some countries require a certified translation of the apostilled document.

Step 4 — DELIVERY
  • We arrange secure delivery of your completed apostilled documents.

Federal Apostille Process (FBI background check, naturalization, etc.):
  • Federal documents skip the Secretary of State and go directly to the
    U.S. Department of State in Washington, D.C.
"""

SERVICE_TIMELINE = {
    "standard": {
        "name": "Standard Service",
        "turnaround": "5–10 business days",
        "description": "Best value for non-urgent apostille requests.",
    },
    "expedited": {
        "name": "Expedited Service",
        "turnaround": "2–3 business days",
        "description": "Faster processing for time-sensitive requests.",
    },
    "rush": {
        "name": "Rush Service",
        "turnaround": "24–48 hours",
        "description": "Fastest available processing. Subject to state availability.",
    },
    "same_day": {
        "name": "Same-Day Service",
        "turnaround": "Same business day",
        "description": "Available for select states when submitted before 10 AM. Call to confirm availability.",
    },
}

COMMON_MISTAKES = [
    "Submitting a photocopy instead of a certified copy.",
    "Applying for an apostille from the wrong state (must match the issuing state).",
    "Forgetting that FBI background checks require the U.S. Dept. of State, not the Secretary of State.",
    "Not verifying whether the destination country is a Hague Convention member.",
    "Submitting an expired document (some countries require documents issued within 6–12 months).",
    "Missing a notarization step for diplomas or affidavits before the apostille.",
    "Sending original (irreplaceable) documents instead of certified copies.",
]

FAQ = {
    "how_long": (
        "Processing times vary by service level: Standard (5–10 business days), "
        "Expedited (2–3 business days), Rush (24–48 hours), Same-Day (when available). "
        "Note that state Secretary of State offices can add additional processing time."
    ),
    "which_state": (
        "The apostille must come from the Secretary of State of the state where the "
        "document was ISSUED, not where you currently live."
    ),
    "original_vs_copy": (
        "We strongly recommend sending certified copies rather than originals. "
        "For documents that only exist as originals (e.g., an original diploma), "
        "we will handle them with utmost care and return them via tracked, insured shipping."
    ),
    "multiple_docs": (
        "Yes, we can process multiple documents at the same time. Each document requires "
        "its own apostille, so pricing is per document."
    ),
    "translation": (
        "Some destination countries require a certified translation in addition to the apostille. "
        "We partner with certified translators and can bundle translation with apostille services."
    ),
    "non_hague": (
        "If your destination country is NOT a Hague Convention member, you will need "
        "embassy legalization instead of (or in addition to) an apostille. "
        "We handle both apostilles and embassy legalization."
    ),
}
