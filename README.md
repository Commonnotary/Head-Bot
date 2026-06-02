# CNA Head-Bot 🧠

**The master brain for Common Notary Apostille LLC.**

Head-Bot directs five sub-bots to run CNA operations: generate clients,
keep clients, market the firm, and build professional relationships with
attorneys, law firms, and corporations across the DMV, Central VA, and SW VA.

---

## What This Repo Holds

| File | Purpose |
|------|---------|
| `routing-rules.json` | Pricing, regions, and routing logic — the rules |
| `bot-prompts.md` | What each sub-bot does and says — the playbook |
| `connections.md` | How the brain wires to Make.com & Airtable — the map |

---

## The Five Sub-Bots

1. **Intake** — captures every new inquiry
2. **Qualifier** — confirms service type and region
3. **Price** — quotes from the rules
4. **Confirm** — drafts confirmation and invoice (stages only)
5. **Dispatch** — executes delivery after Byron approves

---

## The One Rule That Never Bends

> **No email is sent and no call is placed without Byron's approval first.**
> The brain drafts and stages everything, then waits for a yes.

Also never permitted:
- Notary commission numbers in any client-facing message
- Any mention of AI in client communications

---

## The System at a Glance
