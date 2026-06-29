# Engineering & AI Decision Log

This document outlines the thought process, architectural choices, and the dynamic between human engineering direction and AI assistance during the development of this CLI Alarm Clock. It is intended to provide insight into problem definition and technical execution as requested by the hiring team.

## 1. Problem Definition & Requirements Refinement

**Initial Vague Requirement:**
> "Build an alarm clock as a Python CLI application. CLI only, no web UI, no React, no database. There's no detailed spec; decide what to build with the time you have."

**Refinement Strategy (Human directed, AI brainstormed):**
Given a tight 30-minute window, the immediate decision was to prioritize *quality* and *clean architecture* over a bloated feature set. I asked the AI to brainstorm potential features and we collaboratively narrowed them down.

*   **Included Features:**
    *   Set absolute alarms (e.g., `15:30`).
    *   Set relative alarms (e.g., `in 10m`).
    *   Custom notification messages.
    *   Cross-platform audio alerts.
*   **Excluded Features & Why:**
    *   *Recurring Alarms (Cron-style):* Overly complex for a 30-minute scope; introduces edge cases with background daemon management.
    *   *Persistent Storage (SQLite/JSON):* The assignment explicitly prohibited databases. While a local JSON file could save alarms across sessions, keeping state entirely in-memory for the duration of the execution keeps the codebase lean and focused on the core problem.
    *   *External Dependencies (e.g., `click`, `playsound`):* Relying strictly on the Python Standard Library (`argparse`, `time`, `threading`) proves fundamental language proficiency and removes installation friction for the reviewer.

## 2. Design Alternatives & Architectural Decisions

During the design phase, several architectural paths were considered:

### a) Concurrency: `asyncio` vs. `threading` vs. Blocking Execution
*   **Consideration:** An alarm must wait for a period of time. Should we use an async event loop, a background thread, or just block the main thread?
*   **Decision:** We chose a **blocking loop with short sleep intervals** (`time.sleep(1)`). 
*   **Why:** For a simple command-driven CLI (where one command = one process), spinning up an entire `asyncio` event loop is overkill. A blocking thread allows for easy interrupt handling (Ctrl+C) while gracefully checking the remaining time without locking up the CPU. If the app were expanded to an interactive shell (e.g., using the `cmd` module), we would pivot to `threading` to keep the shell responsive.

### b) Interface: Interactive Menu vs. Command-Driven CLI
*   **Consideration:** Should the user boot the app and get a menu (`1. Set Alarm, 2. List Alarms`), or should it behave like standard Unix tools (`alarm set 10:00`)?
*   **Decision:** **Command-driven CLI** via `argparse`.
*   **Why:** It is more idiomatic for developers, allows for scripting/piping in the future, and feels much more professional than a `while True: input()` loop.

## 3. The Human-AI Dynamic

This project was built using a Pair Programming approach with an AI assistant (Gemini). 

**How AI Assisted:**
1.  **Boilerplate Generation:** The AI rapidly drafted the boilerplate for the `argparse` setup, saving valuable minutes.
2.  **Edge-Case Identification:** During time-parsing logic generation, the AI flagged the edge case of setting an absolute time that has already passed today, prompting the logic to roll the alarm over to tomorrow.
3.  **Cross-Platform Fallbacks:** I directed the AI to include sound. The AI suggested `winsound` for Windows, but also intelligently included a `sys.stdout.write('\a')` fallback to ensure it degrades gracefully on macOS/Linux.

**Human Engineering Input & Validation:**
1.  **Scoping:** I constrained the AI from over-engineering the solution. When it initially suggested a background daemon process, I reigned it in to focus on a simpler, synchronous script that guarantees stability within the time limit.
2.  **Code Review & Structuring:** Instead of accepting a single monolithic `main.py` file from the AI, I enforced a modular structure (`main.py`, `alarm.py`, `utils.py`) to demonstrate separation of concerns and testability.
3.  **Test Verification:** I directed the AI to generate unit tests (`test_alarm.py`) specifically for the time-parsing logic, as that is the most error-prone part of an alarm application. I then manually ran the tests and verified edge cases to ensure the AI's logic was mathematically sound.

## Conclusion
The resulting codebase is small but intentionally designed. By aggressively scoping the requirements and managing the AI's output, I was able to deliver a robust, well-structured, and fully tested tool well within the 30-minute constraint.
