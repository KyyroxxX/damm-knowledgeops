# Guia de Traspaso a Produccion — Damm KnowledgeOps

## 1. Requisitos Previos en la Cuenta AWS de Damm
1. Cuenta de AWS corporativa con permisos administrativos para Terraform.
2. Acceso habilitado a los modelos fundacionales en Amazon Bedrock (`eu-west-1`):
   - `amazon.titan-embed-text-v2:0`
   - `anthropic.claude-3-haiku-20240307-v1:0`
   - `anthropic.claude-3-5-sonnet-20240620-v1:0`
3. Zona de DNS en Route 53 (opcional, para dominio personalizado `knowledgeops.damm.com`).

## 2. Despliegue Automatizado
1. Clonar el repositorio oficial transferido.
2. Configurar variables de entorno en `infrastructure/terraform/terraform.tfvars`:
   ```hcl
   environment = "prod"
   aws_region  = "eu-west-1"
   domain_name = "knowledgeops.damm.com"
   ```
3. Ejecutar el pipeline de aprovisionamiento:
   ```bash
   terraform init
   terraform plan -out=tfplan
   terraform apply tfplan
   ```
4. Poblar los primeros manuales oficiales de planta en el bucket `damm-kops-raw-docs-*`.
5. Acceder al panel de Cognito y asignar los primeros usuarios a los grupos `Expert` y `Supervisor`.
