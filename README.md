# Femicide in the United States

A Streamlit app charting femicide in the US (FBI Supplementary Homicide Reports, 1976–2024) alongside poverty, health insurance and education.

## Who owns what

Each person edits **only their own files**, on **their own branch**. Everything reaches `main` through a pull request that the project lead reviews.

| Part of the app | Owner | Branch | Your files |
|---|---|---|---|
| Interactive US map | Person 1 | `map` | `sections/map_section.py`, `maps/` |
| Socio-economic trend charts | Person 2 | `trends` | `sections/trends_section.py` |
| Victim icons and profiles | Person 3 | `profiles` | `sections/profiles_section.py` |
| "A closer look" with demographic filters | Person 4 | `detail` | `sections/detail_section.py` |
| Written text and images | Person 5 | `content` | `content/`, `assets/` |
| Page layout, theme, data access | Project lead | `main` | everything else |

**Please don't edit** `app.py`, `theme.py`, `data.py`, `.streamlit/config.toml` or anyone else's section. If you need a change there, ask the project lead.

## How the app fits together

```
app.py                  page layout: places each section on the page
theme.py                shared colors and fonts (read from .streamlit/config.toml)
data.py                 shared lists (states, years) and BigQuery queries
.streamlit/config.toml  the theme: colors, fonts, chart colors
sections/*.py           one file per section, each with a render() function
content/*.md, *.toml    all written text
assets/                 images (banner.jpg)
maps/                   the map page (us_map.html)
```

If a section has an error, the app shows an error box **in that section only**; the rest of the page keeps working.

## One-time setup

1. Install **GitHub Desktop** (desktop.github.com) and sign in. **File → Clone repository** → pick this repo.
2. Install Python 3.12+ (or Anaconda), then in a terminal in the project folder:
   ```
   conda create -n streamlit python=3.14
   conda activate streamlit
   pip install -r requirements.txt
   ```
3. For real data: copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in the values the project lead sends you privately. Without it the app still runs with placeholder data.

## Your routine

1. In GitHub Desktop: switch to **your branch** (Current branch menu).
2. **Fetch origin**, then **Branch → Update from main**, to get everyone's latest merged work.
3. Edit **only your files**. Test your section on its own:
   ```
   streamlit run sections/your_section.py
   ```
   and the whole app with `streamlit run app.py`.
4. **Commit** with a short message (e.g. "Add poverty line chart"), then **Push origin**.
5. **Create Pull Request** → on GitHub, click **Create pull request**. The project lead reviews and merges it.

Open a pull request every day or two, not one big one at the end.

**Writers (content):** for text-only changes you can edit files directly on GitHub: open the file, click the pencil icon, edit, and choose **Commit to the `content` branch**.

## Rules that keep the app from breaking

- Keep the **setup block** at the top of your section file and the **name and inputs of `render()`** unchanged.
- Give your widgets keys starting with your section name, e.g. `key="detail_age"`, `key="profiles_year"`.
- Never commit passwords or keys. `.streamlit/secrets.toml` is ignored by Git on purpose.
- Need a new Python package? Ask the project lead to add it to `requirements.txt`.
