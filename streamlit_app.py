import streamlit as st
from firecrawl import FirecrawlApp, ScrapeOptions

# === Page config ===
st.set_page_config(page_title="Firecrawl App")
st.title("🔥 Firecrawl Search API App")

st.markdown("""
Built by [Charly Wargnier](https://x.com/DataChaz), this demo highlights Firecrawl’s ace new Search API!

[Docs](https://docs.firecrawl.dev/features/search) | [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/search)
""", unsafe_allow_html=True)

# === 🔧 Sidebar API key config ===
#st.sidebar.markdown("### 🔥 Firecrawl Search API App")

api_key = st.sidebar.text_input("Enter your FirecrawlAPI key", type="password", placeholder="fc-...")

st.sidebar.markdown(
    '<small>No key? Get it from <a href="https://www.firecrawl.dev" target="_blank">🔥 Firecrawl.dev</a></small>!',
    unsafe_allow_html=True,
)



api_provided = bool(api_key)
if api_provided:
    st.session_state.api_key = api_key

app = FirecrawlApp(api_key=st.session_state.api_key) if api_provided else None

# === 🔀 Navigation
page = st.sidebar.radio(
    "📄 Choose a page",
    ["🔍 Basic Search", "🔬 Advanced Search", "🧲 Search + Scrape"]
)

# === 🔍 Basic Search ===
if page == "🔍 Basic Search":
    st.header("🔍 Basic Web Search")
    query = st.text_input("Search query", "firecrawl web scraping")
    limit = st.slider("Number of results", 1, 5, 2)

    if not api_provided:
        st.warning("⚠️ Enter your Firecrawl API key to run the search.")
        st.button("Run Search", disabled=True)
    elif st.button("Run Search"):
        with st.spinner("Searching..."):
            try:
                result = app.search(query, limit=limit)
                if not result.data:
                    st.warning("No results.")
                else:
                    for i, r in enumerate(result.data, 1):
                        st.markdown(f"### {i}. [{r['title']}]({r['url']})")
                        st.write(r.get("description", ""))
                        st.markdown("---")
            except Exception as e:
                st.error("Error during search.")
                st.code(str(e))

# === 🔬 Advanced Search ===
elif page == "🔬 Advanced Search":
    st.header("🔬 Advanced Search Options")
    query = st.text_input("Query", "", key="adv_query")
    limit = st.slider("Number of results", 1, 10, 3, key="adv_limit")
    lang = st.selectbox("Language", ["", "en", "fr", "de"])
    country = st.selectbox("Country", ["", "us", "fr", "de"])
    tbs = st.selectbox("Time filter", ["", "qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"])
    timeout = st.slider("Timeout (sec)", 5, 60, 30)
    formats = st.multiselect("Formats", ["markdown", "html", "links", "screenshot"], default=["markdown", "links"])

    if not api_provided:
        st.info("🔒 Please enter your Firecrawl API key to run the advanced search.")
        st.button("Run Advanced Search", disabled=True)
    elif st.button("Run Advanced Search"):
        with st.spinner("Running advanced search..."):
            try:
                scrape_opts = ScrapeOptions(formats=formats) if formats else None
                result = app.search(
                    query=query,
                    limit=limit,
                    lang=lang or None,
                    country=country or None,
                    tbs=tbs or None,
                    timeout=timeout * 1000,
                    scrape_options=scrape_opts
                )
                if not result.data:
                    st.warning("No data.")
                else:
                    for i, r in enumerate(result.data, 1):
                        st.markdown(f"### {i}. [{r['title']}]({r['url']})")
                        st.write(r.get("description", ""))
                        st.markdown("---")
            except Exception as e:
                st.error("Error during advanced search")
                st.code(str(e))

# === 🧲 Search + Scrape ===
elif page == "🧲 Search + Scrape":
    st.header("🧲 Search and Scrape")
    query = st.text_input("Search query", "firecrawl web scraping", key="scrape_query")
    limit = st.slider("Number of results", 1, 3, 2, key="scrape_limit")
    formats = st.multiselect("Scrape formats", ["markdown", "html", "links"], default=["markdown", "links"])

    if not api_provided:
        st.info("🔒 Please enter your Firecrawl API key to run the scrape.")
        st.button("Run Search + Scrape", disabled=True)
    elif st.button("Run Search + Scrape"):
        with st.spinner("Running search and scraping..."):
            try:
                scrape_opts = ScrapeOptions(formats=formats)
                result = app.search(query, limit=limit, scrape_options=scrape_opts)

                if not result.data:
                    st.warning("No data.")
                else:
                    for i, r in enumerate(result.data, 1):
                        st.markdown(f"## {i}. [{r['title']}]({r['url']})")
                        st.write(r.get("description", ""))

                        if "markdown" in formats:
                            with st.expander("📝 Markdown"):
                                st.markdown(r.get("markdown", "_No markdown content_"))

                        if "html" in formats:
                            with st.expander("💻 HTML"):
                                st.code(r.get("html", "<!-- No HTML content -->"), language="html")

                        if "links" in formats:
                            with st.expander("🔗 Links"):
                                links = r.get("links", [])
                                if links:
                                    for link in links:
                                        st.write(f"- {link}")
                                else:
                                    st.write("_No links found._")

                        st.markdown("---")

            except Exception as e:
                st.error("Scraping error")
                st.code(str(e))

