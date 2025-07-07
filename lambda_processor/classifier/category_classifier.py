from .keywords import CATEGORY_KEYWORDS


class CategoryClassifier:
    """Simple keyword based classifier for news categories."""

    def __init__(self, keywords: dict | None = None) -> None:
        self.keywords = keywords or CATEGORY_KEYWORDS

    def classify(self, title: str, content: str) -> tuple[str, None]:
        """Return the best category name for the given text."""
        text = f"{title} {content}".lower()
        best_category = None
        best_score = 0
        for category, words in self.keywords.items():
            score = sum(1 for w in words if w in text)
            if score > best_score:
                best_category = category
                best_score = score
        if best_category is None or best_score == 0:
            return "Outros", None
        return best_category, None
