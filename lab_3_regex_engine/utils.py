import os
import webbrowser

def nfa_to_dot(nfa):
    '''
    Génère et retourne une chaîne DOT décrivant l'AFN.
    L'état final (finish) est dessiné avec une double bordure.
    Un noeud "init" sert de point d'entrée vers l'état initial.
    '''
    # Récupérer tous les états via un parcours en profondeur
    visited = set()
    states = []
    def dfs(state):
        if state in visited:
            return
        visited.add(state)
        states.append(state)
        for targets in state.transitions.values():
            for s in targets:
                dfs(s)
    dfs(nfa.start)

    dot_lines = []
    dot_lines.append('digraph NFA {')
    dot_lines.append('    rankdir=LR;')  # disposition de gauche à droite
    dot_lines.append('    node [fontname="Helvetica"];')
    # Noeud invisible pour représenter le départ
    dot_lines.append('    init [shape=point];')

    # Déclarer tous les états
    for state in states:
        if state == nfa.finish:
            dot_lines.append(f'    {state.id} [shape=doublecircle, label="{state.id}"];')
        else:
            dot_lines.append(f'    {state.id} [shape=circle, label="{state.id}"];')

    # Lien depuis le point initial vers l'état de départ de l'automate
    dot_lines.append(f'    init -> {nfa.start.id};')

    # Déclarer les transitions
    for state in states:
        for symbol, targets in state.transitions.items():
            label = symbol if symbol is not None else 'ε'
            for t in targets:
                dot_lines.append(f'    {state.id} -> {t.id} [label="{label}"];')
    dot_lines.append('}')
    return "\n".join(dot_lines)



def export_html(nfa, nfa_name="", filename="nfa.html"):
    '''
    Exporte l'AFN dans un fichier HTML qui utilise Viz.js pour afficher le graphe.
    Le fichier HTML inclut la bibliothèque Viz.js via CDN et un script qui transforme la chaîne DOT en SVG.
    '''
    dot_content = nfa_to_dot(nfa).replace("\n", "\\n")  # Échappe les retours à la ligne pour le JS

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Visualisation de l'AFN</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/full.render.js"></script>
    <style>
        #graph {{
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1><pre>{nfa_name}</pre></h1>
    <div id="graph">Chargement du graphe...</div>
    <script>
        // Chaîne DOT générée par l'AFN
        var dot = `{dot_content}`;
        var viz = new Viz();
        viz.renderSVGElement(dot)
           .then(function(element) {{
              var graphDiv = document.getElementById("graph");
              graphDiv.innerHTML = "";
              graphDiv.appendChild(element);
           }})
           .catch(error => {{
             console.error(error);
           }});
    </script>
</body>
</html>'''

    # Écrire le contenu HTML dans le fichier spécifié
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Fichier HTML généré : {filename}")

    file_abs_path = os.path.abspath(filename)  # Ensure it's an absolute path

    # Open the file in the default web browser
    webbrowser.open(f"file://{file_abs_path}")


