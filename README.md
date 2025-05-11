# proiect-SAT
Rezolvarea Problemei de Satisfiabilitate prin Metode Logice și Algoritmice în Informatică

Acest proiect oferă o implementare simplificată a trei metode clasice de rezolvare a problemei SAT (satisfiabilitate booleană), scrise în Python:

- **DPLL** (Davis–Putnam–Logemann–Loveland)
- **DP** (Davis–Putnam)
- **Rezoluție**

Proiectul permite introducerea unei formule  în forma normală conjunctivă (FNC), procesarea acesteia și determinarea satisfiabilității prin metoda selectată.

---

## 📦 Ce conține

### `Problema_SAT.py`
- Verificare și validare a formulei FNC de la utilizator
- Parsare a formulei într-o structură internă de clauze
- Implementarea algoritmilor DPLL, DP și Rezoluție
- Interfață CLI prietenoasă pentru alegerea metodei de rezolvare
- Funcționalitate pentru citirea formulelor din fișier text

### `Manual_de_utilizare.txt`
- O prezentare a modului de utilizare a codului
- Tipurile de date acceptate
- Tipurile de date neacceptate

### `exemplu.txt`
- Un fișier demonstrativ care conține o formulă logică exprimată în forma normală conjunctivă (FNC), utilizat pentru testarea funcției de citire din fișier.
- Formatul este următorul: (A v B) ^ (~A v C) 
