"""
TRENDS SECTION: socio-economic trend charts (right column, "Trends" button)
OWNER: Person 2 · branch: trends

Four small line charts for the state picked in the dropdown, each compared with the US average:
    femicide rate · poverty rate · uninsured rate · bachelor's degree or higher
The area between the state's line and the US line is shaded red where the state is doing worse
than the US and green where it's doing better (for education, higher is better).

Data: data/state_trends.csv  (made by scripts/export_state_trends.py; see the README)

What you can change:  everything in this file.
Please don't change:  the setup block, or the name and inputs of render().
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

import pandas as pd  # noqa: E402
import plotly.graph_objects as go  # noqa: E402

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "state_trends.csv"
START_YEAR = 2005                  # charts start here (the Census series are thin before 2005)
EXCLUDE_FROM_US_FEMICIDE = ["FL"]  # Florida sends almost no SHR reports; leaving it in would drag the US rate down
REPORTING_GAP = (2020.5, 2022.5)   # FBI reporting changeover: femicide counts are incomplete here

# (column in the CSV, chart title, unit, higher_is_worse, decimals)
METRICS = [
    ("female_victims_per_100k_women", "Femicide rate", "per 100k women", True, 2),
    ("poverty_rate", "Poverty rate", "%", True, 1),
    ("uninsured_rate_under65", "Uninsured, under 65", "%", True, 1),
    ("pct_ba_plus_25", "Bachelor's degree or higher, adults 25+", "%", False, 1),
]

# Colors from theme.py (with fallbacks, so this file works even with an older theme.py)
STATE_COLOR = theme.SERIES[0]
US_COLOR = getattr(theme, "US_LINE", "#8f8f8f")
WORSE_FILL = getattr(theme, "WORSE_FILL", "rgba(224, 96, 90, 0.28)")
BETTER_FILL = getattr(theme, "BETTER_FILL", "rgba(27, 175, 122, 0.28)")
WORSE_TEXT = getattr(theme, "WORSE_TEXT", "#c0392b")
BETTER_TEXT = getattr(theme, "BETTER_TEXT", "#0b7a52")


# ---- Data ------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_trends(path: str, modified: float) -> pd.DataFrame:
    """Read the CSV once and keep it in memory. `modified` makes it reload when the file changes."""
    df = pd.read_csv(path, dtype={"state_fips": str})
    df["state_fips"] = df["state_fips"].str.zfill(2)
    df["state_abb"] = df["state_abb"].str.upper()
    return df


@st.cache_data(show_spinner=False)
def us_average(df: pd.DataFrame) -> pd.DataFrame:
    """US value per year for each metric (index = year).

    Femicide: all female victims ÷ all women × 100,000, over states that report.
    Others:   state values weighted by each state's population, so big states count more.
    """
    out = {}
    fem = df[df["female_victims"].notna() & df["pop_female"].notna()
             & ~df["state_abb"].isin(EXCLUDE_FROM_US_FEMICIDE)]
    g = fem.groupby("year")[["female_victims", "pop_female"]].sum()
    out["female_victims_per_100k_women"] = 100000 * g["female_victims"] / g["pop_female"]

    for key, *_ in METRICS[1:]:
        d = df[df[key].notna() & df["pop_total"].notna()]
        g = d.assign(weighted=d[key] * d["pop_total"]).groupby("year")[["weighted", "pop_total"]].sum()
        out[key] = g["weighted"] / g["pop_total"]
    return pd.DataFrame(out)


# ---- Chart pieces ------------------------------------------------------------------
def _shading(years, state_vals, us_vals, higher_is_worse):
    """Polygons filling the gap between the two lines, split where they cross.
    Returns ((worse_x, worse_y), (better_x, better_y)); None separates polygons."""
    worse, better = ([], []), ([], [])

    def add(target, pts):
        for x, y in pts:
            target[0].append(x)
            target[1].append(y)
        target[0].append(None)
        target[1].append(None)

    def pick(diff):
        return worse if (diff > 0) == higher_is_worse else better

    for i in range(len(years) - 1):
        a, b, c, d = state_vals[i], state_vals[i + 1], us_vals[i], us_vals[i + 1]
        if any(pd.isna(v) for v in (a, b, c, d)):
            continue
        x0, x1, d0, d1 = years[i], years[i + 1], a - c, b - d
        if d0 == 0 and d1 == 0:
            continue
        if d0 * d1 >= 0:                                   # no crossing: one quadrilateral
            add(pick(d0 if d0 != 0 else d1), [(x0, a), (x1, b), (x1, d), (x0, c)])
        else:                                              # lines cross: two triangles
            t = d0 / (d0 - d1)
            xc, yc = x0 + t * (x1 - x0), a + t * (b - a)
            add(pick(d0), [(x0, a), (xc, yc), (x0, c)])
            add(pick(d1), [(xc, yc), (x1, b), (x1, d)])
    return worse, better


def _chart(years, state_vals, us_vals, unit, higher_is_worse, decimals, height, gap_band):
    worse, better = _shading(years, state_vals, us_vals, higher_is_worse)
    diffs = [None if pd.isna(s) or pd.isna(u) else s - u for s, u in zip(state_vals, us_vals)]
    pct = unit == "%"
    fmt = f".{decimals}f"

    fig = go.Figure()
    if gap_band:
        fig.add_vrect(x0=gap_band[0], x1=gap_band[1], fillcolor="#efefef", line_width=0, layer="below")
    for (xs, ys), color in [(worse, WORSE_FILL), (better, BETTER_FILL)]:
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", fill="toself", fillcolor=color,
                                 line=dict(width=0), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=years, y=us_vals, mode="lines", name="US average",
                             line=dict(color=US_COLOR, width=1.5, dash="dash"),
                             hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(
        x=years, y=state_vals, mode="lines+markers", name="State",
        line=dict(color=STATE_COLOR, width=2), marker=dict(size=4),
        customdata=list(zip(us_vals, diffs)), showlegend=False,
        hovertemplate=(f"State: %{{y:{fmt}}}{'%' if pct else ''}"
                       f"<br>US: %{{customdata[0]:{fmt}}}{'%' if pct else ''}"
                       f"<br>Difference: %{{customdata[1]:+{fmt}}}{' pts' if pct else ''}<extra></extra>")))

    layout = theme.plotly_layout()
    layout.update(height=height, margin=dict(l=38, r=8, t=6, b=22), hovermode="x unified")
    fig.update_layout(**layout)
    fig.update_xaxes(range=[years[0] - 0.5, years[-1] + 0.5], dtick=5, showgrid=False,
                     ticks="outside", ticklen=3)
    fig.update_yaxes(gridcolor=theme.BORDER, zeroline=False, ticksuffix="%" if pct else "",
                     nticks=4)
    return fig


def _summary(title, years, state_vals, us_vals, unit, higher_is_worse, decimals):
    """Bold title plus the latest year's value, US value and difference (red = worse, green = better)."""
    for i in range(len(years) - 1, -1, -1):
        s, u = state_vals[i], us_vals[i]
        if not (pd.isna(s) or pd.isna(u)):
            diff = s - u
            worse = (diff > 0) == higher_is_worse
            color = WORSE_TEXT if worse and diff != 0 else BETTER_TEXT if diff != 0 else theme.MUTED
            label = "worse than US" if worse and diff != 0 else "better than US" if diff != 0 else "same as US"
            sfx = "%" if unit == "%" else ""
            dsfx = " pts" if unit == "%" else ""
            return (f"**{title}** <span style='color:{theme.MUTED}'>· {years[i]}: "
                    f"{s:.{decimals}f}{sfx} vs US {u:.{decimals}f}{sfx}</span> "
                    f"<span style='color:{color}'>({diff:+.{decimals}f}{dsfx}, {label})</span>")
    return f"**{title}** <span style='color:{theme.MUTED}'>· no data for this state</span>"


def _legend(state):
    swatch = "display:inline-block;width:14px;height:10px;vertical-align:middle;margin:0 4px 0 10px"
    return (f"<div style='font-size:12px;color:{theme.MUTED};margin-bottom:4px'>"
            f"<span style='{swatch};border-top:2px solid {STATE_COLOR};height:0'></span>{state}"
            f"<span style='{swatch};border-top:2px dashed {US_COLOR};height:0'></span>US average"
            f"<span style='{swatch};background:{WORSE_FILL}'></span>Worse"
            f"<span style='{swatch};background:{BETTER_FILL}'></span>Better"
            f"<span style='{swatch};background:#efefef'></span>Incomplete FBI data</div>")


# ---- The section -----------------------------------------------------------------
def render(state: str, height: int = 520) -> None:
    """Draw the four trend charts for `state` (e.g. "Washington").
    `height` is the space for all charts together, in pixels."""
    if not DATA_FILE.exists():
        st.info("Trend data not found. Save it as **data/state_trends.csv** "
                "(run `python scripts/export_state_trends.py`, see the README).")
        theme.placeholder(f"Trend charts: {state}", "Charts appear here once the data file exists.",
                          height=height)
        return

    df = load_trends(str(DATA_FILE), DATA_FILE.stat().st_mtime)
    us = us_average(df)
    abbr = data.STATE_ABBR[state]
    st_rows = df[df["state_abb"] == abbr].set_index("year")

    years = list(range(START_YEAR, int(df["year"].max()) + 1))
    chart_height = max(140, (height - 40) // len(METRICS) - 34)

    st.markdown(_legend(state), unsafe_allow_html=True)
    for key, title, unit, higher_is_worse, decimals in METRICS:
        state_vals = [st_rows[key].get(y) if key in st_rows else None for y in years]
        us_vals = [us[key].get(y) for y in years]
        st.markdown(_summary(title, years, state_vals, us_vals, unit, higher_is_worse, decimals),
                    unsafe_allow_html=True)
        band = REPORTING_GAP if key == "female_victims_per_100k_women" else None
        fig = _chart(years, state_vals, us_vals, unit, higher_is_worse, decimals, chart_height, band)
        st.plotly_chart(fig, theme=None, key=f"trends_{key}", config={"displayModeBar": False})

    if abbr in EXCLUDE_FROM_US_FEMICIDE:
        st.caption(f"{state} sends almost no reports to the FBI's homicide database, "
                   "so its femicide rate is missing or far too low.")


# ===== Test view: runs only with `streamlit run sections/trends_section.py` ========
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Trends section (test view)")
    test_state = st.selectbox("State", data.STATES, index=data.STATES.index(data.DEFAULT_STATE),
                              key="test_state")
    _, col = st.columns([2, 1])           # same width as in the real app
    with col:
        render(test_state)
