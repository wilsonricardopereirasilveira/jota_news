import datetime
from lambda_processor.classifier.category_classifier import CategoryClassifier
from lambda_processor.classifier.urgency_scorer import UrgencyScorer


def test_classify_tributos_news():
    classifier = CategoryClassifier()
    category, _ = classifier.classify(
        "Imposto de Renda deve ser alterado", "Mudancas na declaracao"
    )
    assert category == "Tributos"


def test_urgency_score_calculation():
    scorer = UrgencyScorer()
    score = scorer.score("URGENTE: STF decide", "Conteudo", "2024-01-01T01:00:00Z")
    assert score >= 50
