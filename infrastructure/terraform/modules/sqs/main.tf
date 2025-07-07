resource "aws_sqs_queue" "main" {
  name = "news-${var.environment}-queue"
}

resource "aws_sqs_queue" "dlq" {
  name = "news-${var.environment}-dlq"
}

output "queue_url" {
  value = aws_sqs_queue.main.id
}

output "dlq_arn" {
  value = aws_sqs_queue.dlq.arn
}
