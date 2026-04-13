"""
Country-specific apostille and legalization requirements.
Agents use this to give customers accurate guidance based on
their destination country.
"""

# Hague Convention member countries (apostille accepted — not exhaustive, covers most common)
HAGUE_MEMBERS = {
    "Albania", "Andorra", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Barbados",
    "Belarus", "Belgium", "Belize", "Bosnia and Herzegovina", "Botswana",
    "Brazil", "Bulgaria", "Burundi", "Cape Verde", "Chile", "Colombia",
    "Cook Islands", "Costa Rica", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Dominican Republic", "Ecuador", "El Salvador", "Estonia",
    "Fiji", "Finland", "France", "Georgia", "Germany", "Greece", "Grenada",
    "Guatemala", "Guyana", "Honduras", "Hungary", "Iceland", "India",
    "Ireland", "Israel", "Italy", "Japan", "Kazakhstan", "Kosovo", "Latvia",
    "Lesotho", "Liberia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Malawi", "Malta", "Marshall Islands", "Mauritius", "Mexico", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Namibia", "Netherlands",
    "New Zealand", "Nicaragua", "Nigeria", "North Macedonia", "Norway",
    "Oman", "Panama", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Romania", "Russia", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Serbia",
    "Seychelles", "Singapore", "Slovakia", "Slovenia", "South Africa",
    "South Korea", "Spain", "Suriname", "Swaziland", "Sweden", "Switzerland",
    "Tonga", "Trinidad and Tobago", "Turkey", "Ukraine", "United Kingdom",
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela",
}

# Countries NOT in the Hague Convention — require embassy legalization
NON_HAGUE_COUNTRIES = {
    "China", "Canada", "Egypt", "Iran", "Iraq", "Jordan",
    "Kuwait", "Lebanon", "Libya", "Malaysia", "Myanmar", "Pakistan",
    "Qatar", "Saudi Arabia", "Sri Lanka", "Syria", "Taiwan",
    "Thailand", "Tunisia", "United Arab Emirates", "Vietnam", "Yemen",
}

# Country-specific notes for common destinations
COUNTRY_NOTES = {
    "Italy": (
        "Italy is a Hague member. Apostille is accepted. "
        "Many Italian visa applications require apostilled birth certificates, marriage certificates, "
        "criminal record checks, and diplomas. Translations into Italian are often required alongside the apostille."
    ),
    "Germany": (
        "Germany is a Hague member. Apostille is accepted. "
        "German authorities commonly require apostilles on birth certificates, marriage certificates, "
        "and background checks. German translations may be required."
    ),
    "Spain": (
        "Spain is a Hague member. Apostille is accepted. "
        "Spain often requires apostilled documents for residency applications (non-lucrative visa, golden visa). "
        "Commonly requested: birth certificate, background check, financial documents."
    ),
    "Mexico": (
        "Mexico is a Hague member. Apostille is accepted. "
        "Mexico requires apostilled documents for residency and business registration. "
        "Spanish translation is typically required by Mexican authorities."
    ),
    "Brazil": (
        "Brazil is a Hague member. Apostille is accepted. "
        "Brazil began accepting apostilles directly (without further legalization) after joining in 2016. "
        "Certified Portuguese translation is usually required."
    ),
    "China": (
        "China is NOT a Hague Convention member. Documents must go through "
        "embassy legalization (also called consular legalization): "
        "1) Notarization → 2) Secretary of State authentication → "
        "3) U.S. Dept. of State → 4) Chinese Embassy/Consulate legalization. "
        "Note: China joined the Hague Convention but it has not taken effect yet for all document types — "
        "confirm requirements for your specific use case."
    ),
    "United Arab Emirates": (
        "UAE is NOT a Hague Convention member. Full embassy legalization chain is required: "
        "Notarization → Secretary of State → U.S. Dept. of State → UAE Embassy legalization. "
        "This process typically adds 1–2 weeks. We handle the entire chain."
    ),
    "Saudi Arabia": (
        "Saudi Arabia is NOT a Hague Convention member. Full embassy legalization is required. "
        "Process: Notarization → Secretary of State → U.S. Dept. of State → Saudi Embassy. "
        "Required for many work visa and iqama applications."
    ),
    "Canada": (
        "Canada is NOT a Hague Convention member but has a simplified process. "
        "Documents for use in Canada typically need authentication by Global Affairs Canada, "
        "NOT an apostille. We can advise on the correct process."
    ),
    "France": (
        "France is a Hague member. Apostille is accepted. "
        "For long-stay visas and residency, France commonly requires apostilled birth certificates, "
        "marriage certificates, and background checks. French translations are required."
    ),
    "Philippines": (
        "Philippines is a Hague member. Apostille is accepted. "
        "The Philippines DFA (Department of Foreign Affairs) now accepts apostilles directly. "
        "Required for OFW (Overseas Filipino Worker) documentation and immigration purposes."
    ),
    "India": (
        "India is a Hague member. Apostille is accepted. "
        "MEA (Ministry of External Affairs) apostille is required for most documents used in India. "
        "Common uses: employment visas, PCC, educational documents."
    ),
    "Australia": (
        "Australia is a Hague member. Apostille is accepted. "
        "Australian immigration (DIBP) frequently requires apostilled documents. "
        "Character certificates/police clearances are commonly apostilled for Australian visa applications."
    ),
    "United Kingdom": (
        "UK is a Hague member. Apostille is accepted. "
        "UKVI (UK Visas and Immigration) requires apostilled documents for many visa types. "
        "Apostille is issued by the UK FCDO (Foreign, Commonwealth & Development Office) for UK documents, "
        "or the U.S. Secretary of State for U.S. documents destined for use in the UK."
    ),
}


def check_hague_membership(country: str) -> dict:
    """Return apostille/legalization requirements for a given country."""
    country_title = country.strip().title()

    if country_title in HAGUE_MEMBERS:
        notes = COUNTRY_NOTES.get(country_title, "")
        return {
            "country": country_title,
            "hague_member": True,
            "service_needed": "Apostille",
            "summary": (
                f"{country_title} is a member of the Hague Apostille Convention. "
                "An apostille is sufficient — no embassy legalization required."
            ),
            "notes": notes,
        }
    elif country_title in NON_HAGUE_COUNTRIES:
        notes = COUNTRY_NOTES.get(country_title, "")
        return {
            "country": country_title,
            "hague_member": False,
            "service_needed": "Embassy Legalization",
            "summary": (
                f"{country_title} is NOT a member of the Hague Apostille Convention. "
                "Embassy legalization (notarization → state authentication → U.S. Dept. of State → embassy) "
                "is required instead of a simple apostille."
            ),
            "notes": notes,
        }
    else:
        return {
            "country": country_title,
            "hague_member": None,
            "service_needed": "Verification Required",
            "summary": (
                f"We were unable to automatically confirm whether {country_title} is a Hague Convention member. "
                "Please contact us directly and we will verify the exact requirements for your destination country."
            ),
            "notes": "",
        }
