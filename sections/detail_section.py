"""
DETAIL SECTION: "A closer look": trends by demographic group, with filters (bottom of the page)
OWNER: Person 4 · branch: detail

What you can change:  everything in this file.
Please don't change:  the setup block, or the name and inputs of render().

Give every widget a key that starts with "detail_" (e.g. key="detail_age") so it can't
clash with widgets in other sections.
Test this section on its own (from the project folder):
    streamlit run sections/detail_section.py
"""

# ===== Setup: leave this block as it is ========================================
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # finds theme.py and data.py
import streamlit as st  # noqa: E402

import data  # noqa: E402
import theme  # noqa: E402
# ===============================================================================

AGE_GROUPS = ["Under 18", "18–24", "25–34", "35–49", "50–64", "65+", "Unknown"]
RELATIONSHIPS = ["Intimate partner", "Family member", "Acquaintance", "Stranger", "Unknown"]
RACES = ["Asian / Pacific Islander", "Black", "American Indian / Alaska Native", "White", "Unknown"]


def render(state: str) -> None:
    """Draw the detailed section. `state` is the state chosen in the dropdown above."""
    # ---- Filters ------------------------------------------------------------------
    where = st.radio("Area", [state, "United States"], horizontal=True, key="detail_area")

    c1, c2, c3 = st.columns(3)
    ages = c1.multiselect("Victim age", AGE_GROUPS, default=AGE_GROUPS, key="detail_age")
    rels = c2.multiselect("Relationship to killer", RELATIONSHIPS, default=RELATIONSHIPS,
                          key="detail_relationship")
    races = c3.multiselect("Victim race", RACES, default=RACES, key="detail_race")
    years = st.slider("Years", data.YEARS[0], data.YEARS[-1], (2000, data.YEARS[-1]), key="detail_years")

    st.caption(f"Showing: {where} · {years[0]}–{years[1]} · {len(ages)} age groups · "
               f"{len(rels)} relationship types · {len(races)} race groups")

    # ---- Charts -------------------------------------------------------------------
    left, right = st.columns(2, gap="large")
    with left:
        theme.placeholder("Femicide by age group over time", "Chart goes here.", height=320)
    with right:
        theme.placeholder("Femicide by relationship to the killer", "Chart goes here.", height=320)


# ===== Test view: runs only with `streamlit run sections/detail_section.py` ========
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Detail section (test view)")
    test_state = st.selectbox("State", data.STATES, index=data.STATES.index(data.DEFAULT_STATE),
                              key="test_state")
    render(test_state)
