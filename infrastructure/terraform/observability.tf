resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/aws/lambda/${aws_lambda_function.backend_api.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "ingest_logs" {
  name              = "/aws/lambda/${aws_lambda_function.doc_ingestion.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "damm-kops-lambda-high-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Alarma activada si el backend de Damm KnowledgeOps supera 5 errores en 5 minutos"
}
