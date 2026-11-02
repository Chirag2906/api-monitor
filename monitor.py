"""API check logic (no Streamlit here, so it is easy to test)."""
import time
from datetime import datetime
import requests


def check_api(url, timeout=5):
    """Send one GET request and return a result dict."""
    start = time.perf_counter()
    status, error = None, ""
    try:
        r = requests.get(url, timeout=timeout)
        status = r.status_code
        ok = r.ok
    except requests.exceptions.Timeout:
        ok, error = False, "Timeout"
    except requests.exceptions.RequestException as e:
        ok, error = False, type(e).__name__
    ms = round((time.perf_counter() - start) * 1000, 1)
    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "URL": url,
        "Status": status if status is not None else "-",
        "Response (ms)": ms,
        "Result": "Success" if ok else "Failed",
        "Error": error,
    }


def summarize(df):
    """Return summary stats for a results DataFrame."""
    if df.empty:
        return {"avg": 0, "min": 0, "max": 0, "p95": 0, "success": 0, "total": 0}
    ms = df["Response (ms)"]
    return {
        "avg": round(ms.mean(), 1),
        "min": round(ms.min(), 1),
        "max": round(ms.max(), 1),
        "p95": round(ms.quantile(0.95), 1),
        "success": round((df["Result"] == "Success").mean() * 100, 1),
        "total": len(df),
    }
