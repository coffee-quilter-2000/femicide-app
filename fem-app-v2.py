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
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# Settings: change these as the real pieces arrive
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).parent
BANNER_IMAGE = APP_DIR / "assets" / "banner.jpg"    # photo collage spanning the page
MAP_HTML = APP_DIR / "maps" / "us_map.html"          # teammate's interactive map page
MAP_HEIGHT = 650                                     # pixels; match the map page's height

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
NAV_HEIGHT = 40              # px; matches Streamlit's own top bar so its buttons sit inside the ribbon

# Ribbon colors come from .streamlit/config.toml, so changing the theme changes the ribbon
NAV_BG = st.get_option("theme.primaryColor") or "#e7b70d"
NAV_TEXT = st.get_option("theme.textColor") or "#1b1b1b"
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
      /* Streamlit's own top bar (Rerun / Settings menu, Deploy) stays, but see-through, so its
         buttons appear on top of our ribbon. Clicks pass through it except on its buttons. */
      header[data-testid="stHeader"] {{ background: transparent; }}
      header[data-testid="stHeader"], header[data-testid="stHeader"] * {{ pointer-events: none; }}
      header[data-testid="stHeader"] button,
      header[data-testid="stHeader"] a,
      header[data-testid="stHeader"] [data-testid="stStatusWidget"] {{ pointer-events: auto; }}
      [data-testid="stDecoration"] {{ display: none; }}   /* thin colored line Streamlit adds */
      .block-container {{ padding-top: 0 !important; }}
      [data-testid="stMain"] {{ overflow-x: hidden; }}
      /* Style-only st.markdown blocks still take up a slot (and a gap) in the page; remove them */
      [data-testid="stElementContainer"]:has(style):not(:has(.full-bleed)) {{ display: none; }}

      /* Full-width pieces: break out of Streamlit's centered content column */
      .full-bleed {{ width: 100vw; position: relative; left: 50%; margin-left: -50vw;
                     padding-top: {NAV_HEIGHT}px; }}   /* room for the fixed ribbon */

      .top-nav {{                      /* stays at the top of the window while scrolling */
        position: fixed; top: 0; left: 0; right: 0; z-index: 999989;   /* just under Streamlit's bar */
        background: {NAV_BG}; height: {NAV_HEIGHT}px; display: flex; align-items: center;
        gap: 28px; padding: 0 200px 0 32px;   /* right side left free for Streamlit's buttons */
        font-size: 14px;
      }}
      .top-nav .brand {{ color: {NAV_TEXT}; font-weight: 700; margin-right: auto; letter-spacing: .02em; }}
      .top-nav a {{ color: {NAV_TEXT} !important; text-decoration: none; }}
      .top-nav a:hover {{ text-decoration: underline; }}

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
    import json, random

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
    YEARS = list(range(1976, 2025))
    VIEWS = ["Trends", "Victims"]

    # ---- Data hooks: placeholders now, BigQuery queries later --------------------
    def get_victims(state: str, year: int) -> list[dict]:
        """One dict per female victim. PLACEHOLDER: replace with a BigQuery query
        (shr_victims joined to a profiles table). `has_profile` decides icon color."""
        rng = random.Random(f"{state}-{year}")          # same placeholder list every time
        out = []
        for i in range(rng.randint(15, 90)):
            has_profile = rng.random() < 0.35
            out.append({
                "id": i + 1,
                "has_profile": has_profile,
                "name": f"Profile placeholder #{i + 1}" if has_profile else None,
                "age": rng.randint(16, 80) if has_profile else None,
                "date": f"{year}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}" if has_profile else None,
                "place": f"{state} (county TBD)" if has_profile else None,
                "summary": ("Short profile text will go here: who she was, and what is known "
                            "about her death.") if has_profile else None,
                "source_url": None,
            })
        return out

    # ---- Controls: state first, then the view buttons ---------------------------
    st.subheader("Socio-economic trends")
    state = st.selectbox("State", STATES, index=STATES.index("Washington"), key="state")
    view = st.segmented_control("View", VIEWS, default="Trends", key="view",
                                label_visibility="collapsed") or "Trends"
    # Selected view button: solid theme gold with dark text (the default gold-on-white text is hard to read)
    st.markdown(f"""<style>
      [data-testid="stButtonGroup"] button[aria-checked="true"] {{
        background: {st.get_option("theme.primaryColor")} !important;
        color: {st.get_option("theme.textColor")} !important; font-weight: 700;
      }}</style>""", unsafe_allow_html=True)

    # ---- Trends view -----------------------------------------------------------
    if view == "Trends":
        chart_height = (MAP_HEIGHT - 130) // len(TREND_CHARTS)
        for name in TREND_CHARTS:
            placeholder(f"{name}: {state}", "Trend line chart goes here.", height=chart_height)

    # ---- Victims view: one woman icon per victim ---------------------------------
    else:
        year = st.select_slider("Year", YEARS, value=YEARS[-1], key="victims_year")
        victims = get_victims(state, year)
        n_profiles = sum(v["has_profile"] for v in victims)
        st.markdown(f"**{len(victims)}** women and girls killed in **{state}** in **{year}** "
                    f"· {n_profiles} with a profile  \n*Placeholder data*")

        icon_on = st.get_option("theme.linkColor") or "#917204"
        icon_off = "#b8b8b8"
        text = st.get_option("theme.textColor") or "#1b1b1b"
        surface = st.get_option("theme.secondaryBackgroundColor") or "#f7f7f7"

        per_row = 16
        rows = -(-len(victims) // per_row)               # ceiling division
        height = min(rows * 34 + 60 + 230, 640)          # icons + legend + profile card

        components.html(f"""
<!doctype html><html><head><meta charset="utf-8"><style>
  body {{ margin: 0; font-family: Cantarell, Arial, sans-serif; color: {text}; }}
  .legend {{ font-size: 12px; margin: 2px 0 8px; display: flex; gap: 14px; align-items: center; }}
  .legend svg {{ width: 9px; height: 18px; vertical-align: -4px; margin-right: 4px; }}
  .grid {{ display: grid; grid-template-columns: repeat({per_row}, 1fr); gap: 4px 2px; }}
  .icon {{ border: 0; background: none; padding: 2px 0; line-height: 0; }}
  .icon svg {{ width: 12px; height: 26px; }}
  .icon.on {{ cursor: pointer; color: {icon_on}; }}
  .icon.on:hover svg, .icon.on:focus-visible svg {{ transform: scale(1.25); }}
  .icon.on.active svg {{ outline: 2px solid {icon_on}; outline-offset: 2px; }}
  .icon.off {{ color: {icon_off}; cursor: default; }}
  .card {{ margin-top: 12px; padding: 12px 14px; background: {surface}; border-radius: 4px;
           font-size: 14px; line-height: 1.45; min-height: 120px; }}
  .card h4 {{ margin: 0 0 4px; font-size: 16px; }}
  .card .meta {{ color: #5e5e5e; font-size: 13px; margin-bottom: 6px; }}
  .card .hint {{ color: #5e5e5e; }}
  .photo {{ float: left; width: 64px; height: 80px; margin: 0 12px 4px 0; background: #e2e2e2;
            display: flex; align-items: center; justify-content: center; font-size: 11px; color: #777; }}
</style></head><body>
  <div class="legend">
    <span><svg viewBox="0 0 20 44" style="color:{icon_on}"><use href="#woman"/></svg>Profile available (click)</span>
    <span><svg viewBox="0 0 20 44" style="color:{icon_off}"><use href="#woman"/></svg>No information yet</span>
  </div>
  <svg width="0" height="0" style="position:absolute"><defs>
    <symbol id="woman" viewBox="0 0 20 44">
      <circle cx="10" cy="5" r="4.5" fill="currentColor"/>
      <path d="M6 11 H14 L18.5 29 H1.5 Z" fill="currentColor"/>
      <rect x="6.2" y="29" width="2.8" height="14" rx="1.2" fill="currentColor"/>
      <rect x="11" y="29" width="2.8" height="14" rx="1.2" fill="currentColor"/>
    </symbol>
  </defs></svg>
  <div class="grid" id="grid"></div>
  <div class="card" id="card"><span class="hint">Click a gold icon to see that victim's profile.</span></div>
<script>
  const VICTIMS = {json.dumps(victims)};
  const grid = document.getElementById('grid'), card = document.getElementById('card');
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
  VICTIMS.forEach(v => {{
    const b = document.createElement('button');
    b.className = 'icon ' + (v.has_profile ? 'on' : 'off');
    b.innerHTML = '<svg viewBox="0 0 20 44"><use href="#woman"/></svg>';
    if (v.has_profile) {{
      b.title = v.name;
      b.setAttribute('aria-label', 'Show profile: ' + v.name);
      b.onclick = () => {{
        document.querySelectorAll('.icon.active').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        card.innerHTML =
          '<div class="photo">Photo</div>' +
          '<h4>' + esc(v.name) + '</h4>' +
          '<div class="meta">Age ' + esc(v.age) + ' · ' + esc(v.date) + ' · ' + esc(v.place) + '</div>' +
          '<div>' + esc(v.summary) + '</div>' +
          (v.source_url ? '<div><a href="' + esc(v.source_url) + '" target="_blank" rel="noopener">Source</a></div>' : '');
      }};
    }} else {{
      b.tabIndex = -1;
      b.setAttribute('aria-label', 'Victim, no information yet');
    }}
    grid.appendChild(b);
  }});
</script></body></html>
""", height=height, scrolling=True)
        
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
