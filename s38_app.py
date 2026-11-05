# =============================================================
# FastAPI  -  unim totul intr-un API real (Bounty Board)
# =============================================================
# s38_model.py salveaza (SQLAlchemy), s38_schema.py valideaza (Pydantic).
# Aici le punem impreuna in spatele rutelor FastAPI (s36).


from fastapi import FastAPI, HTTPException

import s38_model
from s38_model import SessionLocal, init_db
from s38_schema import TaskIn

# SessionLocal (definit in s38_model.py) e o fabrica de sesiuni, deja
# configurata cu engine-ul catre MySQL. Fiecare apel SessionLocal()
# creeaza o sesiune noua, iar `with SessionLocal() as s:` o deschide si
# o inchide automat la finalul blocului - acelasi tipar cu `with
# Session(engine) as s:` de la s30, doar ca engine-ul nu se mai repeta
# la fiecare ruta, fiind deja legat de fabrica.


init_db()   # la pornire: cream tabela daca nu exista + punem datele

app = FastAPI(title="Bounty Board", version="0.3.0 (s38, MySQL)")


# #############################################################
# RUTELE - subtiri: deschid o sesiune, cheama functia din s38_model.py.
# Ruta si semnatura sunt recap din s37; TODO-urile marcheaza doar
# interiorul (nou).
# #############################################################


@app.get("/task-uri")
def lista_task_uri():
    # TODO - doar interiorul:
    #   - with SessionLocal() as s: ...
    #   - s38_model.toate_task_urile(s), transformat in lista de dict-uri
    with SessionLocal() as s:
        # Varianta 1
        # l_taskuri = []
        # for t in s38_model.toate_task_urile(s):
        #     l_taskuri.append({"id": t.id, "titlu": t.titlu, "limbaj": t.limbaj,
        #                       "dificultate": t.dificultate, "recompensa": t.recompensa, "rezolvat": t.rezolvat})
        #
        # return l_taskuri

        # Varianta 2
        return [{"id": t.id, "titlu": t.titlu, "limbaj": t.limbaj, "dificultate": t.dificultate, "recompensa": t.recompensa, "rezolvat": t.rezolvat}
                for t in s38_model.toate_task_urile(s)]

@app.get("/task-uri/{task_id}")
def un_task(task_id: int):
    # TODO - doar interiorul:
    #   - s38_model.un_task(s, task_id), daca None -> HTTPException(404)
    #   - altfel intoarce dict-ul
    with SessionLocal() as s:
        t = s38_model.un_task(s, task_id)
        if t is None:
            raise HTTPException(status_code=404, detail=f"Task-ul {task_id} nu exista")
        return { "id": t.id, "titlu": t.titlu, "limbaj": t.limbaj, "dificultate": t.dificultate, "recompensa": t.recompensa, "rezolvat": t.rezolvat }


# data: TaskIn -> FastAPI valideaza body-ul CU SCHEMA din s38_schema.py
# inainte sa ruleze functia; abia apoi salvam prin s38_model.adauga_task().
@app.post("/task-uri", status_code=201)
def adauga_task(data: TaskIn):
    # TODO - doar interiorul:
    #   - s38_model.adauga_task(s, data.titlu, data.limbaj, data.dificultate, data.recompensa)
    #   - intoarce dict-ul
    with SessionLocal() as s:
        t = s38_model.adauga_task(s, data.titlu, data.limbaj, data.dificultate, data.recompensa)
        return { "id": t.id, "titlu": t.titlu, "limbaj": t.limbaj, "dificultate": t.dificultate, "recompensa": t.recompensa, "rezolvat": t.rezolvat }


@app.put("/task-uri/{task_id}/rezolva")
def rezolva_task(task_id: int):
    # TODO - doar interiorul:
    #   - s38_model.marcheaza_rezolvat(s, task_id), daca None -> HTTPException(404)
    #   - altfel {"id": t.id, "rezolvat": t.rezolvat}
    with SessionLocal() as s:
        t = s38_model.marcheaza_rezolvat(s, task_id)
        if t is None:
            raise HTTPException(status_code=404, detail=f"Task-ul {task_id} nu exista")
        return { "id": t.id, "titlu": t.titlu }


@app.delete("/task-uri/{task_id}")
def sterge_task(task_id: int):
    # TODO - doar interiorul:
    #   - s38_model.sterge_task(s, task_id), daca not gasit -> HTTPException(404)
    #   - altfel {"sters": task_id}
    with SessionLocal() as s:
        t = s38_model.sterge_task(s, task_id)
        if t is None:
            raise HTTPException(status_code=404, detail=f"Task-ul {task_id} nu exista")
        return {"sters": task_id}


@app.get("/recompensa-disponibila")
def recompensa_disponibila():
    # TODO - doar interiorul:
    #   - s38_model.recompensa_disponibila(s)
    #   - {"recompensa_totala": ...}
    with SessionLocal() as s:
        return {"recompensa_totala": s38_model.recompensa_disponibila(s)}


# Rulare: python3 s38_app.py (din interiorul session38/) -> /docs
# Test: POST /task-uri cu recompensa negativa -> 422, inainte sa atinga DB.
import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000)


# =============================================================
# RECAP
# =============================================================
# - import s38_model (modulul intreg), nu from ... import, ca sa nu se
#   ciocneasca numele functiilor cu numele rutelor (un_task, sterge_task).
# - POST invalid nu ajunge la s38_model - 422 vine inainte de sesiunea DB.
# - In s39: Depends(get_db) in loc de with SessionLocal() repetat, +
#   middleware + CORS.
# =============================================================