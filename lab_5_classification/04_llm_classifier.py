# LLM classifier: uses a large language model to classify messages.
import requests

from util import Classifier, load_corpus, cross_validate

API_KEY = "PUT YOUR OPENROUTER API KEY HERE"


class LLMClassifier(Classifier):
    """Classifies messages by prompting a large language model."""

    def train(self, label: str, text: str) -> None:
        pass

    def end_training(self) -> None:
        pass

    def classify(self, text: str) -> str:
        # TODO: implement this method.
        # Use the OpenRouter API (same as in 00_hello_llms.py) to ask the LLM
        # whether the message is "ham" or "spam".
        # Your prompt should instruct the model to reply with ONLY "ham" or "spam".
        # Parse the response and return "ham" or "spam".

        return "ham"  # placeholder


if __name__ == "__main__":
    documents = load_corpus()
    cross_validate(LLMClassifier, documents, n_documents=5)  # evaluate on only 5 documents for speed and cost reasons
