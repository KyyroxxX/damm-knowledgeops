output "api_gateway_endpoint" {
  description = "URL publica del API Gateway HTTP"
  value       = aws_apigatewayv2_stage.default_stage.invoke_url
}

output "cognito_user_pool_id" {
  description = "Identificador del User Pool de Cognito"
  value       = aws_cognito_user_pool.damm_pool.id
}

output "cognito_web_client_id" {
  description = "Client ID para integracion frontend en Next.js"
  value       = aws_cognito_user_pool_client.web_client.id
}

output "raw_docs_bucket_name" {
  description = "Nombre del bucket S3 para ingesta de documentos crudos"
  value       = aws_s3_bucket.raw_docs.id
}

output "processed_docs_bucket_name" {
  description = "Nombre del bucket S3 para fragmentos y vectores procesados"
  value       = aws_s3_bucket.processed_docs.id
}

output "kms_key_arn" {
  description = "ARN de la clave KMS CMK utilizada para el cifrado"
  value       = aws_kms_key.damm_kops_key.arn
}
