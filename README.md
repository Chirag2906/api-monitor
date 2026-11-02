# API Performance Monitor

A small Streamlit app that sends repeated requests to a public API and shows response time, status codes and success rate.

## Features
- Preset public APIs or any custom URL
- Configurable number of checks, delay and timeout
- Metrics: average, fastest, slowest, P95 response time, success rate
- Response time chart and a table of every check
- Download results as CSV

## Tech Stack
Python, Streamlit, Requests, Pandas, Plotly

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Project Structure
```text
api-monitor/
├── app.py        # Streamlit UI
├── monitor.py    # request + stats logic
├── requirements.txt
└── README.md
```

## Limitations
Results depend on your own network. Checks run only while the page is open, and history resets when the app restarts. Be polite to public APIs and avoid very high check counts.
