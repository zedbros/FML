# Random classifier: assigns a random label to each document.
import random

from util import Classifier, load_corpus, cross_validate


class RandomClassifier(Classifier):
    """A classifier that randomly assigns labels."""

    def __init__(self):  # this is a class constructor in Python
        self.labels = set()  # initialize an empty set of labels

    def train(self, label: str, text: str) -> None:
        self.labels.add(label)  # add the label to the set of labels seen during training

    def end_training(self) -> None:
        pass  # nothing to do here, we are not training anything, just collecting the labels

    def classify(self, text: str) -> str:
        return random.choice(sorted(self.labels))  # pick a random label from the set of labels seen during training


if __name__ == "__main__":
    documents = load_corpus()
    cross_validate(RandomClassifier, documents)
