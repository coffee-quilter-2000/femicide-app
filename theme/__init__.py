# theme/__init__.py
import streamlit as st

# Shared values come from config.toml, so they're only defined once
PRIMARY    = st.get_option("theme.primaryColor")
TEXT       = st.get_option("theme.textColor")
BACKGROUND = st.get_option("theme.backgroundColor")
SURFACE    = st.get_option("theme.secondaryBackgroundColor")
SERIES     = st.get_option("theme.chartCategoricalColors")

# Extras that Streamlit has no setting for
NAV_BG       = "#000000"
HERO_OVERLAY = "rgba(0, 0, 0, 0.45)"
FONT         = "Source Sans Pro, Arial, sans-serif"

def apply_css():
    # Publishes the theme as CSS variables that any custom HTML can use
    st.markdown(f"""<style>:root {{
        --primary: {PRIMARY}; --text: {TEXT}; --bg: {BACKGROUND};
        --surface: {SURFACE}; --nav-bg: {NAV_BG}; --hero-overlay: {HERO_OVERLAY};
    }}</style>""", unsafe_allow_html=True)

def plotly_layout():
    # Shared look for every Plotly chart
    return dict(font=dict(family=FONT, color=TEXT), colorway=SERIES,
                paper_bgcolor=BACKGROUND, plot_bgcolor=BACKGROUND)