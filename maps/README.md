# maps/: the interactive map page

OWNER: Person 1 · branch: map

- Save the map as **`us_map.html`** in this folder. `sections/map_section.py` shows it in the left column.
- It is shown in a box **650 pixels tall** and about two-thirds of the page wide; design the map to fit.
- The page must be self-contained (scripts and data inside the file, or loaded from public URLs).
- Optional: write `{{STATE}}` or `{{STATE_ABBR}}` anywhere in the HTML/JavaScript and the app replaces it with the state selected in the dropdown (e.g. `Washington` / `WA`), so the map can highlight it.
- Colors: the theme's gold is `#e7b70d` (ribbon) and `#917204` (links); the 10-step gold scale for maps is in `.streamlit/config.toml` (`chartSequentialColors`).
