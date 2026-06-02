## Live Infrastructure

### Make.com
- Scenario: CNA Orchestrator — Main Router
- Region: US2
- Webhook module: CNA Inquiry Intake
- All sources POST to the single webhook URL (stored privately, not here)

### Airtable
- Base: Document Tracking System for Notary and Apostille
- Connected via Airtable OAuth (account: admin@commonapostille.com)
- Tables:
  - Clients
  - Document Requests
  - Status Updates

### Status Field Drives the Router
| Status        | Routes To      |
|---------------|----------------|
| New           | Intake Bot     |
| Qualified     | Qualifier Bot  |
| Service set   | Price Bot      |
| Quoted        | Confirm Bot    |
| Confirmed     | Dispatch Bot   |

## Related Repos
- **Common-Apostille** — client-facing web app, intake form, SEO content
- **Flows** — Make.com scenario configs and automation logic
- **Head-Bot** — this repo, the master brain (rules + prompts + connections)

## Security Notes
- Webhook URL and any API keys are NEVER stored in this repo.
- Notary commission numbers NEVER appear in any file or client message.
