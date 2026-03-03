from nfa import *


def epsilon_closure(states) -> set[State]:
    '''Calcule la fermeture epsilon de l'ensemble d'états (states)'''   
    stack = list(states)  # utilise une pile pour parcourir les états à traiter
    closure = set(states)  # commence par inclure l'ensemble initial d'états
    while stack:  # tant que la pile n'est pas vide
        state = stack.pop()  # récupère le dernier état ajouté à la pile
        if None in state.transitions:  # vérifie si l'état courant possède une transition epsilon
            for next_state in state.transitions[None]:  # itère sur les états accessibles par epsilon
                if next_state not in closure:    # si l'état n'a pas encore été visité
                    closure.add(next_state)      # ajoute l'état à la fermeture epsilon
                    stack.append(next_state)     # ajoute l'état à la pile pour traitement ultérieur
    return closure  # retourne l'ensemble complet des états accessibles par transitions epsilon


def move(states, symbol) -> set[State]:
    """
    Calcule l'ensemble des états accessibles depuis les états dans 'states' en consommant le symbole 'symbol'.
    """
    result = set()
    for state in states:
        if symbol in state.transitions:
            for next_state in state.transitions[symbol]:
                result.add(next_state)
    return result

def accepts(nfa, string) -> bool:
    """
    Teste si l'AFN 'nfa' accepte la chaîne 'string'.
    On utilise l'epsilon closure pour gérer les transitions sans consommation.
    """
    current_states = epsilon_closure({nfa.start})
    for char in string:
        next_states = move(current_states, char)
        current_states = epsilon_closure(next_states)
    return nfa.finish in current_states



if __name__ == '__main__':

    def reinit():
        print("\n────────────────────────────")
        State._next_id = 0 # réinitialisation pour les prochains exemples


    reinit()
    print("# Exemple 1 : Un état isolé")
    a = State()
    closure1 = epsilon_closure({a})
    print("Fermeture epsilon de {a} :", {s.id for s in closure1})
    # Attendu : {0}


    reinit()
    print("# Exemple 2 : A →ε→ B (une transition epsilon directe)")
    a = State()
    b = State()
    a.add_transition(None, b)
    closure2 = epsilon_closure({a})
    print("Fermeture epsilon de {A} :", {s.id for s in closure2})
    # Attendu : {0, 1} (0 = A, 1 = B)


    reinit()
    print("# Exemple 3 : Chaîne A →ε→ B →ε→ C    (une chaîne de transitions epsilon)")
    # TODO: compléter cet exemple


    reinit()
    print("# Exemple 4 : Branching via epsilon (A → {B, C} et C →ε→ D)")
    # TODO: compléter cet exemple


    reinit()
    print("# Exemple 5 : Epsilon avec boucle (cycle)")
    # TODO: compléter cet exemple

    