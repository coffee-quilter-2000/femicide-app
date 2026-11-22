"""
MAP SECTION: interactive US map (left column, 2/3 of the page)
OWNER: Person 1 · branch: map

What you can change:  everything in this file, and anything in the maps/ folder.
Please don't change:  the setup block, or the name and inputs of render().

Your interactive map is an HTML page. Save it as  maps/us_map.html  and this section shows it.
Test this section on its own (from the project folder):
    streamlit run sections/map_section.py
"""

# ===== Setup: leave this block as it is ========================================
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # finds theme.py and data.py
import streamlit as st  # noqa: E402
import streamlit.components.v1 as components  # noqa: E402

import data  # noqa: E402
import theme  # noqa: E402
# ===============================================================================

MAP_FILE = Path(__file__).resolve().parents[1] / "maps" / "us_map.html"


def render(state: str, height: int = 650) -> None:
    """Draw the map. `state` is the state chosen in the dropdown (e.g. "Washington"),
    in case the map should highlight it. `height` is the space available, in pixels."""
    if not MAP_FILE.exists():
        theme.placeholder(
            "Interactive US map",
            "Save the map page as maps/us_map.html and it will appear here.",
            height=height,
        )
        return

    html = MAP_FILE.read_text(encoding="utf-8")
    # Optional: put the text {{STATE}} anywhere in your HTML/JavaScript and it is replaced with
    # the selected state's name, e.g.  const selectedState = "{{STATE}}";
    html = html.replace("{{STATE}}", state).replace("{{STATE_ABBR}}", data.STATE_ABBR.get(state, ""))
    components.html(html, height=height, scrolling=False)


# ===== Test view: runs only with `streamlit run sections/map_section.py` ===========
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Map section (test view)")
    test_state = st.selectbox("State", data.STATES, index=data.STATES.index(data.DEFAULT_STATE),
                              key="test_state")
    col, _ = st.columns([2, 1])           # same width as in the real app
    with col:
        render(test_state)
