import streamlit as st
from firecrawl import FirecrawlApp, ScrapeOptions

# === 🔑 Configuration API Key ===
st.sidebar.title("🔐 Firecrawl API Key")
api_key = st.sidebar.text_input("Enter your API key", type="password", placeholder="fc-...")
if api_key:
    st.session_state.api_key = api_key

if "api_key" not in st.session_state or not st.session_state.api_key:
    st.warning("Please enter your Firecrawl API key in the sidebar.")
    st.stop()

@st.cache_resource
def get_firecrawl_client(api_key):
    return FirecrawlApp(api_key=api_key)

app = get_firecrawl_client(st.session_state.api_key)

# === 📄 Navigation Pages ===
page = st.sidebar.radio(
    "📄 Choose a page",
    ["🔍 Basic Search", "🧲 Search + Scrape", "🔬 Advanced Search", "🤖 FIRE-1 Agent"]
)

# === 🔍 Page 1: Basic Search ===
if page == "🔍 Basic Search":
    st.header("🔍 Basic Web Search")

    query = st.text_input("Search query", "firecrawl web scraping")
    limit = st.slider("Number of results", 1, 5, 2)

    if st.button("Run Search"):
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

# === 🧲 Page 2: Search + Scrape ===
elif page == "🧲 Search + Scrape":
    st.header("🧲 Search and Scrape")

    query = st.text_input("Search query", "firecrawl web scraping", key="scrape_query")
    limit = st.slider("Number of results", 1, 3, 2, key="scrape_limit")
    formats = st.multiselect("Scrape formats", ["markdown", "html", "links"], default=["markdown", "links"])

    if st.button("Run Search + Scrape"):
        with st.spinner("Running search and scraping..."):
            try:
                scrape_opts = ScrapeOptions(formats=formats)
                result = app.search(query, limit=limit, scrape_options=scrape_opts)
                if not result.data:
                    st.warning("No data.")
                else:
                    for i, r in enumerate(result.data, 1):
                        st.markdown(f"### {i}. [{r['title']}]({r['url']})")
                        st.write(r.get("description", ""))
                        if "markdown" in formats:
                            st.markdown("#### Markdown")
                            st.markdown(r.get("markdown", "_No markdown_"))
                        if "html" in formats:
                            st.markdown("#### HTML")
                            st.code(r.get("html", ""), language="html")
                        if "links" in formats:
                            st.markdown("#### Links")
                            for link in r.get("links", []):
                                st.write(link)
                        st.markdown("---")
            except Exception as e:
                st.error("Scraping error")
                st.code(str(e))

# === 🔬 Page 3: Advanced Search ===
elif page == "🔬 Advanced Search":
    st.header("🔬 Advanced Search Options")

    query = st.text_input("Query", "latest web scraping techniques", key="adv_query")
    limit = st.slider("Number of results", 1, 10, 3, key="adv_limit")
    lang = st.selectbox("Language", ["", "en", "fr", "de"], index=0)
    country = st.selectbox("Country", ["", "us", "fr", "de"], index=0)
    tbs = st.selectbox("Time filter", ["", "qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"], index=0)
    timeout = st.slider("Timeout (sec)", 5, 60, 30)
    formats = st.multiselect("Formats", ["markdown", "html", "links", "screenshot"], default=["markdown", "links"])

    if st.button("Run Advanced Search"):
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

# === 🤖 Page 4: FIRE-1 Agent ===
elif page == "🤖 FIRE-1 Agent":
    st.header("🤖 FIRE-1 Agent Test")
    
    st.markdown("This demo navigates to [tatielou.com](https://tatielou.com), clicks 'Contact Us', then extracts the H1 heading from the contact page.")
    
    # Ajout d'options de débogage
    debug_mode = st.checkbox("Mode debug", value=True)
    
    if st.button("Run FIRE-1 Agent"):
        with st.spinner("Running FIRE-1..."):
            try:
                if debug_mode:
                    st.info("🔍 Tentative de scraping avec FIRE-1...")
                
                result = app.scrape_url(
                    url="https://tatielou.com/contact",
                    formats=["markdown", "html"],
                    agent={
                        "model": "FIRE-1",
                        "prompt": "Navigate to this contact page and extract the main H1 heading. Look for the primary title or heading on the page."
                    }
                )
                
                if debug_mode:
                    st.info("✅ Requête envoyée avec succès")
                    st.json({"type": type(result).__name__, "attributes": dir(result)})
                
                # ✅ CORRECTION PRINCIPALE : Accès aux données
                if hasattr(result, 'data'):
                    data = result.data
                elif hasattr(result, 'content'):
                    data = result.content
                else:
                    data = result
                
                st.success("Scrape completed.")
                
                # Affichage sécurisé des résultats
                st.subheader("📝 Markdown Content")
                markdown_content = data.get("markdown", "_No markdown content_") if isinstance(data, dict) else getattr(data, 'markdown', '_No markdown content_')
                st.markdown(markdown_content)
                
                st.subheader("🔗 HTML Content")
                html_content = data.get("html", "<!-- No HTML -->") if isinstance(data, dict) else getattr(data, 'html', '<!-- No HTML -->')
                st.code(html_content, language="html")
                
                if debug_mode:
                    st.subheader("🐛 Debug Info")
                    st.json(data if isinstance(data, dict) else str(data))
                    
            except Exception as e:
                st.error(f"🚨 FIRE-1 agent failed: {type(e).__name__}")
                st.code(f"Error details: {str(e)}")
                
                # Messages d'aide spécifiques
                error_msg = str(e).lower()
                if "rate limit" in error_msg:
                    st.warning("⚠️ **Rate limit atteint** : FIRE-1 limite à 10 requêtes/minute")
                elif "credit" in error_msg or "billing" in error_msg:
                    st.warning("⚠️ **Crédits insuffisants** : FIRE-1 coûte 150 crédits par scrape")
                elif "unauthorized" in error_msg or "api key" in error_msg:
                    st.warning("⚠️ **Problème d'authentification** : Vérifiez votre clé API")
                elif "timeout" in error_msg:
                    st.warning("⚠️ **Timeout** : La page met trop de temps à répondre")
                else:
                    st.info("💡 **Conseils de débogage** :")
                    st.markdown("""
                    - Vérifiez que votre clé API est valide et active
                    - Assurez-vous d'avoir suffisamment de crédits (150 par requête FIRE-1)
                    - Testez d'abord avec une page plus simple
                    - Vérifiez que l'URL est accessible publiquement
                    """)

