import re
import time
import tracemalloc

# Funcție care transformă formula FNC (scrisă ca text) într-o listă de clauze
def citeste_fnc(text_intrare):
    # Înlocuim simbolul '∨' cu 'v' pentru a fi uniform
    text_intrare = text_intrare.replace('∨', 'v')

    clauze = []
    for clauza in text_intrare.strip().split("^"):
        litere = clauza.strip().replace("(", "").replace(")", "").split("v")
        clauze.append(set(litera.strip() for litera in litere))
    return clauze


# Verifică dacă o clauză conține un singur literal
def este_unitara(clauza):
    return len(clauza) == 1


# DPLL
def dpll(clauze, atribuire={}):
    if not clauze:  # Nu mai avem clauze — formula este satisfiabilă
        return True, atribuire

    if any(len(clauza) == 0 for clauza in clauze):  # Clauză vidă — formula nu este satisfiabilă
        return False, None

    # Propagare unități (dacă găsim o clauză cu un singur literal)
    for clauza in clauze:
        if este_unitara(clauza):
            literal = next(iter(clauza))
            return dpll(propagare_unitara(clauze, literal), {**atribuire, literal: True})

    # Alegem un literal oarecare (prima clauză, primul literal)
    literal = next(iter(next(iter(clauze))))

    # Încercăm cu literalul considerat adevărat
    rezultat, atrib_noua = dpll(propagare_unitara(clauze, literal), {**atribuire, literal: True})
    if rezultat:
        return True, atrib_noua

    # Dacă nu merge, încercăm cu opusul literalului
    literal_negat = neaga_literal(literal)
    return dpll(propagare_unitara(clauze, literal_negat), {**atribuire, literal_negat: True})


# DP
def dp(clauze):
    while True:
        # Eliminăm tautologiile (literal + negația lui în aceeași clauză)
        clauze = [c for c in clauze if len(c) != 0 and not any(neaga_literal(l) in c for l in c)]
        if not clauze:
            return True

        unitare = [c for c in clauze if len(c) == 1]
        if not unitare:
            break

        for unit in unitare:
            literal = next(iter(unit))
            clauze = propagare_unitara(clauze, literal)

    return not any(len(c) == 0 for c in clauze)


# Rezoluție
def rezolutie(clauze):
    clauze = list(map(frozenset, clauze))  # Transformă clauzele inițiale în frozenset-uri
    noi = set()

    while True:
        for i, ci in enumerate(clauze):
            for j, cj in enumerate(clauze):
                if i >= j:
                    continue
                rezolvate = rezolva(set(ci), set(cj))  # Transformăm înapoi în seturi pentru procesare
                for cl in rezolvate:
                    if len(cl) == 0:
                        return False
                    noi.add(frozenset(cl))
        if noi.issubset(set(clauze)):
            return True
        clauze.extend(noi - set(clauze))  # Adăugăm doar cele noi


# Aplică regula de rezoluție pe două clauze
def rezolva(c1, c2):
    rezultate = []
    for lit in c1:
        if neaga_literal(lit) in c2:
            noua_clauza = (c1 - {lit}) | (c2 - {neaga_literal(lit)})
            rezultate.append(noua_clauza)
    return rezultate


# Elimină literalul opus din toate clauzele, dacă am presupus că literalul e adevărat
def propagare_unitara(clauze, literal):
    clauze_noi = []
    for clauza in clauze:
        if literal in clauza:
            continue  # Clauza deja satisfăcută
        noua_clauza = clauza - {neaga_literal(literal)}
        clauze_noi.append(noua_clauza)
    return clauze_noi


# Negarea unui literal (ex: A → ~A, ~B → B)
def neaga_literal(literal):
    return literal[1:] if literal.startswith("~") else "~" + literal


# Verifică dacă formula este validă (valabilă pentru orice atribuire)
def este_valida(clauze):
    negata = [set(neaga_literal(l) for l in clauza) for clauza in clauze]
    return not dpll(negata)[0]



# Funcție pentru validarea intrării utilizatorului
def citire_valida():
    while True:
        formula = input("Introdu formula FNC (ex: (A v B) ^ (~A v C)): ").strip()
        if re.match(r'^[a-zA-Z~()^v∨\s]+$', formula) and ('v' in formula or '∨' in formula) and '^' in formula:
            return formula
        else:
            print("Formula introdusă nu este validă. Te rog să introduci o formulă corectă în format FNC.")


# Funcție pentru citirea formulei din fișier
def citire_din_fisier(nume_fisier):
    try:
        with open(nume_fisier, 'r') as f:
            formula = f.read().strip()
        return formula
    except FileNotFoundError:
        print(f"Fișierul {nume_fisier} nu a fost găsit.")
        return None

def aplica_metoda(metoda, clauze):
    tracemalloc.start()
    timp_inceput = time.perf_counter()

    if metoda == "DPLL":
        satisfiabila, _ = dpll(clauze)
    elif metoda == "DP":
        satisfiabila = dp(clauze)
    elif metoda == "Rezolutie":
        satisfiabila = rezolutie(clauze)
    else:
        return {"rezultat": "Metodă invalidă", "timp (ms)": 0, "memorie (KB)": 0}

    timp_final = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    timp_ms = round((timp_final - timp_inceput) * 1000, 4)
    memorie_kb = round(peak / 1024, 4)

    rezultat = "Satisfiabilă" if satisfiabila else "Nesatisfiabilă"

    return {
        "rezultat": rezultat,
        "timp (ms)": timp_ms,
        "memorie (KB)": memorie_kb
    }

if __name__ == "__main__":
    alegere = input("Vrei să citești formula dintr-un fișier? (da/nu): ").strip().lower()

    if alegere == "da":
        nume_fisier = input("Introdu numele fișierului: ").strip()
        formula = citire_din_fisier(nume_fisier)
        if not formula:
            print("Fișierul nu a fost găsit sau este gol.")
            exit()
        clauze = citeste_fnc(formula)
        rezultate = []
        for metoda in ["DP", "DPLL", "Rezolutie"]:
            rezultat = aplica_metoda(metoda, clauze)
            rezultate.append((metoda, rezultat))

        satisfiabila = any(rez["rezultat"] == "Satisfiabilă" for _, rez in rezultate)
        mesaj = "Formula este satisfiabilă." if satisfiabila else "Formula este nesatisfiabilă."
        print(f"\n{mesaj}\n")

        # Afișare tabel
        print("\nMetoda     | Timpul (ms) | Memorie (KB)")
        print("----------------------------------------")
        for metoda, rez in rezultate:
            print(f"{metoda:<10} | {rez['timp (ms)']:<11} | {rez['memorie (KB)']}")
        print("----------------------------------------")

    elif alegere == "nu":
        formula = citire_valida()
        clauze = citeste_fnc(formula)

        print("Alege metoda:\n1. DPLL\n2. DP\n3. Rezoluție")
        optiune = input("Număr metodă: ").strip()

        metode_map = {"1": "DPLL", "2": "DP", "3": "Rezolutie"}
        metoda = metode_map.get(optiune)

        if not metoda:
            print("Metodă invalidă.")
            exit()

        rezultat = aplica_metoda(metoda, clauze)
        print(f"\nRezultat: {rezultat['rezultat']}")
        print(f"Timp de execuție: {rezultat['timp (ms)']} ms")
        print(f"Memorie utilizată: {rezultat['memorie (KB)']} KB")

    else:
        print("Eroare. Încearcă din nou.")
