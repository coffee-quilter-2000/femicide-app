"""
theme.py: shared colors and fonts for everything that Streamlit's theme doesn't style on its own
(custom HTML, the icon grid, Plotly charts saved outside Streamlit, the map page).

OWNER: project lead. Section owners import it but don't edit it.

The main values come from .streamlit/config.toml, so changing the theme there updates
every section. Restart the app after editing config.toml.

How to use it in a section file:
    import theme
    theme.PRIMARY                      # gold, e.g. for a highlight
    theme.SERIES[0]                    # first chart color
    fig.update_layout(**theme.plotly_layout())
"""

import streamlit as st


def _opt(name: str, fallback):
    value = st.get_option(f"theme.{name}")
    return value if value else fallback


# ---- From .streamlit/config.toml ---------------------------------------------
PRIMARY = _opt("primaryColor", "#e7b70d")            # gold: ribbon, selected buttons
TEXT = _opt("textColor", "#1b1b1b")
BACKGROUND = _opt("backgroundColor", "#ffffff")
SURFACE = _opt("secondaryBackgroundColor", "#f7f7f7")  # light gray boxes
LINK = _opt("linkColor", "#917204")                  # darker gold: links, clickable icons
BORDER = _opt("borderColor", "#e2e2e2")
SERIES = _opt("chartCategoricalColors", ["#a6830a", "#2a78d6", "#b8336a", "#1baf7a", "#6250d6"])
SEQUENTIAL = _opt("chartSequentialColors", None)

# ---- Extras with no config.toml setting ------------------------------------
MUTED = "#5e5e5e"            # secondary text
US_LINE = "#8f8f8f"          # national-average comparison line
WORSE_FILL = "rgba(224, 96, 90, 0.28)"     # light red: state worse than the US average
BETTER_FILL = "rgba(27, 175, 122, 0.28)"   # light green: state better than the US average
WORSE_TEXT = "#c0392b"       # red text for "worse" differences
BETTER_TEXT = "#0b7a52"      # green text for "better" differences
NO_DATA = "#b8b8b8"          # gray icons / states without data
FONT = "Cantarell, Arial, sans-serif"
HEADING_FONT = "'Work Sans', Arial, sans-serif"


def plotly_layout() -> dict:
    """Shared look for Plotly charts:  fig.update_layout(**theme.plotly_layout())"""
    return dict(
        font=dict(family=FONT, color=TEXT, size=12),
        colorway=SERIES,
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        margin=dict(l=40, r=10, t=40, b=30),
    )


def placeholder(label: str, note: str = "", height: int = 160) -> None:
    """A bordered box marking where a real element will go."""
    with st.container(border=True, height=height):
        st.markdown(f"**{label}**")
        if note:
            st.caption(note)


def css_variables() -> str:
    """CSS variables for custom HTML, e.g.  background: var(--primary);"""
    return (f":root {{ --primary: {PRIMARY}; --text: {TEXT}; --bg: {BACKGROUND}; "
            f"--surface: {SURFACE}; --link: {LINK}; --border: {BORDER}; --muted: {MUTED}; "
            f"--no-data: {NO_DATA}; --font: {FONT}; }}")
