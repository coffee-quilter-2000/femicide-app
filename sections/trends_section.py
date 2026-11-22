"""
TRENDS SECTION: socio-economic trend charts (right column, "Trends" button)
OWNER: Person 2 · branch: trends

What you can change:  everything in this file.
Please don't change:  the setup block, or the name and inputs of render().

The column is narrow (about 1/3 of the page), so keep charts compact.
Test this section on its own (from the project folder):
    streamlit run sections/trends_section.py
"""

# ===== Setup: leave this block as it is ========================================
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # finds theme.py and data.py
import streamlit as st  # noqa: E402

import data  # noqa: E402
import theme  # noqa: E402
# ===============================================================================

CHARTS = [
    "Femicide rate (per 100k women)",
    "Poverty rate",
    "Uninsured rate",
    "Education (bachelor's degree or higher)",
]


def render(state: str, height: int = 520) -> None:
    """Draw the trend charts for `state` (e.g. "Washington"). `height` is the space
    available for all charts together, in pixels."""
    chart_height = height // len(CHARTS)
    for name in CHARTS:
        theme.placeholder(f"{name}: {state}", "Trend line chart goes here.", height=chart_height)

    # ---- Example of a real chart (delete the placeholders above when you use this) ----
    # import plotly.express as px
    # df = data.run_query(f'''
    #     SELECT year, poverty_rate
    #     FROM {data.table('femicide_census_state_year')}
    #     WHERE state_abb = '{data.STATE_ABBR[state]}' AND year >= 2005
    #     ORDER BY year''')
    # fig = px.line(df, x="year", y="poverty_rate", title=f"Poverty rate: {state}")
    # fig.update_layout(height=chart_height, **theme.plotly_layout())
    # st.plotly_chart(fig)


# ===== Test view: runs only with `streamlit run sections/trends_section.py` ========
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Trends section (test view)")
    test_state = st.selectbox("State", data.STATES, index=data.STATES.index(data.DEFAULT_STATE),
                              key="test_state")
    _, col = st.columns([2, 1])           # same width as in the real app
    with col:
        render(test_state)
