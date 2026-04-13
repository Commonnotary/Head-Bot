import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

COMPANY_NAME    = os.getenv("COMPANY_NAME", "Common Notary Apostille")
COMPANY_EMAIL   = os.getenv("COMPANY_EMAIL", "info@commonapostille.com")
COMPANY_PHONE   = os.getenv("COMPANY_PHONE", "")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://www.commonapostille.com")

# Model used by the orchestrating Head Bot (most capable)
HEAD_BOT_MODEL = os.getenv("HEAD_BOT_MODEL", "claude-opus-4-6")

# Model used by focused sub-agents (fast, efficient)
AGENT_MODEL = os.getenv("AGENT_MODEL", "claude-sonnet-4-6")
