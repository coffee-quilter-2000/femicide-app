"""
Femicide in the United States: main app

OWNER: project lead. This file only arranges the page. Each part of the page lives in its own file:

    sections/map_section.py        Person 1  interactive US map (left column)
    sections/trends_section.py     Person 2  socio-economic trend charts (right column, "Trends")
    sections/profiles_section.py   Person 3  victim icons and profiles (right column, "Victims")
    sections/detail_section.py     Person 4  detailed trends with demographic filters (bottom)
    content/  and  assets/         Person 5  all written text and images

Run from the project folder:   streamlit run app.py
"""

import base64
import importlib
import tomllib
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Femicide in the United States", page_icon="📊", layout="wide")

import data   # noqa: E402  (imports after set_page_config on purpose)
import theme  # noqa: E402

APP_DIR = Path(__file__).parent
CONTENT = APP_DIR / "content"
BANNER_IMAGE = APP_DIR / "assets" / "banner.jpg"
MAP_HEIGHT = 650          # px; the map and the right column are this tall
BANNER_HEIGHT = 200       # px
NAV_HEIGHT = 40           # px; matches Streamlit's own top bar so its buttons sit inside the ribbon


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_text(name: str, default: str = "") -> str:
    """Text from content/<name>, or a default if the file is missing."""
    path = CONTENT / name
    return path.read_text(encoding="utf-8").strip() if path.exists() else default


def read_header() -> dict:
    path = CONTENT / "header.toml"
    try:
        return tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except tomllib.TOMLDecodeError as e:
        st.error(f"content/header.toml has a formatting error, so default text is shown: {e}")
        return {}


def safe_render(section: str, name: str, **kwargs) -> None:
    """Load sections/<section>.py and run its render(). If the file has any error (even a typo
    that stops it from loading), show a message in its place instead of stopping the whole app,
    so one person's mistake can't break anyone else's section."""
    try:
        module = importlib.import_module(f"sections.{section}")
        module.render(**kwargs)
    except Exception as e:
        st.error(f"The **{name}** section has an error and is hidden for now. "
                 "The rest of the app still works.")
        with st.expander("Error details (for the section owner)"):
            st.exception(e)


# ---------------------------------------------------------------------------
# 1. Top ribbon, banner with title, subtitle ribbon
# ---------------------------------------------------------------------------
header = read_header()
TITLE = header.get("title", "Femicide in the United States")
SUBTITLE = header.get("subtitle", "")
BANNER_ALT = header.get("banner_alt", "A collage of photographs of women and girls killed in the United States")
NAV_LINKS = [            # (label, link to a section heading further down the page)
    ("What is femicide?", "#what-is-femicide"),
    ("Map", "#femicide-across-the-us"),
    ("Trends", "#socio-economic-trends"),
    ("Details", "#a-closer-look"),
]

if BANNER_IMAGE.exists():
    img_b64 = base64.b64encode(BANNER_IMAGE.read_bytes()).decode()
    banner_bg = f"url('data:image/jpeg;base64,{img_b64}') center / cover no-repeat"
    banner_note = ""
else:
    banner_bg = "linear-gradient(120deg, #3a3a3a, #1f1f1f)"
    banner_note = '<div class="hero-note">Banner placeholder: save the photo collage as assets/banner.jpg</div>'

nav_html = "".join(f'<a href="{href}" target="_self">{label}</a>' for label, href in NAV_LINKS)

st.markdown(
    f"""
    <style>
      {theme.css_variables()}

      /* Streamlit's own top bar (Rerun menu, Deploy) stays, but see-through, so its
         buttons sit on our ribbon. Clicks pass through it except on its buttons. */
      header[data-testid="stHeader"] {{ background: transparent; }}
      header[data-testid="stHeader"], header[data-testid="stHeader"] * {{ pointer-events: none; }}
      header[data-testid="stHeader"] button,
      header[data-testid="stHeader"] a,
      header[data-testid="stHeader"] [data-testid="stStatusWidget"] {{ pointer-events: auto; }}
      [data-testid="stDecoration"] {{ display: none; }}
      .block-container {{ padding-top: 0 !important; }}
      [data-testid="stMain"] {{ overflow-x: hidden; }}
      /* Style-only st.markdown blocks still take up a slot (and a gap) in the page; remove them */
      [data-testid="stElementContainer"]:has(style):not(:has(.full-bleed)) {{ display: none; }}

      .full-bleed {{ width: 100vw; position: relative; left: 50%; margin-left: -50vw;
                     padding-top: {NAV_HEIGHT}px; }}
      .top-nav {{
        position: fixed; top: 0; left: 0; right: 0; z-index: 999989;
        background: var(--primary); height: {NAV_HEIGHT}px; display: flex; align-items: center;
        gap: 28px; padding: 0 200px 0 32px; font-size: 14px;
      }}
      .top-nav .brand {{ color: var(--text); font-weight: 700; margin-right: auto; letter-spacing: .02em; }}
      .top-nav a {{ color: var(--text) !important; text-decoration: none; }}
      .top-nav a:hover {{ text-decoration: underline; }}

      .hero {{ height: {BANNER_HEIGHT}px; background: {banner_bg}; position: relative;
               display: flex; align-items: center; justify-content: center; }}
      .hero::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.45); }}
      .hero-title {{ position: relative; color: #fff; text-align: center; margin: 0; padding: 0 24px;
                     font-size: clamp(2rem, 5vw, 3.75rem); font-weight: 800; line-height: 1.1;
                     text-shadow: 0 2px 12px rgba(0, 0, 0, 0.6); }}
      .hero-note {{ position: absolute; bottom: 12px; width: 100%; text-align: center;
                    color: #bdbdbd; font-size: 13px; }}
      .subtitle-ribbon {{ background: var(--surface); border-bottom: 1px solid var(--border);
                          padding: 10px 24px; text-align: center; color: var(--text); font-size: 15px;
                          margin-bottom: 1.5rem; }}

      /* Selected Trends / Victims button: solid gold with dark text */
      [data-testid="stButtonGroup"] button[aria-checked="true"] {{
        background: var(--primary) !important; color: var(--text) !important; font-weight: 700; }}
      /* Chips in multiselect boxes: dark text on the gold (white text is hard to read) */
      [data-baseweb="tag"], [data-baseweb="tag"] span {{ color: var(--text) !important; }}
      [data-baseweb="tag"] svg {{ fill: var(--text) !important; }}
    </style>

    <div class="full-bleed">
      <nav class="top-nav"><span class="brand">{TITLE}</span>{nav_html}</nav>
      <div class="hero" role="img" aria-label="{BANNER_ALT}">
        <div class="hero-title" role="heading" aria-level="1">{TITLE}</div>
        {banner_note}
      </div>
      <div class="subtitle-ribbon">{SUBTITLE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

warning = read_text("content_warning.md")
if warning:
    st.info(warning, icon=":material/info:")

# ---------------------------------------------------------------------------
# 2. What is femicide?  (text from content/intro.md)
# ---------------------------------------------------------------------------
st.subheader("What is femicide?")
st.markdown(read_text("intro.md", "*Intro text goes in content/intro.md*"))
st.divider()

# ---------------------------------------------------------------------------
# 3. Map (2/3) and right column (1/3)
# ---------------------------------------------------------------------------
left, right = st.columns([2, 1], gap="large")

# Controls first, so the map also knows the selected state
with right:
    state = st.selectbox("Select State:", data.STATES, index=data.STATES.index(data.DEFAULT_STATE), key="state")
    view = st.segmented_control("View", ["Trends", "Victims"], default="Trends", key="view",
                                label_visibility="collapsed") or "Trends"

with left:
    st.subheader("Femicide across the US")
    safe_render("map_section", "map", state=state, height=MAP_HEIGHT)

with right:
    if view == "Trends":
        safe_render("trends_section", "trends", state=state, height=MAP_HEIGHT - 130)
    else:
        safe_render("profiles_section", "victim profiles", state=state)

st.divider()

# ---------------------------------------------------------------------------
# 4. A closer look: detailed trends with demographic filters
# ---------------------------------------------------------------------------
st.subheader("A closer look")
safe_render("detail_section", "detailed trends", state=state)
st.divider()

# ---------------------------------------------------------------------------
# 5. Sources and notes  (text from content/sources.md)
# ---------------------------------------------------------------------------
with st.expander("Data sources and notes"):
    st.markdown(read_text("sources.md", "*Sources go in content/sources.md*"))
