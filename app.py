# Import libraries
import streamlit as st

# --- PAGE SETUP ---
main_page = st.Page(
    "views/slidegenie_app.py",
    title="Slide Genie",
    icon=":material/jamboard_kiosk:",
    default=True,
)

config_page = st.Page(
    "views/configuration.py",
    title="Configuration",
    icon=":material/toggle_on:",
)


about_page = st.Page(
    "views/about.py",
    title="About",
    icon=":material/info:",
)

pg = st.navigation({
    "Admin": [config_page],
    "Home": [main_page],
    "About": [about_page],
                    })

pg.run()
