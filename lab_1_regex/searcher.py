import os
import re
import math

class Searcher:
    """
    La classe Searcher facilite l'apprentissage des expressions régulières en Python
    en traitant des fichiers texte et en indiquant quelles parties du fichier correspondent
    à une expression régulière donnée.
    """

    def __init__(self, filename):
        """
        Crée un objet de recherche pour un fichier particulier.
        
        @param filename Le nom du fichier
        @raises FileNotFoundError Si le fichier n'existe pas
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Le fichier {filename} n'existe pas.")
        self.filename = filename

    def show_matches(self, regex, show_line_numbers=True):
        """
        Affiche les lignes du fichier qui correspondent à l'expression régulière fournie,
        ainsi que des marqueurs indiquant quelle portion de la ligne a été trouvée.
        
        @param regex Chaîne contenant une expression régulière Python
        @param show_line_numbers Si vrai, les numéros de ligne seront inclus dans la sortie
        """
        pattern = re.compile(regex)
        total_matches = 0
        line_matches = 0

        with open(self.filename, encoding="utf-8") as f:
            lines = f.readlines()

        for line_idx, curLine in enumerate(lines):
            curLineStripped = curLine.rstrip('\n')
            matches = list(pattern.finditer(curLineStripped))
            if matches:
                total_matches += len(matches)
                line_matches += 1
                if show_line_numbers:
                    # Affiche le numéro de ligne et la ligne correspondante
                    print(f"{line_idx+1}: {curLineStripped}")
                    # Calculer le nombre de chiffres du numéro de ligne
                    digits = int(math.log10(line_idx+1)) + 1 if line_idx+1 > 0 else 1
                    # Imprimer des espaces pour compenser le numéro et ": "
                    print(" " * (digits + 2), end="")
                else:
                    print(curLineStripped)
                last_end = 0
                # Pour chaque match, affiche un marqueur sous la correspondance
                for m in matches:
                    start, end = m.start(), m.end()
                    # Affiche les espaces entre le dernier marqueur et le début du match
                    print(" " * (start - last_end), end="")
                    # Affiche le premier marqueur '^'
                    print("^", end="")
                    span = end - start
                    if span > 1:
                        # Affiche des tirets pour la longueur du match moins deux
                        dash_count = span - 2
                        if dash_count > 0:
                            print("-" * dash_count, end="")
                        # Si le match contient plus d'un caractère, affiche '^'
                        print("^", end="")
                    last_end = end
                print("\n")
        print(f"{total_matches} correspondances au total, {line_matches}/{len(lines)} lignes matchent.")

    def match_list(self, regex):
        """
        Retourne une liste de listes de trois éléments, où chaque liste correspond
        à une région du fichier qui correspond à l'expression régulière fournie.
        Les trois entrées de chaque liste sont : 
          1) le numéro de la ligne de la correspondance,
          2) la position de départ dans la ligne,
          3) et la position de fin dans la ligne.
        
        @param regex Chaîne contenant une expression régulière Python
        @return Liste de listes décrivant les correspondances
        """
        matches = []
        pattern = re.compile(regex)
        with open(self.filename, encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.rstrip('\n')
                for m in pattern.finditer(line):
                    matches.append([line_num, m.start(), m.end()])
        return matches


