Sesiunea 38-39 — Bounty Board
La s37 aveam un API FastAPI care mergea, dar tot ce salva traia intr-o lista Python — la restart, disparea. Azi ii punem o baza de date reala si o interfata. Patru bucati, in ordinea in care le construim.

1. Schema bazei de date — s38_model.py
Aici definim cum arata un task ca tabela, si cum se salveaza. Fara FastAPI, fara Pydantic — doar SQLAlchemy.

[ ] clasa Task(Base) — coloanele: id, titlu, limbaj, dificultate, recompensa, rezolvat
[ ] adauga_task
[ ] toate_task_urile
[ ] un_task
[ ] marcheaza_rezolvat
[ ] sterge_task
[ ] recompensa_disponibila
[ ] testat din consola Python, fara server — inchid, redeschid, datele sunt tot acolo
2. Schema Pydantic — s38_schema.py
Limbaj, Dificultate, TaskIn sunt exact ce am scris la s37 — nu le rescriem, doar le aducem aici ca sa le importam in pasul urmator.

[ ] recap rapid: Limbaj, Dificultate (Enum)
[ ] recap rapid: TaskIn (schema de validare)
[ ] importat TaskIn in s38_app.py
3. FastAPI — conectarea — s38_app.py
Rutele in sine (decorator, semnatura) raman ca la s37. Ce schimbam e interiorul: in loc sa umblam in lista din memorie, deschidem o sesiune si chemam functia potrivita din s38_model.py.

[ ] GET /task-uri
[ ] GET /task-uri/{id}
[ ] POST /task-uri
[ ] PUT /task-uri/{id}/rezolva
[ ] DELETE /task-uri/{id}
[ ] GET /recompensa-disponibila
[ ] test: POST, apoi restart server — datele raman (asta e diferenta fata de s37)
4. Streamlit — interfata — s38_ui.py, s38_pages/, comun.py
Un client vizual pentru API-ul de mai sus. Widget-urile individuale le stim de la s22, ce e nou e organizarea pe pagini.

[ ] comun.py — functiile care vorbesc cu API-ul
[ ] s38_pages/lista.py
[ ] s38_pages/adauga.py
[ ] s38_pages/dashboard.py
[ ] s38_ui.py — st.Page + st.navigation
[ ] test complet: MySQL pornit → s38_app.py → streamlit run s38_ui.py, adaug un task din UI, il vad in /docs