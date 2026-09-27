# Vireo Audio — Weekly SLA Breach Report

**To:** Neha Kulkarni, Support Operations Manager  
**Subject:** Weekly first-response SLA breach report — findings and actions

## The number
Across the policy-defined period (1 Apr 2025–30 Jun 2026), **10,176 unique tickets** were assessed. **2,341 breached** their channel-specific first-response target, a **23.0% breach rate**. At ₹350 per breach, that is **₹8.19 lakh of SLA-credit exposure** in the supplied period.

A proposed management target is to move the breach rate toward **15%**. At the dataset's average quarterly volume, that corresponds to roughly **163 fewer breaches and ₹57,000 less SLA-credit exposure per quarter**. The 15% target is proposed, not a supplied policy threshold.

## What is driving the number?
Morning has **1,957 breaches**, about **84% of all breaches**. But **1,548 (79%) of Morning breaches were created during Night hours**.

The policy says tickets outside staffed hours are picked up by the next shift in creation order. The data therefore points to **night-to-morning queue carryover** as a major operational mechanism behind the Morning breach count. This is an observed relationship, not proof that the roster or handoff caused every breach.

Channel detail:
- Morning chat: **44.1%** breached.
- Day chat: **10.1%** breached.
- Morning email: **28.5%** breached.
- Morning social: **33.5%** breached.
- Voice callback: about **5.8% Morning / 5.5% Day**.

## Recommended operating tests
1. Make the weekly report a **queue-management report**, not an agent leaderboard. Show breach rate, volume, and whether the ticket was created during Night hours.
2. Add a **night→morning carryover metric** to the weekly review: tickets entering Morning already close to or beyond SLA, by channel.
3. Test a **handoff intervention without adding headcount**, such as reserving initial Morning capacity for aged Night-created tickets, and compare breach rate over 2–4 weeks.
4. Keep **Tier 2 separate from Tier 1 volume comparisons**, as required by the supplied policy.

## Data / method notes
The raw export contains 11,816 rows but 11,200 unique ticket IDs; 616 IDs appear twice due to migration re-imports. Operational fields match, so the helpdesk copy is retained. Timestamps are converted from UTC to IST and channel-specific SLAs are applied.

The supplied policy is effective 1 Apr 2025. Jan–Mar 2025 are excluded from the main KPI because no earlier policy was supplied; they remain available as a sensitivity view.
