data "archive_file" "ingestion_zip" {
  type        = "zip"
  source_file = "${path.module}/../../backend/app/ingestion.py"
  output_path = "${path.module}/ingestion.zip"
}

resource "aws_iam_role" "lambda_ingest_role" {
  name = "damm-kops-ingest-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_ingest_policy" {
  name = "damm-kops-ingest-policy"
  role = aws_iam_role.lambda_ingest_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:eu-west-1:*:*"
      },
      {
        Effect = "Allow"
        Action = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.raw_docs.arn}/*"
      },
      {
        Effect = "Allow"
        Action = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.processed_docs.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Resource = aws_dynamodb_table.documents.arn
      },
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:eu-west-1::foundation-model/amazon.titan-embed-text-v2:0"
      },
      {
        Effect = "Allow"
        Action = ["kms:Decrypt", "kms:GenerateDataKey"]
        Resource = aws_kms_key.damm_kops_key.arn
      }
    ]
  })
}

resource "aws_lambda_function" "doc_ingestion" {
  function_name    = "damm-kops-doc-ingestion"
  runtime          = "python3.11"
  handler          = "ingestion.handler"
  role             = aws_iam_role.lambda_ingest_role.arn
  filename         = data.archive_file.ingestion_zip.output_path
  source_code_hash = data.archive_file.ingestion_zip.output_base64sha256
  timeout          = 60
  memory_size      = 512

  environment {
    variables = {
      DOCUMENTS_TABLE  = aws_dynamodb_table.documents.name
      PROCESSED_BUCKET = aws_s3_bucket.processed_docs.id
    }
  }
}

resource "aws_lambda_permission" "allow_s3_raw" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.doc_ingestion.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw_docs.arn
}

resource "aws_s3_bucket_notification" "raw_bucket_notification" {
  bucket = aws_s3_bucket.raw_docs.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.doc_ingestion.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3_raw]
}
