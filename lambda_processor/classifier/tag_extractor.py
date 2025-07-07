from collections import Counter
from ..utils.text_processor import tokenize


class TagExtractor:
    def extract(self, text: str, limit: int = 10):
        tokens = tokenize(text)
        counts = Counter(tokens)
        tags = [word for word, _ in counts.most_common(limit)]
        return tags
