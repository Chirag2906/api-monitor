import time
import pandas as pd
import plotly.express as px
import streamlit as st
from monitor import check_api, summarize

st.set_page_config(page_title="API Performance Monitor", page_icon="📡", layout="wide")
st.title("📡 API Performance Monitor")
st.caption("Send repeated requests to a public API and track response time, status and success rate.")

PRESETS = {
    "GitHub API": "https://api.github.com",
    "JSONPlaceholder": "https://jsonplaceholder.typicode.com/posts/1",
    "HTTPBin (status 200)": "https://httpbin.org/status/200",
    "HTTPBin (random 500 error)": "https://httpbin.org/status/500",
    "Custom URL": "",
}

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Settings")
    choice = st.selectbox("API", list(PRESETS))
    url = st.text_input("URL", value=PRESETS[choice], placeholder="https://...")
    checks = st.slider("Number of checks", 1, 30, 10)
    delay = st.slider("Delay between checks (sec)", 0.0, 5.0, 0.5, 0.5)
    timeout = st.slider("Timeout (sec)", 1, 15, 5)
    run = st.button("Run checks", type="primary", width="stretch")
    if st.button("Clear history", width="stretch"):
        st.session_state.history = []
        st.rerun()

if run:
    if not url.startswith(("http://", "https://")):
        st.warning("Enter a valid URL starting with http:// or https://")
    else:
        bar = st.progress(0.0, text="Running checks...")
        for i in range(checks):
            st.session_state.history.append(check_api(url, timeout))
            bar.progress((i + 1) / checks, text=f"Check {i + 1}/{checks}")
            if i < checks - 1:
                time.sleep(delay)
        bar.empty()

df = pd.DataFrame(st.session_state.history)

if df.empty:
    st.info("Pick an API in the sidebar and click **Run checks**.")
else:
    view = df[df["URL"] == url] if url in set(df["URL"]) else df
    s = summarize(view)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Avg response", f"{s['avg']} ms")
    c2.metric("Fastest", f"{s['min']} ms")
    c3.metric("Slowest", f"{s['max']} ms")
    c4.metric("P95", f"{s['p95']} ms", help="95% of requests were faster than this.")
    c5.metric("Success rate", f"{s['success']}%")

    view = view.reset_index(drop=True)
    view["Check #"] = view.index + 1
    fig = px.line(view, x="Check #", y="Response (ms)", color="Result", markers=True,
                  title="Response time per check",
                  color_discrete_map={"Success": "#2ca02c", "Failed": "#d62728"})
    st.plotly_chart(fig, width="stretch")

    st.subheader("All checks")
    st.dataframe(view.drop(columns="Check #").iloc[::-1], width="stretch", hide_index=True)
    st.download_button("Download CSV", view.to_csv(index=False), "api_checks.csv", "text/csv")

st.divider()
st.caption("Built with Python • Streamlit • Requests • Pandas • Plotly")
