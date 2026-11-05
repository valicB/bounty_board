# =============================================================
# Streamlit  -  interfata web pentru Bounty Board (aplicatie MULTI-PAGINA)
# =============================================================
# Nou fata de s22: st.Page(cale, title=, icon=) descrie o pagina;
# st.navigation([...]) construieste meniul din sidebar; navigare.run()
# ruleaza fisierul paginii alese (restul din s38_pages/ nu ruleaza).
#
# STRUCTURA:  s38_ui.py (pornire) + comun.py (API) + s38_pages/{lista,adauga,dashboard}.py
# comun.py sta LANGA s38_ui.py, nu in s38_pages/: Python cauta module in
# folderul fisierului de PORNIRE - din s38_pages/, importul ar da ModuleNotFoundError.
#
# CERINTE:  MySQL pornit + s38_app.py ruland (alt terminal); pip install streamlit requests
# Rulare:  streamlit run s38_ui.py
# =============================================================

import streamlit as st

st.set_page_config(page_title="Bounty Board", page_icon="🧩", layout="wide")

pagina_lista = st.Page("s38_pages/lista.py", title="Task-uri", icon="📋", default=True)
pagina_adauga = st.Page("s38_pages/adauga.py", title="Adauga task", icon="➕", )
pagina_dashboard = st.Page("s38_pages/dashboard.py", title="Dashboard", icon="📊")

navigare = st.navigation([pagina_lista, pagina_adauga, pagina_dashboard])
navigare.run()


# =============================================================
# RECAP
# =============================================================
# Widget-urile din pagini sunt toate din s22 - doar "cutia" multi-pagina
# e noua. comun.py e singurul loc care vorbeste cu API-ul.
# =============================================================