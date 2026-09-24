# Personal LLM Red Teaming Lab

A hands-on red teaming exercise against a self-built fintech support chatbot — attacking it, logging the results, and measuring the difference between an undefended and a hardened system prompt.

This is Project 1 of a five-project AI security portfolio spanning fintech and healthtech. Project 2, [injectguard](https://github.com/sethumak-ai/injectguard), is the defensive tool built directly off what this project exposed.

## What this is

A Streamlit-based support chatbot ("SupportBot") for a fictional fintech company, running on a local LLM (Ollama / llama3.2). The bot was then systematically red-teamed — probed with prompt injection, jailbreak, and social-engineering attempts aimed at the kind of things a real fintech assistant needs to protect: other customers' account data, identity verification, and unauthorized transaction approval.

Every attack attempt and the bot's response was logged, so the results are reproducible and auditable rather than anecdotal.

## How it works

- **SupportBot** — a Streamlit chat interface backed by Ollama/llama3.2, playing the role of a fintech account assistant
- **Attack logging** — every prompt sent to the bot, along with its response and whether the attack succeeded, is recorded to a local SQLite database
- **Baseline vs hardened comparison** — the bot was tested twice: once with a minimal/undefended system prompt, and once with a hardened system prompt, to measure how much a properly written system prompt alone can reduce successful attacks
- **Reporting** — results from both runs are compiled into PDF reports comparing baseline and hardened performance

## Why it matters

Most businesses deploying an LLM chatbot never test it against adversarial input before it goes live. This project demonstrates, concretely and with logged evidence, how much a chatbot can be manipulated with no defenses in place — and how much (or how little) a hardened system prompt closes that gap on its own. That gap is exactly what Project 2 (injectguard) is built to close further.

## Tech stack

- Python
- Streamlit
- Ollama (llama3.2, running locally)
- SQLite (attack logging)
- PDF report generation

## Status

Core build complete — SupportBot, attack logging, and baseline/hardened comparison reports are done. Demo video scripted but not yet recorded.

## Related projects

- [Project 2 — injectguard](https://github.com/sethumak-ai/injectguard): the prompt injection detection tool built as the direct fix for what this project exposed.

---

*Part of a five-project AI security portfolio (fintech + healthtech) built while studying AI security via TryHackMe.*
