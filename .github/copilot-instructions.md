# Copilot / AI agent instructions for Head-Bot

This file captures the minimal, actionable knowledge an AI coding agent needs to be productive in the Head-Bot repository.

Purpose
- This repository implements an automation helper called "Head-Bot" to assist Common Notary (Commonnotary) with client generation, retention, and outreach. See `README.md` for the project's stated goals.

What to do first
- Open and read `README.md` to understand the non-technical goals (emails, calls, client workflows).
- Confirm repository context with the user before running external commands or contacting third parties; the README explicitly requires permission before making calls.

Repository layout & important facts
- This repo is minimal and currently contains only `README.md`. The default branch is `main` and the owner is Commonnotary.
- Because there are no build or test files present, assume there are no automated pipelines until told otherwise.

Coding / change rules for AI agents
- Keep changes minimal and focused. This repo appears to be a specification/assistant; avoid creating large scaffolding without user approval.
- Do not perform network requests, send emails, or place phone calls on behalf of the user. If asked to generate message drafts or call scripts, produce them for human review first.
- When modifying files, prefer small, reversible commits and ask the user whether to open a PR to `main`.

Patterns & examples (discoverable)
- Non-technical requirements live in `README.md`. Any automation that interacts with clients must include an explicit permission step.
- There are no language-specific patterns or frameworks present; treat the repository as documentation-first until code appears.

Developer workflows (what to ask the user)
- Does the project have a preferred runtime, language, or framework to scaffold? If so, provide the language and the commands to build and test.
- Are there CI/CD or infra credentials the agent should not attempt to modify? Ask before touching `.github` workflows or pipeline files.

Safety and privacy
- This project deals with client outreach — be conservative about producing or using personal data. Never auto-send content to third parties.

If you add code
- Add a short README section explaining how to run locally and include explicit `run` and `test` commands.
- Add a `CHANGELOG.md` entry for notable behavior or privacy/security-affecting changes.

When in doubt
- Ask a clarifying question rather than making assumptions. Mention explicit permission for any client-facing action.

Feedback
- After making edits or adding code, ask the human maintainer for feedback and whether to open a PR to `main`.
