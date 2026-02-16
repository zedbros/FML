import os
import re
import math
import unittest


from regex_lab import *

from searcher import Searcher


class RegexExercisesTest(unittest.TestCase):
    """
    Tests de soumission pour le laboratoire d'expressions régulières.
    """

    def setUp(self):
        # Remarque : assurez-vous que les fichiers "BleakHouse.txt" et "numbers.txt" existent dans le répertoire.
        self.bh_searcher = Searcher("BleakHouse.txt")
        self.num_searcher = Searcher("numbers.txt")

    def test_01_planets(self):
        results = self.bh_searcher.match_list(RegexExercises.planets())
        self.assertEqual(len(results), 44)

    def test_02_dashes(self):
        results = self.bh_searcher.match_list(RegexExercises.dashes())
        self.assertEqual(len(results), 2155)

    def test_03_quotes(self):
        results = self.bh_searcher.match_list(RegexExercises.quotes())
        self.assertEqual(len(results), 3219)

    def test_04_rain(self):
        results = self.bh_searcher.match_list(RegexExercises.rain())
        self.assertEqual(len(results), 41)

    def test_05_east(self):
        results = self.bh_searcher.match_list(RegexExercises.east())
        self.assertEqual(len(results), 20)

    def test_06_hyphenated(self):
        results = self.bh_searcher.match_list(RegexExercises.hyphenated())
        self.assertEqual(len(results), 2202)
        self.assertEqual(results[1620], [26589, 0, 14])

    def test_07_digits(self):
        results = self.num_searcher.match_list(RegexExercises.digits())
        self.assertEqual(results[0], [1, 0, 17], "Le premier résultat est incorrect")

    def test_08_ssn(self):
        results = self.num_searcher.match_list(RegexExercises.ssn())
        self.assertEqual(results[0], [2, 0, 17], "Le premier résultat est incorrect")

    def test_09_commaNumbers(self):
        results = self.num_searcher.match_list(RegexExercises.commaNumbers())
        self.assertEqual(len(results), 4, "Le nombre de résultats est incorrect: " + str(results))
        self.assertEqual(results[0], [3, 0, 17], "Le premier résultat est incorrect")
        self.assertEqual(results[1], [4, 0, 17], "Le deuxième résultat est incorrect")
        self.assertEqual(results[2], [5, 0, 17], "Le troisième résultat est incorrect")
        self.assertEqual(results[3], [6, 0, 17], "Le quatrième résultat est incorrect")

    def test_10_decimalNumbers(self):
        results = self.num_searcher.match_list(RegexExercises.decimalNumbers())
        self.assertEqual(len(results), 3, "Le nombre de résultats est incorrect: " + str(results))
        self.assertEqual(results[0], [9, 0, 17], "Le premier résultat est incorrect")
        self.assertEqual(results[1], [10, 0, 17], "Le deuxième résultat est incorrect")
        self.assertEqual(results[2], [11, 0, 17], "Le troisième résultat est incorrect")

    def test_11_realNumbers(self):
        results = self.num_searcher.match_list(RegexExercises.realNumbers())
        self.assertEqual(len(results), 9, "Le nombre de résultats est incorrect: " + str(results))
        self.assertEqual(results[0], [1, 0, 17], "Le premier résultat est incorrect")
        self.assertEqual(results[1], [9, 0, 17], "Le deuxième résultat est incorrect")
        self.assertEqual(results[2], [10, 0, 17], "Le troisième résultat est incorrect")
        self.assertEqual(results[3], [11, 0, 17], "Le quatrième résultat est incorrect")
        self.assertEqual(results[8], [17, 0, 17], "Le neuvième résultat est incorrect")


class Helper:
    """
    Classe d'aide pour debugger vos expressions régulières
    """

    def main():
        bh_searcher = Searcher("BleakHouse.txt")
        num_searcher = Searcher("numbers.txt")

        # Ajoutez vos tests à analyser ici, comme par exemple:
        bh_searcher.show_matches(RegexExercises.dashes())


# Code permettant d'exécuter le pilote ou les tests
if __name__ == '__main__':
    # Décommentez la ligne suivante pour vous aider à visualiser les résultats de vos expressions régulières
    # Helper.main()
    
    # Pour exécuter les tests unitaires avec l'option failfast, utilisez :
    unittest.main(failfast=True)
