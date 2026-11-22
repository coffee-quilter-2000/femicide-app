"""
data.py: shared data access and lists used by more than one section.

OWNER: project lead. Section owners import it but don't edit it.
Ask the project lead if you need something added here.

How to use it in a section file:
    import data
    data.STATES                                   # list of state names
    df = data.run_query(f"SELECT * FROM {data.table('femicide_state_rate')} WHERE ...")
    if not data.bigquery_ready(): ...             # show placeholder data instead

BigQuery credentials live in .streamlit/secrets.toml on each person's computer
(never on GitHub). See .streamlit/secrets.toml.example for the format.
"""

import pandas as pd
import streamlit as st

# ---- Shared lists -------------------------------------------------------------
STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
    "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
]
STATE_ABBR = dict(zip(STATES, [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN",
    "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
    "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
    "VT", "VA", "WA", "WV", "WI", "WY",
]))
YEARS = list(range(1976, 2025))
DEFAULT_STATE = "Washington"


# ---- BigQuery -----------------------------------------------------------------
def _secrets() -> dict:
    try:
        return st.secrets.to_dict()
    except Exception:          # no secrets.toml on this computer
        return {}


def bigquery_ready() -> bool:
    """True when this computer has BigQuery settings in .streamlit/secrets.toml."""
    return "bigquery" in _secrets()


def table(name: str) -> str:
    """Full BigQuery table name in backticks, e.g. table('femicide_state_rate')."""
    bq = _secrets().get("bigquery", {})
    return f"`{bq.get('project', 'PROJECT_ID')}.{bq.get('dataset', 'femicide_project')}.{name}`"


@st.cache_resource(show_spinner=False)
def _client():
    from google.cloud import bigquery

    secrets = _secrets()
    project = secrets.get("bigquery", {}).get("project")
    if "gcp_service_account" in secrets:                       # shared service-account key
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_info(secrets["gcp_service_account"])
        return bigquery.Client(credentials=creds, project=project or creds.project_id)
    return bigquery.Client(project=project)                     # your own `gcloud` login


@st.cache_data(ttl=3600, show_spinner="Loading data…")
def run_query(sql: str) -> pd.DataFrame:
    """Run a BigQuery query and return a DataFrame. Results are cached for an hour,
    so the same query doesn't run again on every click."""
    return _client().query(sql).to_dataframe()
