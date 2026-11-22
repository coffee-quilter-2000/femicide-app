"""
Femicide in the United States: Streamlit app (layout with placeholders)

Run from the project folder:
    streamlit run app.py

Layout
    1. Title
    2. Banner image across the top of the page      -> assets/banner.jpg
    3. Short description of femicide
    4. Two columns
         left  (2/3): interactive US map (HTML page)  -> maps/us_map.html
         right (1/3): socio-economic trend lines      -> to be built
    5. Sources and notes
"""


from pathlib import Path
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# Settings: change these as the real pieces arrive
# ---------------------------------------------------------------------------

import theme
theme.apply_css()

# custom HTML uses the CSS variables
#   .top-nav { background: var(--nav-bg); }
#   .subtitle-ribbon { background: var(--surface); color: var(--text); }

APP_DIR: Path = Path(__file__).parent
BANNER_IMAGE = APP_DIR / "assets" / "banner.jpg"    # photo collage spanning the page
MAP_HTML = APP_DIR / "maps" / "us_map.html"          # teammate's interactive map page
MAP_HEIGHT = 500                                     # pixels; match the map page's height

TREND_CHARTS = [
    "Femicide rate (per 100k women)",
    "Poverty rate",
    "Uninsured rate",
    "Education (bachelor's degree or higher)",
]

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Femicide in the United States",
    page_icon="📊",
    layout="wide",                  # use the full browser width
)

# Slightly tighter spacing at the top of the page
st.markdown(
    """
    <style>
      .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def placeholder(label: str, note: str, height: int) -> None:
    """A bordered, fixed-height box that marks where a real element will go."""
    with st.container(border=True, height=height):
        st.markdown(f"**{label}**")
        st.caption(note)


# ---------------------------------------------------------------------------
# 1–2. Top nav ribbon, full-width banner with the title, subtitle ribbon
# ---------------------------------------------------------------------------
import base64

TITLE = "Femicide in the United States"
SUBTITLE = "Homicides of women and girls, 1976–2024, alongside poverty, health insurance and education"
BANNER_HEIGHT = 200          # px
NAV_LINKS = [                # (label, link to a section heading further down the page)
    ("What is femicide?", "#what-is-femicide"),
    ("Map", "#femicide-across-the-us"),
    ("Trends", "#socio-economic-trends"),
]

# Banner background: the photo collage if it exists, otherwise a dark placeholder
if BANNER_IMAGE.exists():
    img_b64 = base64.b64encode(BANNER_IMAGE.read_bytes()).decode()
    mime = "image/png" if BANNER_IMAGE.suffix.lower() == ".png" else "image/jpeg"
    banner_bg = f"url('data:{mime};base64,{img_b64}') center / cover no-repeat"
    banner_note = ""
else:
    banner_bg = "linear-gradient(120deg, #3a3a3a, #1f1f1f)"
    banner_note = (f'<div class="hero-note">Banner placeholder: save the photo collage as '
                   f'{BANNER_IMAGE.relative_to(APP_DIR).as_posix()}</div>')

nav_html = "".join(f'<a href="{href}" target="_self">{label}</a>' for label, href in NAV_LINKS)

st.markdown(
    f"""
    <style>
      /* Hide Streamlit's own top bar so the black ribbon is the top of the page */
      header[data-testid="stHeader"] {{ display: none; }}
      .block-container {{ padding-top: 0 !important; }}
      [data-testid="stMain"] {{ overflow-x: hidden; }}
      /* Style-only st.markdown blocks still take up a slot (and a gap) in the page; remove them */
      [data-testid="stElementContainer"]:has(style):not(:has(.full-bleed)) {{ display: none; }}

      /* Full-width pieces: break out of Streamlit's centered content column */
      .full-bleed {{ width: 100vw; position: relative; left: 50%; margin-left: -50vw; }}

      .top-nav {{
        background: st.get_option("theme.primaryColor"); height: 44px; display: flex; align-items: center;
        gap: 28px; padding: 0 32px; font-size: 14px;
      }}
      .top-nav .brand {{ color: #fff; font-weight: 700; margin-right: auto; letter-spacing: .02em; }}
      .top-nav a {{ color: #d6d6d6 !important; text-decoration: none; }}
      .top-nav a:hover {{ color: #fff !important; text-decoration: underline; }}

      .hero {{
        height: {BANNER_HEIGHT}px; background: {banner_bg};
        display: flex; align-items: center; justify-content: center; position: relative;
      }}
      .hero::before {{                 /* darkens the photos so the title stays readable */
        content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.45);
      }}
      .hero-title {{
        position: relative; color: #fff; text-align: center; margin: 0; padding: 0 24px;
        font-size: clamp(2rem, 5vw, 3.75rem); font-weight: 800; line-height: 1.1;
        text-shadow: 0 2px 12px rgba(0, 0, 0, 0.6);
      }}
      .hero-note {{
        position: absolute; bottom: 12px; width: 100%; text-align: center;
        color: #bdbdbd; font-size: 13px;
      }}

      .subtitle-ribbon {{
        background: #f2f2f2; border-bottom: 1px solid #e0e0e0;
        padding: 10px 24px; text-align: center; color: #333; font-size: 15px;
        margin-bottom: 1.5rem;
      }}
    </style>

    <div class="full-bleed">
      <nav class="top-nav"><span class="brand">{TITLE}</span>{nav_html}</nav>
      <div class="hero" role="img"
           aria-label="A collage of photographs of women and girls killed in the United States">
        <div class="hero-title" role="heading" aria-level="1">{TITLE}</div>
        {banner_note}
      </div>
      <div class="subtitle-ribbon">{SUBTITLE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 3. What is femicide?
# ---------------------------------------------------------------------------
st.subheader("What is femicide?")
st.markdown(
    """
    *Placeholder text: edit to match the group's definition.*

    **Femicide** is the killing of women and girls, most often because they are women.
    The World Health Organization describes it as the intentional killing of women, and notes
    that a large share of these killings are committed by a current or former intimate partner.
    The United States has no official femicide count, so this project builds one from the FBI's
    Supplementary Homicide Reports and looks at how it moves alongside poverty, health insurance
    coverage and education.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# 4. Two columns: map (2/3) and trend lines (1/3)
# ---------------------------------------------------------------------------
left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader("Femicide across the US")
    if MAP_HTML.exists():
        components.html(MAP_HTML.read_text(encoding="utf-8"), height=MAP_HEIGHT, scrolling=False)
    else:
        placeholder(
            "Interactive US map",
            f"The map page goes here. Save the HTML file as `{MAP_HTML.relative_to(APP_DIR)}` "
            "(or point `MAP_HTML` at its location) and it will load automatically.",
            height=MAP_HEIGHT,
        )

with right:
    st.subheader("Socio-economic trends")
    st.selectbox("State", ["United States"], disabled=True,
                 help="Placeholder: will let readers pick a state")
    chart_height = (MAP_HEIGHT - 60) // len(TREND_CHARTS)
    for name in TREND_CHARTS:
        placeholder(name, "Trend line chart goes here.", height=chart_height)

st.divider()

# ---------------------------------------------------------------------------
# 5. Sources and notes
# ---------------------------------------------------------------------------
with st.expander("Data sources and notes"):
    st.markdown(
        """
        - **Femicide counts:** FBI Supplementary Homicide Reports, 1976–2024
          (Jacob Kaplan's concatenated files, openICPSR).
        - **Population:** SEER U.S. population estimates (National Cancer Institute),
          based on U.S. Census Bureau estimates.
        - **Poverty, health insurance, education:** U.S. Census Bureau (SAIPE, SAHIE, American Community Survey).
        - **Reporting gaps:** police agencies report to the SHR voluntarily. Florida sends almost no
          reports, and 2021–2022 are incomplete because of the FBI's switch to a new reporting system.
        """
    )
