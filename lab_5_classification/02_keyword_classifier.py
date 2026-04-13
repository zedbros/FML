# Keyword classifier: uses hand-curated positive/negative word lists.
from util import Classifier, load_corpus, cross_validate


def load_words(path):
    """Load a word list from a text file (one word per line)."""
    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


class KeywordClassifier(Classifier):
    """Classifies messages by counting positive (ham) and negative (spam) keyword matches."""

    def __init__(self):
        self.positive_words = load_words("02_positive_words.txt")
        self.negative_words = load_words("02_negative_words.txt")
        assert self.positive_words and self.negative_words, "Word lists must not be empty"

    def train(self, label: str, text: str) -> None:
        pass  # nothing to do here, we are not training anything

    def end_training(self) -> None:
        pass  # nothing to do here, we are not training anything

    def classify(self, text: str) -> str:
        # count the number of positive and negative words in the text
        words = text.lower().split()
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        # return "spam" if there are more negative words than positive words, otherwise "ham"
        return "spam" if neg_count > pos_count else "ham"


if __name__ == "__main__":
    documents = load_corpus()
    cross_validate(KeywordClassifier, documents)
