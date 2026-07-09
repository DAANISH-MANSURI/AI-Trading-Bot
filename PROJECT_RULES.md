# AI Trading Bot v3.0

## Project
This project's roadmap is defined in:
- trading_bot_roadmap.md

Always follow the roadmap.
Do not implement future phases.
Implement only the current phase.

---

# Project Goal
Build one institutional Smart Money Concepts (SMC) trading system.
This is NOT a collection of independent strategies.
Every module contributes to a single trade decision pipeline.
Final trade decisions are based on institutional confluence.

---

# Blueprint Requirement

For these core decision-logic phases only, provide a short blueprint 
BEFORE writing code — just 4-5 bullet points stating the exact rule, 
condition, or threshold. No long explanation. After the blueprint, wait 
for approval, then implement:

- Market Structure (BOS / CHoCH detection rules)
- Fair Value Gap (FVG) detection rules
- Support / Resistance zone scoring rules
- Fibonacci Golden Zone + confluence overlap rules
- Confluence Engine scoring/threshold system

For all other phases (chart drawing, logging, risk formula implementation 
using already-agreed rules, live execution wiring, integration work), 
proceed directly to implementation without a blueprint step.

---

# Data Integrity Rules
Do not build logic that depends on tick volume as if it were real 
institutional volume. MT5 tick volume is a proxy, not real order flow.
Use pure price-action logic for structure, liquidity, and confluence 
detection.
Do not introduce "order flow," "liquidity analysis," or "volume profile" 
concepts unless explicitly requested — these terms often disguise weak 
or unverifiable logic.

---

# Development Rules
Always inspect the existing implementation before writing code.
Reuse existing code whenever possible.
Avoid duplicate logic.
Keep modules modular and reusable.
Maintain backward compatibility unless the roadmap explicitly requires 
breaking changes.

---

# File Rules
Modify any existing file if required for the current phase.
Create new files only within the scope of the current phase, as defined 
in trading_bot_roadmap.md.
Do not create files belonging to future phases, even if it seems like it 
would improve architecture.
Remove obsolete code only if it is no longer used.
Do not perform unnecessary formatting changes.

---

# Architecture Rules
Respect the existing project structure.
Respect existing folders.
Respect existing module boundaries.
Do not redesign the architecture without approval.
Do not create duplicate implementations.
One responsibility per module.

---

# Integration Rules
Before importing anything:
- Verify the function exists.
- Verify the module exists.
- Do not import incomplete modules.
- Do not leave broken imports.

If a new module requires integration, update all required imports and 
integration points.

---

# Startup Rules
The project must remain runnable after every implementation.

Before completing a phase verify:
- No ImportError
- No circular imports
- No missing functions
- No broken integration
- No startup errors

Fix integration issues before considering the phase complete.

---

# Trading Flow
Always preserve this pipeline:

Higher Timeframe Bias
↓
Market Structure
↓
BOS / CHOCH
↓
Fibonacci Golden Zone
↓
Fair Value Gap (FVG)
↓
Support / Resistance
↓
Confirmation Candle
↓
Confluence Engine
↓
Risk Manager
↓
Trade Execution
↓
Trade Management
↓
Logging

Do not change this flow unless the roadmap explicitly requires it.

---

# Confluence Engine
This project uses ONE institutional trading system.
The Confluence Engine evaluates how many required conditions align 
before allowing a trade.
It does NOT combine unrelated trading strategies.
Each phase builds another component of the same trading system.

---

# Coding Style
Write production-quality Python.
Match the existing coding style.
Use descriptive names.
Avoid duplicated calculations.
Keep functions small and reusable.
Write clean, maintainable code.

---

# Before Completing Any Phase
Verify:
- imports
- integration
- modified modules
- compatibility
- startup

For core decision-logic phases (see Blueprint Requirement section), the 
Implementation Summary must clearly state the exact logic used — precise 
conditions, threshold values, and scoring weights — not just a list of 
functions created. This must be manually verifiable against real chart 
examples before the phase is considered complete.

Do not finish the phase if the project is broken.

---

# Response Format
After implementation provide only:
1. Files Created
2. Files Modified
3. Implementation Summary
4. Manual Testing Steps
5. Git Commit Message
