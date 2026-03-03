class State:
    '''Un état d un AFN avec un identifiant séquentiel lisible.'''
    _next_id = 0 # attribut de classe servant de compteur d'ID
    def __init__(self):
        # transitions : dictionnaire { symbole (None pour epsilon): [états cibles] }
        self.transitions = {}
        # affectation d'un identifiant unique et lisible à chaque état créé
        self.id = State._next_id
        State._next_id += 1
    def add_transition(self, symbol, state):
        '''ajoute une transition vers state avec le symbole (None pour epsilon)
        .'''
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]
    def __str__(self):
        lst = []
        for symbole, states in self.transitions.items():
            s_symbole = symbole if symbole is not None else 'ε'
            ids = [s.id for s in states]
            lst.append(f"{s_symbole} -> {ids}")
        return f"State({self.id}): " + ", ".join(lst)
class NFA:
    '''Un AFN qui posséde un état initial et un état final.'''
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
    def display(self):
        '''affichage simple de l AFN par parcours en profondeur.'''
        visited = set()
        def dfs(state):
            if state in visited:
                return
            visited.add(state)
            print(state)
            for nexts in state.transitions.values():
                for s in nexts:
                    dfs(s) # récursif
        dfs(self.start)



# # Création d'un AFN simple pour le symbole 'a'
# start = State()
# finish = State()
# start.add_transition('a', finish)
# nfa_symbol_a = NFA(start, finish)
# nfa_symbol_a.display()


#////////////////////////////////////////////////
def symbol(sym)-> NFA:
    start = State()
    finish = State()
    start.add_transition(str(sym), finish)
    return NFA(start, finish)

def concat(nfa1, nfa2)-> NFA:
    start = nfa1.start
    finish = nfa2.finish
    start.add_transition(None, finish)
    return NFA(start, finish)

def union(nfa1, nfa2)-> NFA:
    new_start = State()
    new_finish = State()
    new_start.add_transition(None, nfa1.start)
    new_start.add_transition(None, nfa2.start)
    nfa1.finish.add_transition(None, new_finish)
    nfa2.finsh.add_transistion(None, new_finish)
    return NFA(new_start, new_finish)

def star(nfa)-> NFA:
    new_start = State()
    new_finish = State()
    new_start.add_transition(None, nfa.start)
    new_start.add_transition(None, nfa.finish)
    nfa.finish.add_transition(None, nfa.start)
    nfa.finish.add_transition(None, new_finish)
    return NFA(new_start, new_finish)




if __name__ == '__main__':
    from utils import export_html
    # Etape 1: construire un AFN pour la regex "a|b"
    nfa_a = symbol('a')
    nfa_b = symbol('b')
    nfa_union = union(nfa_a, nfa_b)
    # Etape 2: construire un AFN pour la regex "(a|b)*"
    nfa_star = star(nfa_union)
    # Afficher l'AFN
    print("AFN pour (a|b)* :")
    nfa_star.display()
    # Exporter l'AFN en HTML pour visualisation graphique
    export_html(nfa_star, nfa_name="(a|b)*", filename="nfa_star.html")