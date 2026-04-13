# Shared utilities: Classifier interface, corpus loading, and cross-validation.
import csv
import random
from abc import ABC, abstractmethod


class Classifier(ABC):
    """Base class for all text classifiers."""

    @abstractmethod
    def train(self, label: str, text: str) -> None:
        pass

    @abstractmethod
    def end_training(self) -> None:
        pass

    @abstractmethod
    def classify(self, text: str) -> str:
        pass


def load_corpus(path="email_data.csv"):
    """Load the email corpus from a CSV file.
    Returns a list of (label, text) tuples.
    """
    documents = []
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            documents.append((row[0], row[1]))
    return documents


def cross_validate(classifier_class, documents, n_documents=None, print_wrongly_classified=False):
    """Run 10-fold cross-validation on a classifier and print metrics.

    If n_documents is set, evaluate on only that many documents (single split)
    instead of full cross-validation. Useful for slow classifiers (e.g. LLM).
    """
    random.seed(42)
    shuffled = documents.copy()
    random.shuffle(shuffled)

    all_true = []
    all_pred = []

    if n_documents is not None:
        test_docs = shuffled[:n_documents]
        train_docs = shuffled[n_documents:]

        clf = classifier_class()
        for label, text in train_docs:
            clf.train(label, text)
        clf.end_training()

        for label, text in test_docs:
            all_true.append(label)
            predicted_label = clf.classify(text)
            all_pred.append(predicted_label)
            if print_wrongly_classified and label != predicted_label:
                print(f"Wrongly classified: {text} (expected {label}, got {predicted_label})")

        _print_metrics(all_true, all_pred)
        return

    n_folds = 10
    fold_size = len(shuffled) // n_folds

    for i in range(n_folds):
        test_start = i * fold_size
        test_end = (i + 1) * fold_size if i < n_folds - 1 else len(shuffled)
        test_fold = shuffled[test_start:test_end]
        train_fold = shuffled[:test_start] + shuffled[test_end:]

        clf = classifier_class()
        for label, text in train_fold:
            clf.train(label, text)
        clf.end_training()

        for label, text in test_fold:
            all_true.append(label)
            predicted_label = clf.classify(text)
            all_pred.append(predicted_label)
            if print_wrongly_classified and label != predicted_label:
                print(f"Wrongly classified: {text} (expected {label}, got {predicted_label})")

    _print_metrics(all_true, all_pred)


def _print_metrics(true_labels, pred_labels):
    """Compute and print classification metrics."""
    labels = sorted(set(true_labels) | set(pred_labels))

    class_metrics = {}
    for label in labels:
        tp = sum(1 for t, p in zip(true_labels, pred_labels) if t == label and p == label)
        fp = sum(1 for t, p in zip(true_labels, pred_labels) if t != label and p == label)
        fn = sum(1 for t, p in zip(true_labels, pred_labels) if t == label and p != label)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        class_metrics[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": tp + fn,
        }

    correct = sum(1 for t, p in zip(true_labels, pred_labels) if t == p)
    accuracy = correct / len(true_labels)

    macro_precision = sum(m["precision"] for m in class_metrics.values()) / len(class_metrics)
    macro_recall = sum(m["recall"] for m in class_metrics.values()) / len(class_metrics)
    macro_f1 = sum(m["f1"] for m in class_metrics.values()) / len(class_metrics)

    print(f"\n--- Results ({len(true_labels)} documents) ---")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {macro_precision:.4f}  (macro average)")
    print(f"Recall:    {macro_recall:.4f}  (macro average)")
    print(f"F1:        {macro_f1:.4f}  (macro average)")

    print(f"\nPer-class Results:")
    print(f"{'Class':<10} {'Precision':<12} {'Recall':<12} {'F1':<12} {'Support'}")
    print("-" * 58)
    for label in labels:
        m = class_metrics[label]
        print(f"{label:<10} {m['precision']:<12.4f} {m['recall']:<12.4f} {m['f1']:<12.4f} {m['support']}")
