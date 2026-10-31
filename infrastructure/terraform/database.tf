resource "aws_dynamodb_table" "documents" {
  name         = "damm-kops-documents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "GSI1PK"
    type = "S"
  }

  attribute {
    name = "GSI1SK"
    type = "S"
  }

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "GSI1PK"
    range_key       = "GSI1SK"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.damm_kops_key.arn
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "incidents" {
  name         = "damm-kops-incidents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "GSI1PK"
    type = "S"
  }

  attribute {
    name = "GSI1SK"
    type = "S"
  }

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "GSI1PK"
    range_key       = "GSI1SK"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.damm_kops_key.arn
  }
}

resource "aws_dynamodb_table" "training" {
  name         = "damm-kops-training"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.damm_kops_key.arn
  }
}

output "dynamodb_documents_table" {
  value = aws_dynamodb_table.documents.name
}

output "dynamodb_incidents_table" {
  value = aws_dynamodb_table.incidents.name
}

output "dynamodb_training_table" {
  value = aws_dynamodb_table.training.name
}
