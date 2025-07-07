import json
from unittest.mock import patch
from lambda_processor.lambda_function import lambda_handler


def test_lambda_processes_record():
    event = {
        "Records": [
            {"body": json.dumps({"title": "Teste", "content": "algo"})}
        ]
    }
    with patch("lambda_processor.lambda_function.insert_news") as mock_insert:
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200
        mock_insert.assert_called_once()
