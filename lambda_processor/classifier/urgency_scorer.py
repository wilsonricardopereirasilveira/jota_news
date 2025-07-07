import datetime
from .keywords import URGENT_KEYWORDS


class UrgencyScorer:
    """Calculate urgency score for a piece of news."""

    def score(self, title: str, content: str, published_at: str | None = None) -> int:
        text = f"{title} {content}".lower()
        score = 0
        for word in URGENT_KEYWORDS:
            if word in text:
                score += 30
        if published_at:
            try:
                dt = datetime.datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            except ValueError:
                dt = datetime.datetime.utcnow()
        else:
            dt = datetime.datetime.utcnow()
        if dt.hour >= 22 or dt.hour < 6 or dt.weekday() >= 5:
            score += 20
        authorities = ['presidente', 'ministro', 'governador', 'prefeito']
        if any(a in text for a in authorities):
            score += 20
        return min(score, 100)
