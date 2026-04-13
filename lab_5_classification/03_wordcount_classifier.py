# Word count classifier: uses word frequencies from training data.
from collections import defaultdict

from util import Classifier, load_corpus, cross_validate


class WordCountClassifier(Classifier):
    """Classifies messages based on word frequencies observed during training."""

    def __init__(self):
        self.word_counts = defaultdict(lambda: defaultdict(int))

    def train(self, label: str, text: str) -> None:
        for word in text.lower().split():
            if len(word) > 3:
                self.word_counts[label][word] += 1

    def end_training(self) -> None:
        pass

    def classify(self, text: str) -> str:
        words = [w.lower() for w in text.split() if len(w) > 3]

        # TODO: for each label, compute a score by summing the frequencies
        # of the words in the message. Return the label with the highest score.

        return "ham"  # placeholder


if __name__ == "__main__":
    documents = load_corpus()
    cross_validate(WordCountClassifier, documents)
