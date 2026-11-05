# =============================================================
# PAGINA  -  Task-uri  (listare, filtre, rezolva, sterge)
# =============================================================
# Widget-urile sunt toate din s22. Nou e doar sursa datelor: API-ul
# din s38_app.py, prin api() din comun.py.
# =============================================================

import streamlit as st
from comun import api

st.title("📋 Task-uri")

ok, task_uri = api("GET", "/task-uri")
if not ok:
    st.error(task_uri)
    st.stop()

if not task_uri:
    st.info("Nu exista niciun task inca. Adauga unul din pagina 'Adauga task'.")
    st.stop()


# TODO: sidebar cu filtre
#   - selectbox cu limbajele disponibile (+ optiunea "Toate")
#   - checkbox "Doar nerezolvate"
#   - filtreaza task_uri dupa alegerile de mai sus
# --- SIDEBAR: filtre (client-side) ---
st.sidebar.header("Filtre")
limbaje_disponibile = sorted({t["limbaj"] for t in task_uri})
limbaj_ales = st.sidebar.selectbox("Limbaj", ["Toate"] + limbaje_disponibile)
doar_nerezolvate = st.sidebar.checkbox("Doar nerezolvate", value=False)

task_uri_filtrate = task_uri
if limbaj_ales != "Toate":
    task_uri_filtrate = [t for t in task_uri_filtrate if t["limbaj"] == limbaj_ales]
if doar_nerezolvate:
    task_uri_filtrate = [t for t in task_uri_filtrate if not t["rezolvat"]]

st.caption(f"{len(task_uri_filtrate)} din {len(task_uri)} task-uri afisate")


# TODO: un "rand de card" pentru fiecare task
#   - st.container(border=True) cu 4 coloane: info, stare, rezolva, sterge
#   - info: titlu (markdown) + limbaj/dificultate/recompensa (caption)
#   - stare: st.success daca rezolvat, st.warning daca nu
# --- LISTA, ca randuri de card (nu st.dataframe - avem nevoie de butoane) ---
for t in task_uri_filtrate:
    with st.container(border=True):
        c_info, c_stare, c_rezolva, c_sterge = st.columns([4, 2, 1, 1])

        with c_info:
            st.markdown(f"**{t['titlu']}**")
            st.caption(f"{t['limbaj']} · {t['dificultate']} · {t['recompensa']:.0f} RON")

        with c_stare:
            if t["rezolvat"]:
                st.success("rezolvat", icon="✅")
            else:
                st.warning("in asteptare", icon="⏳")

        with c_rezolva:
            # TODO: butonul apare doar cat timp task-ul NU e rezolvat
            #   - la click: api("PUT", f"/task-uri/{t['id']}/rezolva")
            #   - daca ok: st.rerun() - reincarca pagina, ca sa vezi
            #     imediat starea noua (fara rerun, butonul ar ramane
            #     vizibil desi task-ul tocmai s-a rezolvat)
            #   - daca nu: st.error(rezultat)
            if not t["rezolvat"]:
                if st.button("Rezolva", key=f"rezolva_{t['id']}"):
                    ok, rezultat = api("PUT", f"/task-uri/{t['id']}/rezolva")
                    if ok:
                        st.rerun()
                    else:
                        st.error(rezultat)

        with c_sterge:
            # TODO: la click pe Sterge
            #   - api("DELETE", f"/task-uri/{t['id']}")
            #   - daca ok: st.rerun() - task-ul disparut nu mai trebuie
            #     sa apara in lista redesenata
            #   - daca nu: st.error(rezultat)
            if st.button("Sterge", key=f"sterge_{t['id']}"):
                ok, rezultat = api("DELETE", f"/task-uri/{t['id']}")
                if ok:
                    st.rerun()
                else:
                    st.error(rezultat)