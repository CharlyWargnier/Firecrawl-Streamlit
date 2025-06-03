Parfait ! Voici la version entièrement prête à copier-coller dans ton fichier README.md en Markdown pur, sans encodage ni échappement – tu peux l’insérer telle quelle :

⸻


# 🔥 Firecrawl Search API App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://firecrawl.streamlit.app/)

Built by [Charly Wargnier](https://x.com/DataChaz), this Streamlit demo highlights Firecrawl’s ace new Search API — allowing you to search the web and optionally scrape content in one go!

👉 [Docs](https://docs.firecrawl.dev/features/search) • [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/search)

---

## 🔍 What This App Does

This demo lets you:
- Run web searches via the `/search` endpoint
- Scrape content (Markdown, HTML, Links, Screenshots)
- Filter results by language, country, and time
- Control timeouts and result limits

All powered by [`firecrawl-py`](https://pypi.org/project/firecrawl-py/).

---

## 🚀 Quickstart

Install the Python SDK:

```bash
pip install firecrawl-py

Basic usage:

from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

result = app.search("firecrawl web scraping", limit=3)

for r in result.data:
    print(r["title"], r["url"])

With scraping:

from firecrawl import FirecrawlApp, ScrapeOptions

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

scraped = app.search(
    "firecrawl web scraping",
    limit=3,
    scrape_options=ScrapeOptions(formats=["markdown", "links"])
)

for r in scraped.data:
    print(r["title"])
    print(r.get("markdown", "")[:150])
    print(r.get("links", [])[:3])


⸻

🛠 Advanced Options

You can customize:
	•	lang: Language (e.g. "en", "fr")
	•	country: Country (e.g. "us", "de")
	•	tbs: Time filter (qdr:h, qdr:d, qdr:w, etc.)
	•	timeout: Search timeout (in ms)
	•	scrape_options: Output formats (["markdown", "html", "links"], etc.)

⸻

🔗 Useful Links
	•	🌐 Firecrawl.dev
	•	📘 Search API Docs
	•	⚙️ API Reference

⸻

✨ Credits

Created by Charly Wargnier
Follow for updates, SEO magic, and creative dev experiments!

---

Tu peux coller ça tel quel dans ton fichier `README.md` et l'affichage GitHub sera nickel ✨. Si tu veux, je peux aussi te générer le fichier prêt à uploader. Tu veux ?