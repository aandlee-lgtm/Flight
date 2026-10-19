# Working rules for this repository

- Treat the owner's feedback as feature requests: add each one to `docs/BACKLOG.md`
  (date, description, status "Planned").
- Record every discussion in `docs/PRODUCT_HISTORY.md`: the owner's requests and questions, the
  answers and explanations, the decisions, and what shipped in each version. Keep its glossary of
  definitions current. It is the source for user instructions, definitions and release notes.
- Do **not** bump the version, deploy, turn on the schedule or create a release until the owner's
  message explicitly includes `build_new`.
- **No paid services.** Every provider, host and tool must be usable at no cost (owner's decision,
  2026-10-19). Ask before proposing anything that could bill.
- Never fabricate or reuse fares. Cached prices are always labelled Indicative; nothing is
  called bookable unless a source has confirmed it.
- Keep secrets in GitHub Actions secrets or local environment variables, never in the repository.
