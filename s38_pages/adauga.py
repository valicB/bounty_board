# =============================================================
# PAGINA  -  Adauga task
# =============================================================
# st.form (s22) trimite toate campurile O SINGURA DATA, la submit.
# O eroare 422 apare aici ca mesaj clar, camp cu camp - formatat de api().
# =============================================================

import streamlit as st

from comun import api

st.title("➕ Adauga task")

# TODO: formularul de adaugare
#   - titlu: st.text_input
#   - limbaj + dificultate: cate un st.selectbox, pe aceeasi linie (st.columns)
#   - recompensa: st.number_input
#   - buton de submit: st.form_submit_button
with st.form("form_task_nou", clear_on_submit=True):
    titlu = st.text_input("Titlu", placeholder="ex: Fix bug la login")

    c1, c2 = st.columns(2)
    limbaj = c1.selectbox("Limbaj", ["Python", "JavaScript", "Go", "Rust"])
    dificultate = c2.selectbox("Dificultate", ["usor", "mediu", "greu"])

    recompensa = st.number_input("Recompensa (RON)", min_value=0.0, step=10.0, value=50.0)

    trimis = st.form_submit_button("Creeaza task", type="primary")

# TODO: cand formularul e trimis (trimis == True)
#   - trimite campurile completate mai sus catre API, ca JSON:
#       api("POST", "/task-uri", json={"titlu": titlu, "limbaj": limbaj,
#           "dificultate": dificultate, "recompensa": recompensa})
#   - daca ok: rezultat e task-ul creat, asa cum l-a intors serverul -
#     arata un mesaj de succes cu rezultat['titlu'] si rezultat['id'],
#     apoi st.balloons() (formularul se goleste singur, clear_on_submit=True)
#   - daca nu: st.error(rezultat) - mesajul vine deja formatat de api(),
#     camp cu camp
if trimis:
    ok, rezultat = api("POST", "/task-uri", json={
        "titlu": titlu,
        "limbaj": limbaj,
        "dificultate": dificultate,
        "recompensa": recompensa,
    })
    if ok:
        st.success(f"Task creat: \"{rezultat['titlu']}\" (id {rezultat['id']})")
        st.balloons()
    else:
        # ex: "titlu: String should have at least 3 characters" - regula
        # Field(min_length=3) din s38_schema.py, tradusa pentru formular.
        st.error(rezultat)