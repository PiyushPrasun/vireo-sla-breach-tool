
import streamlit as st
import pandas as pd
from analysis import load_data, prepare, summary, shift_channel, weekly, agent_stats, CREDIT_INR

st.set_page_config(page_title="Vireo SLA Breach Tool", layout="wide")
st.title("Vireo Audio — Weekly SLA Breach Report")
st.caption("Deterministic SLA calculation + optional AI-assisted client summary.")

@st.cache_data
def get_data():
    tickets, agents = load_data("data")
    return prepare(tickets, agents)

t = get_data()
policy = st.sidebar.checkbox("Policy-defined period only (from 1 Apr 2025)", True)
d = t[t["policy_period"]] if policy else t

st.sidebar.markdown("### Method")
for item in [
    "Deduplicate ticket_id; retain the helpdesk copy.",
    "Convert UTC timestamps to IST.",
    "Apply chat 15m / voice 2h / social 4h / email 8h.",
    "Use the resolving agent's active roster assignment.",
    "Breach = first response later than channel target.",
]:
    st.sidebar.write("• " + item)

s = summary(t, policy)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Tickets", f"{s['tickets']:,}")
c2.metric("Breaches", f"{s['breaches']:,}")
c3.metric("Breach rate", f"{s['rate']:.1%}")
c4.metric("SLA-credit exposure", f"₹{s['credits']:,.0f}")

st.markdown("### Business goal")
st.info(
    f"Proposed target: move the breach rate from {s['rate']:.1%} toward 15%. "
    f"At average quarterly volume, each 1-point reduction is worth about "
    f"₹{s['quarters']['tickets'].mean()*0.01*CREDIT_INR:,.0f}/quarter in avoided SLA credits. "
    "15% is a proposed operating target, not a policy threshold."
)

morning = d[d["shift"]=="Morning"]
nb = ((morning["creation_shift"]=="Night") & morning["breach"]).sum()
share = nb / max(1, int(morning["breach"].sum()))
st.warning(
    f"Morning has {morning['breach'].sum():,} breaches; {nb:,} ({share:.0%}) "
    "were created during Night hours. The supplied policy says after-hours tickets "
    "are picked up by the next shift in creation order."
)

st.markdown("### Shift × channel")
sc = shift_channel(t, policy).copy()
sc["breach_rate"] = sc["breach_rate"].map(lambda x: f"{x:.1%}")
st.dataframe(sc, use_container_width=True, hide_index=True)

st.markdown("### Weekly trend")
w = weekly(t, policy)
pivot = w.pivot(index="week_start", columns="shift", values="breach_rate").sort_index()
st.line_chart(pivot)

st.markdown("### Agent detail")
a = agent_stats(t, policy)
tier_filter = st.selectbox("Tier", ["All", "Tier 1", "Tier 2"])
if tier_filter != "All":
    a = a[a["tier"] == int(tier_filter.split()[-1])]
a["breach_rate"] = a["breach_rate"].map(lambda x: f"{x:.1%}")
a["avg_response_minutes"] = a["avg_response_minutes"].round(1)
st.dataframe(a.sort_values(["shift","breaches"], ascending=[True,False]), use_container_width=True, hide_index=True)

st.markdown("### Data-quality checks")
dq = pd.DataFrame({
    "check": ["Raw rows","Unique IDs after dedupe","Duplicate IDs collapsed","Unmatched roster assignments",
              "Missing first responses","Negative response times"],
    "value": [11816,len(t),616,int(t["shift"].isna().sum()),
              int(t["first_response_at"].isna().sum()),int((t["response_minutes"]<0).sum())]
})
st.dataframe(dq, use_container_width=True, hide_index=True)


