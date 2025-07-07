from lambda_processor.utils.text_processor import tokenize


def test_news_list_performance(benchmark):
    result = benchmark(lambda: tokenize("Noticia de teste " * 50))
    assert len(result) > 0
