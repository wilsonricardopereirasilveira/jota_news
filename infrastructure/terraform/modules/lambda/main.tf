resource "aws_iam_role" "lambda" {
  name = "lambda-${var.environment}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_lambda_function" "processor" {
  filename         = var.package_file
  function_name    = "news-processor-${var.environment}"
  role             = aws_iam_role.lambda.arn
  handler          = var.handler
  source_code_hash = filebase64sha256(var.package_file)
  runtime          = "python3.9"
  timeout          = 300
  memory_size      = 512
  environment {
    variables = {
      QUEUE_URL = var.queue_url
      DB_SECRET = var.db_secret_arn
    }
  }
  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }
  dead_letter_config {
    target_arn = var.dlq_arn
  }
  reserved_concurrent_executions = var.reserved_concurrency
}
