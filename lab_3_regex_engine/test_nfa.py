import unittest
from nfa import symbol, concat, union, star, NFA, State


class TestSymbol(unittest.TestCase):

    def setUp(self):
        # Réinitialiser le compteur d'ID pour éviter des interférences entre tests
        State._next_id = 0

    def test_symbol_transition_unique(self):
        # Test 1 : l'état de départ possède une transition labellisée par le symbole donné vers l'état final.
        nfa = symbol('a')
        self.assertIn('a', nfa.start.transitions, "La transition pour le symbole 'a' doit exister dans l'état de départ.")
        self.assertEqual(len(nfa.start.transitions['a']), 1, "Il doit y avoir une seule transition pour 'a'.")
        self.assertEqual(nfa.start.transitions['a'][0], nfa.finish, "La transition doit pointer vers l'état final.")

    def test_symbol_etats_distincts(self):
        # Test 2 : vérifier que l'état de départ et l'état final sont bien différents.
        nfa = symbol('x')
        self.assertNotEqual(nfa.start, nfa.finish, "Les états start et finish doivent être différents.")

    def test_symbol_pas_de_transition_sur_finish(self):
        # Test 3 : vérifier que l'état final n'a aucune transition.
        nfa = symbol('z')
        self.assertEqual(nfa.finish.transitions, {}, "L'état final ne doit posséder aucune transition.")


class TestConcat(unittest.TestCase):
    def setUp(self):
        State._next_id = 0

    def test_concat_transition_epsilon(self):
        # Test 1 : la concaténation doit ajouter une transition epsilon de nfa1.finish vers nfa2.start.
        nfa1 = symbol('a')
        nfa2 = symbol('b')
        nfa_concat = concat(nfa1, nfa2)
        self.assertIn(None, nfa1.finish.transitions, "Une transition epsilon doit être présente dans nfa1.finish.")
        self.assertEqual(nfa1.finish.transitions[None][0], nfa2.start, "La transition epsilon doit pointer vers nfa2.start.")

    def test_concat_etats_debut_fin(self):
        # Test 2 : l'AFN résultant doit avoir comme début nfa1.start et comme fin nfa2.finish.
        nfa1 = symbol('c')
        nfa2 = symbol('d')
        nfa_concat = concat(nfa1, nfa2)
        self.assertEqual(nfa_concat.start, nfa1.start, "L'état initial de l'AFN concaténé doit être celui de nfa1.")
        self.assertEqual(nfa_concat.finish, nfa2.finish, "L'état final de l'AFN concaténé doit être celui de nfa2.")

    def test_concat_pas_de_transition_supplémentaire(self):
        # Test 3 : vérifier que concat ne modifie pas les autres transitions des NFAs.
        nfa1 = symbol('e')
        nfa2 = symbol('f')
        # Avant concat, nfa2.finish ne possède aucune transition.
        self.assertEqual(nfa2.finish.transitions, {}, "Avant la concaténation, l'état final de nfa2 ne doit pas avoir de transitions.")
        concat(nfa1, nfa2)
        self.assertEqual(nfa2.finish.transitions, {}, "Après concat, nfa2.finish ne doit toujours pas avoir de transitions.")


class TestUnion(unittest.TestCase):
    def setUp(self):
        State._next_id = 0

    def test_union_start_transitions(self):
        # Test 1 : l'état de début de l'union doit posséder deux transitions epsilon, une vers nfa1.start et une vers nfa2.start.
        nfa1 = symbol('a')
        nfa2 = symbol('b')
        nfa_union = union(nfa1, nfa2)
        self.assertIn(None, nfa_union.start.transitions, "L'état de début de l'union doit avoir des transitions epsilon.")
        epsilon_transitions = nfa_union.start.transitions[None]
        self.assertEqual(len(epsilon_transitions), 2, "Il doit y avoir exactement 2 transitions epsilon depuis le nouvel état de début.")
        self.assertIn(nfa1.start, epsilon_transitions, "nfa1.start doit être accessible via une transition epsilon.")
        self.assertIn(nfa2.start, epsilon_transitions, "nfa2.start doit être accessible via une transition epsilon.")

    def test_union_finish_transitions(self):
        # Test 2 : les états finaux originaux doivent posséder une transition epsilon pointant vers le nouvel état final.
        nfa1 = symbol('x')
        nfa2 = symbol('y')
        nfa_union = union(nfa1, nfa2)
        self.assertIn(None, nfa1.finish.transitions, "nfa1.finish doit comporter une transition epsilon vers le nouvel état final.")
        self.assertIn(nfa_union.finish, nfa1.finish.transitions[None], "La transition epsilon de nfa1.finish doit pointer vers l'état final de l'union.")
        self.assertIn(None, nfa2.finish.transitions, "nfa2.finish doit comporter une transition epsilon vers le nouvel état final.")
        self.assertIn(nfa_union.finish, nfa2.finish.transitions[None], "La transition epsilon de nfa2.finish doit pointer vers l'état final de l'union.")

    def test_union_nouveaux_etats(self):
        # Test 3 : vérifier que union crée bien de nouveaux états pour le début et la fin et que ceux-ci sont distincts
        nfa1 = symbol('p')
        nfa2 = symbol('q')
        nfa_union = union(nfa1, nfa2)
        self.assertNotEqual(nfa_union.start, nfa1.start, "Le nouvel état de début doit être différent de nfa1.start.")
        self.assertNotEqual(nfa_union.start, nfa2.start, "Le nouvel état de début doit être différent de nfa2.start.")
        self.assertNotEqual(nfa_union.finish, nfa1.finish, "Le nouvel état final doit être différent de nfa1.finish.")
        self.assertNotEqual(nfa_union.finish, nfa2.finish, "Le nouvel état final doit être différent de nfa2.finish.")


class TestStar(unittest.TestCase):
    def setUp(self):
        State._next_id = 0

    def test_star_start_transitions(self):
        # Test 1 : l'état de début de l'AFN étoilé doit avoir une transition epsilon vers nfa.start et une vers le nouvel état final.
        nfa = symbol('a')
        nfa_star = star(nfa)
        self.assertIn(None, nfa_star.start.transitions, "L'état de début de l'AFN étoilé doit avoir au moins une transition epsilon.")
        transitions_start = nfa_star.start.transitions[None]
        self.assertEqual(len(transitions_start), 2, "L'état de début doit comporter exactement 2 transitions epsilon.")
        self.assertIn(nfa.start, transitions_start, "Il doit y avoir une transition epsilon de new_start vers nfa.start.")
        self.assertIn(nfa_star.finish, transitions_start, "Il doit y avoir une transition epsilon de new_start vers le nouvel état final.")

    def test_star_finish_transitions(self):
        # Test 2 : l'état final d'origine doit avoir une transition epsilon vers nfa.start et une vers le nouvel état final.
        nfa = symbol('b')
        nfa_star = star(nfa)
        self.assertIn(None, nfa.finish.transitions, "L'ancien état final doit avoir une transition epsilon.")
        transitions_finish = nfa.finish.transitions[None]
        self.assertEqual(len(transitions_finish), 2, "nfa.finish doit comporter exactement 2 transitions epsilon.")
        self.assertIn(nfa.start, transitions_finish, "nfa.finish doit avoir une transition epsilon vers nfa.start pour la répétition.")
        self.assertIn(nfa_star.finish, transitions_finish, "nfa.finish doit avoir une transition epsilon vers le nouvel état final.")

    def test_star_accepte_chaine_vide(self):
        # Test 3 : vérifier que l'AFN étoilé accepte la chaîne vide grâce à la transition directe new_start -> new_finish.
        nfa = symbol('c')
        nfa_star = star(nfa)
        transitions_start = nfa_star.start.transitions.get(None, [])
        # On vérifie que new_finish est accessible depuis new_start par epsilon (donc la chaîne vide est acceptée).
        self.assertIn(nfa_star.finish, transitions_start, "L'AFN étoilé doit accepter la chaîne vide via new_start -> new_finish.")


if __name__ == '__main__':
    unittest.main()
