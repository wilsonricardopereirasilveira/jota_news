from lambda_processor.utils.text_processor import tokenize


def test_tokenize_removes_stopwords():
    tokens = tokenize("O ministro falou com a imprensa")
    assert "o" not in tokens
    assert "ministro" in tokens
