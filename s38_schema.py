from enum import Enum
from pydantic import BaseModel, Field, ValidationError


# #############################################################
# PARTEA 1 - SCHEMA: ce inseamna un task "valid"
# #############################################################


# 1. Enum-uri  -  campul poate fi DOAR una din valorile listate
# -------------------------------------------------------------
# Fara Enum, `limbaj: str` ar accepta orice text ("Cobol", "asdf", "").
# Cu Enum, doar una din cele patru valori de mai jos trece validarea.
class Limbaj(str, Enum):
    PYTHON     = "Python"
    JAVASCRIPT = "JavaScript"
    GO         = "Go"
    RUST       = "Rust"


class Dificultate(str, Enum):
    USOR  = "usor"
    MEDIU = "mediu"
    GREU  = "greu"


# 2. TaskIn  -  schema propriu-zisa
# -------------------------------------------------------------
# Field(min_length=3)  -> titlul trebuie sa aiba macar 3 caractere.
# Field(gt=0)           -> recompensa trebuie sa fie STRICT pozitiva.
# limbaj / dificultate  -> valori limitate de Enum-urile de mai sus.
class TaskIn(BaseModel):
    titlu:       str = Field(min_length=3)
    limbaj:      Limbaj
    dificultate: Dificultate
    recompensa:  float = Field(gt=0)


# 3. O functie care iti spune DOAR daca datele sunt valide
# -------------------------------------------------------------
# Utila cand vrei sa verifici niste date FARA sa creezi inca nimic -
# exact ce facea /valideaza-task la sesiunea 37, dar acum fara server.
def valideaza(date_brute: dict):
    try:
        task = TaskIn.model_validate(date_brute)
        return {"valid": True, "task": task}
    except ValidationError as e:
        erori = [f"{'.'.join(str(p) for p in er['loc'])}: {er['msg']}" for er in e.errors()]
        return {"valid": False, "erori": erori}