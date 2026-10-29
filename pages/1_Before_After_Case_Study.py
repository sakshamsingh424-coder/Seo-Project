import pandas as pd
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auditor import analyze, compare
from sample_pages import CASE, FIXES

st.set_page_config(page_title="Before / After SEO Case Study", page_icon="📈", layout="wide")
st.title("📈 Before vs After SEO: Case Study")
st.caption(f"Website: {CASE['site']}  |  Target keyword: '{CASE['keyword']}'")

res = {}
for k in ("before", "after"):
    c = CASE[k]
    res[k] = analyze(c["html"], c["url"], c["load"], 200, CASE["keyword"], c["robots"], c["sitemap"])

b, a = res["before"], res["after"]
issues = lambda r: sum(x["status"] != "pass" for x in r["checks"])
c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall score", f"{a['score']}/100", f"+{a['score'] - b['score']} from {b['score']}")
c2.metric("On-Page", a["category_scores"]["On-Page"], f"+{a['category_scores']['On-Page'] - b['category_scores']['On-Page']}")
c3.metric("Technical", a["category_scores"]["Technical"], f"+{a['category_scores']['Technical'] - b['category_scores']['Technical']}")
c4.metric("Issues remaining", issues(a), f"-{issues(b) - issues(a)}", delta_color="inverse")

st.subheader("Score comparison")
st.bar_chart(pd.DataFrame({"Before SEO": [b["score"], b["category_scores"]["On-Page"], b["category_scores"]["Technical"]],
                           "After SEO": [a["score"], a["category_scores"]["On-Page"], a["category_scores"]["Technical"]]},
                          index=["Overall", "On-Page", "Technical"]))

st.subheader("Problems found initially and how they were fixed")
st.dataframe(pd.DataFrame(FIXES, columns=["Area", "Problem BEFORE", "Fix applied AFTER"]), hide_index=True, width="stretch")

st.subheader("Check-by-check result")
icon = {"pass": "✅", "warn": "⚠️", "fail": "❌", "-": "-"}
df = pd.DataFrame(compare(b, a))
df["before"] = df["before"].map(icon); df["after"] = df["after"].map(icon)
st.dataframe(df[["category", "check", "before", "after", "before_msg", "after_msg"]], hide_index=True, width="stretch")
st.download_button("Download comparison (CSV)", df.to_csv(index=False), "before_after.csv")
