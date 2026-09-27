# Vireo Audio SLA Breach Tool

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Scope
The runtime needs only `tickets.csv` and `agents.csv`. The README, policy and email context were used to establish the methodology and are not required for the calculation engine.

## Method decisions
- 616 ticket IDs are duplicated by migration re-import. Duplicate copies match on operational fields, so the current `helpdesk` copy is retained.
- Ticket timestamps are UTC; analysis converts them to IST.
- SLA targets: chat 15m, voice 2h, social 4h, email 8h.
- Breach = first response later than the target.
- Shift is mapped from the resolving agent's active roster assignment on resolution date; unresolved/pending uses first-response date.
- The supplied policy is effective 1 Apr 2025, so the main KPI uses that period. A dashboard toggle exposes the full dataset for sensitivity analysis.
- ₹350 is the policy's per-breach store-credit amount; the tool calls this exposure rather than claiming every open/pending case has already been credited.

## Key interpretation
The Morning shift has most breaches, but 79% of Morning breaches in the policy period were created during Night hours. The supplied policy says after-hours tickets are picked up by the next shift in creation order. This makes queue carryover a key operational hypothesis rather than evidence of individual-agent fault.

## AI use
The breach calculation is deterministic. AI is optional and limited to summarizing verified metrics for the client memo.
