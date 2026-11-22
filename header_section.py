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
        background: #000; height: 44px; display: flex; align-items: center;
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
