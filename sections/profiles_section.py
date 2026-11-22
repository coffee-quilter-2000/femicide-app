"""
PROFILES SECTION: one woman icon per victim, clickable profiles (right column, "Victims" button)
OWNER: Person 3 · branch: profiles

What you can change:  everything in this file.
Please don't change:  the setup block, or the name and inputs of render().

The data comes from get_victims() below. Right now it makes up PLACEHOLDER victims;
replace its inside with a real query when the profiles table is ready (keep the same fields).
Give every widget a key that starts with "profiles_" so it can't clash with other sections.
Test this section on its own (from the project folder):
    streamlit run sections/profiles_section.py
"""

# ===== Setup: leave this block as it is ========================================
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # finds theme.py and data.py
import json  # noqa: E402
import random  # noqa: E402

import streamlit as st  # noqa: E402
import streamlit.components.v1 as components  # noqa: E402

import data  # noqa: E402
import old-themes  # noqa: E402
# ===============================================================================

ICONS_PER_ROW = 16


def get_victims(state: str, year: int) -> list[dict]:
    """One dict per female victim in `state` and `year`.

    Fields each victim needs:
        id           unique number
        has_profile  True = gold, clickable icon; False = gray icon
        name, age, date, place, summary, source_url   (None when unknown)

    PLACEHOLDER: makes up victims so the layout can be built. Replace with a query, e.g.
        df = data.run_query(f"SELECT ... FROM {data.table('victim_profiles')} WHERE ...")
        return df.to_dict("records")
    """
    rng = random.Random(f"{state}-{year}")          # same placeholder list every time
    victims = []
    for i in range(rng.randint(15, 90)):
        has_profile = rng.random() < 0.35
        victims.append({
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
    return victims


def render(state: str) -> None:
    """Draw the year slider, the icon grid and the profile card for `state`."""
    year = st.select_slider("Year", data.YEARS, value=data.YEARS[-1], key="profiles_year")
    victims = get_victims(state, year)
    n_profiles = sum(v["has_profile"] for v in victims)
    st.markdown(f"**{len(victims)}** women and girls killed in **{state}** in **{year}** "
                f"· {n_profiles} with a profile  \n*Placeholder data*")

    rows = -(-len(victims) // ICONS_PER_ROW)             # rows of icons, rounded up
    height = min(rows * 34 + 60 + 230, 640)              # icons + legend + profile card
    components.html(_icon_grid_html(victims), height=height, scrolling=True)


def _icon_grid_html(victims: list[dict]) -> str:
    on, off = old-themes.LINK, old-themes.NO_DATA
    return f"""
<!doctype html><html><head><meta charset="utf-8"><style>
  body {{ margin: 0; font-family: {old-themes.FONT}; color: {old-themes.TEXT}; }}
  .legend {{ font-size: 12px; margin: 2px 0 8px; display: flex; gap: 14px; align-items: center; }}
  .legend svg {{ width: 9px; height: 18px; vertical-align: -4px; margin-right: 4px; }}
  .grid {{ display: grid; grid-template-columns: repeat({ICONS_PER_ROW}, 1fr); gap: 4px 2px; }}
  .icon {{ border: 0; background: none; padding: 2px 0; line-height: 0; }}
  .icon svg {{ width: 12px; height: 26px; }}
  .icon.on {{ cursor: pointer; color: {on}; }}
  .icon.on:hover svg, .icon.on:focus-visible svg {{ transform: scale(1.25); }}
  .icon.on.active svg {{ outline: 2px solid {on}; outline-offset: 2px; }}
  .icon.off {{ color: {off}; cursor: default; }}
  .card {{ margin-top: 12px; padding: 12px 14px; background: {old-themes.SURFACE}; border-radius: 4px;
           font-size: 14px; line-height: 1.45; min-height: 120px; }}
  .card h4 {{ margin: 0 0 4px; font-size: 16px; }}
  .card .meta {{ color: {old-themes.MUTED}; font-size: 13px; margin-bottom: 6px; }}
  .card .hint {{ color: {old-themes.MUTED}; }}
  .photo {{ float: left; width: 64px; height: 80px; margin: 0 12px 4px 0; background: #e2e2e2;
            display: flex; align-items: center; justify-content: center; font-size: 11px; color: #777; }}
</style></head><body>
  <div class="legend">
    <span><svg viewBox="0 0 20 44" style="color:{on}"><use href="#woman"/></svg>Profile available (click)</span>
    <span><svg viewBox="0 0 20 44" style="color:{off}"><use href="#woman"/></svg>No information yet</span>
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
  const VICTIMS = {json.dumps(victims, default=str)};
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
"""


# ===== Test view: runs only with `streamlit run sections/profiles_section.py` ======
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Profiles section (test view)")
    test_state = st.selectbox("State", data.STATES, index=data.STATES.index(data.DEFAULT_STATE),
                              key="test_state")
    _, col = st.columns([2, 1])           # same width as in the real app
    with col:
        render(test_state)
