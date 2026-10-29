import json
import pandas as pd
import streamlit as st
from auditor import audit_url, analyze
from sample_pages import SAMPLES

st.set_page_config(page_title="SEO Audit Platform", page_icon="🔍", layout="wide")
st.title("🔍 AI-Powered SEO Audit & Optimization Platform")
st.caption("Milestone 1 · Rule-based on-page and technical SEO analysis")

with st.sidebar:
    st.header("Audit settings")
    demo = st.toggle("Offline demo mode (sample pages)")
    if demo:
        sample = st.selectbox("Sample page", list(SAMPLES))
        url = "https://demo.shop/"
    else:
        url = st.text_input("Page URL", "https://example.com")
    keyword = st.text_input("Target keyword (optional)")
    run = st.button("Run audit", type="primary", width="stretch")

if run:
    try:
        with st.spinner("Fetching and analysing page..."):
            st.session_state["res"] = (analyze(SAMPLES[sample], url, 0.8, 200, keyword, True, demo and sample.startswith("Well"))
                                       if demo else audit_url(url, keyword))
    except Exception as e:
        st.error(f"Could not audit that URL: {e}")

res = st.session_state.get("res")
if not res:
    st.info("Enter a URL in the sidebar and click **Run audit**.")
    st.stop()

df = pd.DataFrame(res["checks"])
c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall SEO score", f"{res['score']}/100")
c2.metric("On-Page", res["category_scores"]["On-Page"])
c3.metric("Technical", res["category_scores"]["Technical"])
c4.metric("Issues (warn + fail)", int((df.status != "pass").sum()))

left, right = st.columns([3, 2])
with left:
    st.subheader("Audit checks")
    pick = st.multiselect("Status", ["fail", "warn", "pass"], default=["fail", "warn"])
    icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}
    view = df[df.status.isin(pick)].copy()
    view["status"] = view.status.map(icon)
    st.dataframe(view[["status", "category", "check", "message", "fix"]], width="stretch", hide_index=True)
with right:
    st.subheader("Top keywords")
    kdf = pd.DataFrame(res["keywords"], columns=["keyword", "count", "density %"])
    st.bar_chart(kdf.set_index("keyword")["count"])
    st.caption(f"{res['word_count']} words analysed")

st.download_button("Download report (JSON)", json.dumps(res, indent=2), "seo_report.json")
st.download_button("Download checks (CSV)", df.to_csv(index=False), "seo_checks.csv")
