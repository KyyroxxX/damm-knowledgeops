# Guia de Traspaso a Produccion y Escalado Enterprise — Damm KnowledgeOps

> [!NOTE] Objeto del Traspaso
> Esta guia detalla el procedimiento tecnico para que el equipo de Cloud Platform y Ciberseguridad de **Damm** tome posesion del repositorio, configure su propia cuenta corporativa de AWS y elija entre el despliegue serverless optimizado o la arquitectura empresarial avanzada.

---

## 1. Opciones de Despliegue en la Cuenta de Damm

El proyecto soporta tres modalidades escalonadas de despliegue dentro de la infraestructura corporativa de Damm:

1. **Tier 1: Despliegue Lean Serverless (~32 EUR/mes):**
   - Arquitectura 100% Serverless Pay-per-Use con Lambda, DynamoDB, Bedrock Guardrails y almacenamiento cifrado en S3.
   - Ideal para pruebas piloto acotadas en una sola linea de envasado o en el centro de formacion tecnica.
   
2. **Tier 2: Despliegue Industrial Hybrid (~285 EUR/mes):**
   - Incorpora VPC privada con AWS PrivateLink (sin salida a Internet), conexion VPN con las fabricas, motor vectorial Aurora Serverless v2 PostgreSQL con `pgvector`, federacion SSO con Microsoft Entra ID y proteccion perimetral con AWS WAF.
   - Disenado para produccion en 1 o 2 fabricas principales (El Prat de Llobregat / Santa Coloma).

3. **Tier 3: Despliegue Mission-Critical Multi-Planta (~1.315 - 2.380 EUR/mes):**
   - Multi-Account Landing Zone (AWS Control Tower), Bedrock Knowledge Bases con OpenSearch Serverless, AWS Direct Connect, Network Firewall, exportacion a SIEM corporativo (Splunk/Wazuh), CloudHSM FIPS 140-2 Nivel 3 y Disaster Recovery multi-region (`eu-west-1` + `eu-central-1`) para cumplimiento estricto de **NIS 2**, **ISO 27001** y **ENS**.
   - Consultar la especificacion y justificacion economica completa en: [`ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md`](file:///c:/Users/Creep/Documents/Git%20Repositorios/damm-knowledgeops/docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md).

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
