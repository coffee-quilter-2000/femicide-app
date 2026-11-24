"""
Export the Trends data from BigQuery to data/state_trends.csv.

OWNER: project lead (run once, then again whenever the BigQuery tables change).
Run from the project folder, with the streamlit environment active:

    python scripts/export_state_trends.py

It reads the project, dataset and (optional) service-account key from .streamlit/secrets.toml.
Without a service-account key it uses your own Google login
(run `gcloud auth application-default login` once).
"""

import sys
import tomllib
from pathlib import Path

from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = ROOT / "scripts" / "state_trends.sql"
OUT_FILE = ROOT / "data" / "state_trends.csv"

secrets_file = ROOT / ".streamlit" / "secrets.toml"
secrets = tomllib.loads(secrets_file.read_text(encoding="utf-8")) if secrets_file.exists() else {}
bq = secrets.get("bigquery", {})
project = bq.get("project")
dataset = bq.get("dataset", "femicide_project")
if not project:
    sys.exit("Add your project to .streamlit/secrets.toml first:\n[bigquery]\nproject = \"...\"")

if "gcp_service_account" in secrets:
    from google.oauth2 import service_account
    creds = service_account.Credentials.from_service_account_info(secrets["gcp_service_account"])
    client = bigquery.Client(credentials=creds, project=project)
else:
    client = bigquery.Client(project=project)

sql = SQL_FILE.read_text(encoding="utf-8").replace("PROJECT_ID.femicide_project", f"{project}.{dataset}")
df = client.query(sql).to_dataframe()

OUT_FILE.parent.mkdir(exist_ok=True)
df.to_csv(OUT_FILE, index=False)
print(f"Saved {len(df):,} rows ({df['state_abb'].nunique()} states, "
      f"{df['year'].min()}–{df['year'].max()}) to {OUT_FILE.relative_to(ROOT)}")
