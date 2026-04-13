import re
import sys
import pandas as pd
from datasets import load_dataset # pip install datasets
from collections import defaultdict

STOP_AFTER_N_ARTICLES = 2000
MIN_WORD_FREQUENCY = 3

# see https://huggingface.co/datasets/wikimedia/wikipedia
dataset = load_dataset("wikimedia/wikipedia", "20231101.fr", split='train', streaming=True)

word_freq = defaultdict(int)

for i, sample in enumerate(dataset):

    text = sample.get('text', '')

    words = re.findall(r'\w+', text.lower())  # ah tiens, une regex!

    for word in words:
        word_freq[word] += 1
    
    if (i + 1) % 1000 == 0:
        print(f"Processed {i + 1} articles")

    if i == STOP_AFTER_N_ARTICLES:
        break


filtered_word_freq = {word: freq for word, freq in word_freq.items() if freq >= MIN_WORD_FREQUENCY}

df = pd.DataFrame(list(filtered_word_freq.items()), columns=['Word', 'Frequency'])
df.sort_values(by='Frequency', ascending=False, inplace=True)
df.to_csv(f'word_frequencies_{STOP_AFTER_N_ARTICLES}.tsv', sep='\t', index=False)
print("Done :-)")

# if on google colab
if 'google.colab' in sys.modules:
    print("Now let's download the file")
    from google.colab import files
    files.download(f'word_frequencies_{STOP_AFTER_N_ARTICLES}.tsv')
