data "aws_caller_identity" "current" {}

resource "aws_kms_key" "damm_kops_key" {
  description             = "KMS Key para cifrado de documentos y datos de Damm KnowledgeOps"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_kms_alias" "damm_kops_key_alias" {
  name          = "alias/damm-kops-key"
  target_key_id = aws_kms_key.damm_kops_key.key_id
}

resource "aws_s3_bucket" "raw_docs" {
  bucket        = "damm-kops-raw-docs-${data.aws_caller_identity.current.account_id}"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "raw_versioning" {
  bucket = aws_s3_bucket.raw_docs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw_encryption" {
  bucket = aws_s3_bucket.raw_docs.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.damm_kops_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "raw_public_block" {
  bucket = aws_s3_bucket.raw_docs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "raw_enforce_tls" {
  bucket = aws_s3_bucket.raw_docs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLSRequestsOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.raw_docs.arn,
          "${aws_s3_bucket.raw_docs.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

resource "aws_s3_bucket" "processed_docs" {
  bucket        = "damm-kops-processed-docs-${data.aws_caller_identity.current.account_id}"
  force_destroy = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "processed_encryption" {
  bucket = aws_s3_bucket.processed_docs.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.damm_kops_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "processed_public_block" {
  bucket = aws_s3_bucket.processed_docs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "raw_docs_bucket_name" {
  value = aws_s3_bucket.raw_docs.id
}

output "processed_docs_bucket_name" {
  value = aws_s3_bucket.processed_docs.id
}

output "kms_key_arn" {
  value = aws_kms_key.damm_kops_key.arn
}
