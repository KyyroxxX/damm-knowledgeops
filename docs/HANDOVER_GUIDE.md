# Guia de Traspaso a Produccion y Escalado Enterprise — Damm KnowledgeOps

> [!NOTE] Objeto del Traspaso
> Esta guia detalla el procedimiento tecnico para que el equipo de Cloud Platform y Ciberseguridad de **Damm** tome posesion del repositorio, configure su propia cuenta corporativa de AWS y elija entre el despliegue serverless optimizado o la arquitectura empresarial avanzada.

---

## 1. Opciones de Despliegue en la Cuenta de Damm

El proyecto soporta dos modalidades de operacion dentro de la infraestructura corporativa de Damm:

1. **Modalidad A: Despliegue Directo Serverless (Low TCO / Piloto Inicial):**
   - Mantiene la arquitectura serverless original basada en AWS Lambda, DynamoDB y Amazon Bedrock con indices en S3.
   - Coste mensual insignificante (~$5 - $30 USD/mes segun uso).
   - Ideal para pruebas piloto en una sola linea de envasado o centro de formacion.
   
2. **Modalidad B: Arquitectura Enterprise de Alta Seguridad (Produccion Multi-Planta):**
   - Incorpora VPC privada con AWS PrivateLink, federacion SSO con Microsoft Entra ID, Bedrock Guardrails, OpenSearch Serverless, AWS WAF y enlace con el SIEM corporativo.
   - Consultar la especificacion completa en: [`ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md`](file:///c:/Users/Creep/Documents/Git%20Repositorios/damm-knowledgeops/docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md).

---

## 2. Requisitos Previos en la Cuenta AWS de Damm

1. Cuenta de AWS corporativa con permisos administrativos para aprovisionamiento mediante Terraform (v1.8+).
2. Modelos fundacionales habilitados en Amazon Bedrock (`eu-west-1` Irlanda o `eu-central-1` Frankfurt):
   - `amazon.titan-embed-text-v2:0` (Embeddings vectoriales de 1024 dimensiones)
   - `anthropic.claude-3-haiku-20240307-v1:0` (Clasificacion rapida e incidencias)
   - `anthropic.claude-3-5-sonnet-20240620-v1:0` (Razonamiento contextual de alta precision)
3. Zona alojada privada o publica en Amazon Route 53 para el nombre de dominio corporativo (ej. `knowledgeops.damm.com`).

---

## 3. Procedimiento de Despliegue Automatizado

1. Clonar el repositorio transferido en el entorno seguro de CI/CD de Damm (GitLab CI, GitHub Enterprise o AWS CodePipeline).
2. Crear el archivo de variables parametrizadas `infrastructure/terraform/terraform.tfvars`:
   ```hcl
   environment  = "prod"
   aws_region   = "eu-west-1"
   project_name = "damm-knowledgeops"
   ```
3. Ejecutar el ciclo de aprovisionamiento de infraestructura:
   ```bash
   terraform init
   terraform plan -out=tfplan
   terraform apply tfplan
   ```
4. Cargar los manuales tecnicos y procedimientos operativos estandar (SOPs) reales de planta en el bucket `damm-kops-raw-docs-<account-id>`.
5. Los documentos cargados activaran automaticamente el procesamiento mediante la Lambda de ingesta, generando chunks cifrados y metadatos en DynamoDB con estado `PENDING_EXPERT_APPROVAL`.
6. Los ingenieros jefes de planta asignados al grupo `Expert` podran validar formalmente los manuales desde la interfaz antes de que esten disponibles para consultas de los operarios.
