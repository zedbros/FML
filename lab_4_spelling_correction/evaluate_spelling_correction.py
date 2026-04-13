from spelling_correction import correct_spelling

# on compte le nombre de mots correctement corrigés et le nombre total de mots
correct_count = 0
total_count = 0

with open('evaluation_corpus.tsv', 'r', encoding='utf-8') as file:
    next(file) # saute la première ligne (header)
    for line in file:            
        incorrect_word, correct_word = line.strip().split('\t')
        # passer le mot à corriger à notre fonction de correction
        correction = correct_spelling(incorrect_word)
        # vérifier si la correction proposée correspond exactement au mot correct
        is_correct = correct_word == correction
        print(f"mot à corriger: {incorrect_word.ljust(15)} mot juste: {correct_word.ljust(15)} notre correction: {correction.ljust(15)} correction correcte: {is_correct}")
        # incrémenter le compteur de mots correctement corrigés
        if is_correct:
            correct_count += 1
        total_count += 1

# l'accuracy est le nombre de mots correctement corrigés divisé par le nombre total de mots
accuracy = correct_count / total_count if total_count > 0 else 0
print(f"{'-'*80}\naccuracy: {accuracy:.2%}")
