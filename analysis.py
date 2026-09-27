
import pandas as pd

SLA_MIN = {"chat": 15, "voice": 120, "social": 240, "email": 480}
POLICY_START = pd.Timestamp("2025-04-01", tz="Asia/Kolkata")
CREDIT_INR = 350

def load_data(data_dir="data"):
    tickets = pd.read_csv(f"{data_dir}/tickets.csv")
    agents = pd.read_csv(f"{data_dir}/agents.csv")
    for c in ["created_at", "first_response_at", "resolved_at"]:
        tickets[c] = pd.to_datetime(tickets[c], utc=True, errors="coerce")
    for c in ["from_date", "to_date"]:
        agents[c] = pd.to_datetime(agents[c], errors="coerce")
    return tickets, agents

def prepare(tickets, agents):
    t = tickets.copy()
    t["_helpdesk"] = t["source_system"].eq("helpdesk").astype(int)
    t = t.sort_values(["ticket_id", "_helpdesk"], ascending=[True, False]).drop_duplicates("ticket_id", keep="first").copy()
    t["created_ist"] = t["created_at"].dt.tz_convert("Asia/Kolkata")
    t["first_response_ist"] = t["first_response_at"].dt.tz_convert("Asia/Kolkata")
    t["resolved_ist"] = t["resolved_at"].dt.tz_convert("Asia/Kolkata")
    t["response_minutes"] = (t["first_response_at"] - t["created_at"]).dt.total_seconds() / 60
    t["target_minutes"] = t["channel"].map(SLA_MIN)
    t["breach"] = t["response_minutes"] > t["target_minutes"]
    t["policy_period"] = t["created_ist"] >= POLICY_START
    t["week_start"] = t["created_ist"].dt.normalize() - pd.to_timedelta(t["created_ist"].dt.weekday, unit="D")
    t["creation_shift"] = t["created_ist"].dt.hour.map(
        lambda h: "Night" if h >= 22 or h < 6 else ("Morning" if h < 14 else "Day")
    )

    roster = agents.copy()
    def match(row):
        d = row["resolved_ist"].date() if pd.notna(row["resolved_ist"]) else row["first_response_ist"].date()
        m = roster[
            (roster["agent_id"] == row["agent_id"]) &
            (roster["from_date"].dt.date <= d) &
            (roster["to_date"].isna() | (roster["to_date"].dt.date >= d))
        ]
        return m.iloc[0] if len(m) == 1 else None

    matches = [match(r) for _, r in t.iterrows()]
    for col in ["shift", "tier", "site", "team", "name"]:
        t[col] = [m[col] if m is not None else None for m in matches]
    return t

def summary(t, policy_only=True):
    d = t[t["policy_period"]] if policy_only else t
    q = d.assign(quarter=d["created_ist"].dt.to_period("Q").astype(str)).groupby("quarter").agg(
        tickets=("ticket_id", "size"), breaches=("breach", "sum")
    ).reset_index()
    q["breach_rate"] = q["breaches"] / q["tickets"]
    q["credit_inr"] = q["breaches"] * CREDIT_INR
    return {"tickets": len(d), "breaches": int(d["breach"].sum()),
            "rate": float(d["breach"].mean()), "credits": int(d["breach"].sum()*CREDIT_INR),
            "quarters": q}

def shift_channel(t, policy_only=True):
    d = t[t["policy_period"]] if policy_only else t
    return d.groupby(["shift","channel"]).agg(tickets=("ticket_id","size"), breaches=("breach","sum")).reset_index().assign(
        breach_rate=lambda x: x["breaches"]/x["tickets"])

def weekly(t, policy_only=True):
    d = t[t["policy_period"]] if policy_only else t
    return d.groupby(["week_start","shift"]).agg(tickets=("ticket_id","size"), breaches=("breach","sum")).reset_index().assign(
        breach_rate=lambda x: x["breaches"]/x["tickets"])

def agent_stats(t, policy_only=True):
    d = t[t["policy_period"]] if policy_only else t
    return d.groupby(["agent_id","name","tier","shift","site","team"]).agg(
        tickets=("ticket_id","size"), breaches=("breach","sum"),
        avg_response_minutes=("response_minutes","mean")).reset_index().assign(
        breach_rate=lambda x: x["breaches"]/x["tickets"])
