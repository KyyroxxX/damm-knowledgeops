# Damm KnowledgeOps — Intelligent Industrial Knowledge Management & Training Platform

[![AWS Cloud-Native](https://img.shields.io/badge/AWS-Cloud--Native%20Serverless-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Amazon Bedrock](https://img.shields.io/badge/AI-Amazon%20Bedrock%20%7C%20Claude%203.5-7B2CBF)](https://aws.amazon.com/bedrock/)
[![Challenge](https://img.shields.io/badge/Challenge-Metr%C3%B2polisFPLab%20%7C%20Damm-C8102E)](https://www.metropolisfplab.cat/)
[![Architecture](https://img.shields.io/badge/Architecture-100%25%20Serverless%20Pay--per--Use-blue)](docs/ARCHITECTURE_AND_RAG.md)
[![Security](https://img.shields.io/badge/Security-Zero%20Trust%20%7C%20Bedrock%20Guardrails-green)](docs/SECURITY_AND_COMPLIANCE.md)
[![DevSecOps](https://img.shields.io/badge/DevSecOps-Gitleaks%20%7C%20Semgrep%20%7C%20Checkov-blueviolet)](docs/SECURITY_AND_COMPLIANCE.md)

---

## AVISO LEGAL Y POLITICA DE DATOS SINTETICOS / LEGAL DISCLAIMER

> [!IMPORTANT] Marco del Proyecto y Seguridad de la Informacion
> **Castellano:**
> Este repositorio constituye el **centro de documentacion tecnica, arquitectura cloud y propuesta estrategica** desarrollada como solucion al reto de innovacion abierta **MetròpolisFPLab** presentado por **Damm**.
> - **Cero Datos Corporativos Reales:** Este repositorio **NO contiene, utiliza ni expone ninguna documentacion confidencial, secretos industriales, recetas de elaboracion, credenciales internas ni acceso a redes de Damm**.
> - **Entorno de Datos Sinteticos:** El 100% de los manuales tecnicos de maquinaria, codigos de averia, diagramas de troubleshooting y evaluaciones de operarios analizados en esta propuesta son **completamente sinteticos, ficticios o basados en especificaciones publicas genericas de fabricantes OEM**.
> - **Arquitectura Aislada:** La solucion esta concebida bajo el principio de *Customer-Owned Infrastructure*, disenada para que Damm pueda desplegarla de manera independiente dentro de su propia cuenta corporativa de AWS con sus propias claves KMS tras una transferencia formal.
>
> **English:**
> This repository represents the **technical documentation, cloud architecture, and strategic proposal center** developed for the **MetròpolisFPLab** open innovation challenge presented by **Damm**.
> - **Zero Production Data Policy:** This repository does **NOT contain, access, or expose any confidential Damm systems, real production recipes, employee records, internal network endpoints, or private credentials**.
> - **Synthetic Dataset:** All machinery manuals, maintenance SOPs, error codes, and assessment quizzes referenced are **100% synthetic, fictional, or derived from generic public OEM equipment specifications**.
> - **Air-Gapped Design:** The architecture follows strict zero-trust parameters, designed to be deployed independently inside Damm's private AWS account via parameterized Terraform modules upon formal handover.

---

## 1. Project Overview

**Damm KnowledgeOps** is an enterprise-grade cloud-native platform designed as a proposed solution for the **MetròpolisFPLab** innovation challenge presented by **Damm**.

The platform transforms tacit, fragmented industrial knowledge into structured, validated, and instantly accessible intelligence for plant operations:
1. **Accelerated Onboarding:** Interactive training paths and automated competency assessments for newly hired operators.
2. **Guided Incident Troubleshooting:** Step-by-step diagnostic workflows assisting maintenance technicians during unplanned line stops.
3. **Knowledge Preservation:** Systematic capture and validation of expert technician procedures before staff turnover or retirement.
4. **Zero-Hallucination Industrial RAG:** Domain-grounded conversational assistant that quotes approved procedures by document, section, and page, enforcing strict abstention and human escalation on safety-critical interventions.
5. **Kaizen & Worker Voice:** Dedicated conversational channel for ergonomics, health improvements, and plant optimization with complete anonymity control, troll filtering, and supervisor priority triage.

---

## 2. Serverless Cloud Architecture

```
                                [ Plant Operator / Maintenance Tablet ]
                                                   |
                                     ( HTTPS / TLS 1.3 Inspection )
                                                   v
                                   +-------------------------------+
                                   |  Amazon CloudFront / Amplify  |
                                   |     Next.js Enterprise UI     |
                                   +-------------------------------+
                                        |                     |
                      [ 1. JWT Authentication ]        [ 2. REST API Requests ]
                                        v                     v
                        +----------------------+    +---------------------------+
                        | Amazon Cognito Pool  |    | Amazon API Gateway (HTTP) |
                        | RBAC: Employee/Expert|    | Native JWT Authorizer     |
                        +----------------------+    +---------------------------+
                                                                  |
                                              [ AWS_PROXY Lambda Trigger ]
                                                                  v
+=======================================================================================================+
AWS Serverless Backend (eu-west-1)                                                                    |
|                                                                                                       |
|  +-------------------------------------------------------------------------------------------------+  |
|  | AWS Lambda: damm-kops-backend-api (Python 3.11 + FastAPI + Mangum)                              |  |
|  | - Chat Ingestion & Vector Retrieval Engine                                                     |  |
|  | - Incident Registration & Step-by-Step Troubleshooting                                          |  |
|  | - Operator Training Progression & Quiz Scoring                                                 |  |
|  | - Kaizen, Ergonomics & Worker Voice Processing                                                 |  |
|  +-------------------------------------------------------------------------------------------------+  |
|               |                                       |                                   |           |
|     [ Read/Write Metadata ]                 [ Vector Search ]                   [ RAG Inference ]     |
|               v                                       v                                   v           |
|  +-------------------------+             +--------------------------+    +-------------------------+  |
|  | Amazon DynamoDB         |             | Amazon S3 (Encrypted)    |    | Amazon Bedrock          |  |
|  | Mode: PAY_PER_REQUEST   |             | - raw-docs (KMS CMK)     |    | - Titan Embeddings v2   |  |
|  | - documents metadata    |             | - processed-docs         |    | - Claude 3.5 Sonnet     |  |
|  | - plant incidents       |             | S3 Trigger -> Lambda     |    | - Claude 3 Haiku        |  |
|  | - training progress     |             | text extraction & chunks |    | - Bedrock Guardrails    |  |
|  | - proposals (Kaizen)    |             +--------------------------+    +-------------------------+  |
|  +-------------------------+                                                                          |
+=======================================================================================================+
                                              |
                          [ Audit Logging & Operational Metrics ]
                                              v
                              +-------------------------------+
                              | Amazon CloudWatch & CloudTrail|
                              | 14-Day Log Retention Policy   |
                              +-------------------------------+
```

---

## 3. Key Functional Modules

| Module | Purpose | Core Technologies |
|---|---|---|
| **Module A: Identity & RBAC** | Multi-tier authorization distinguishing `Employee`, `Supervisor`, `Expert`, and `Admin`. | Amazon Cognito User Pools, JWT verification. |
| **Module B: Knowledge Management** | Secure document ingestion, text parsing, semantic chunking, and expert approval workflows. | Amazon S3, AWS KMS, AWS Lambda, DynamoDB. |
| **Module C: Grounded Assistant** | Natural language queries with verified citations, prompt injection defense, and safety escalation. | Amazon Bedrock, Titan Embeddings v2, Claude 3.5. |
| **Module D: Incident Troubleshooting** | Interactive breakdown diagnostics, resolution auditing, and automated SOP promotion. | FastAPI, DynamoDB, Bedrock. |
| **Module E: Training & Assessments** | Departmental learning paths and automated procedural quizzes. | Next.js, DynamoDB, Python backend. |
| **Module F: Audit & DevSecOps** | Cost governance, least-privilege IAM, and continuous security testing. | AWS Budgets, CloudWatch, Terraform, GitHub Actions. |
| **Module G: Kaizen & Worker Voice** | Dedicated channel for ergonomics/workplace improvements, troll filtering, priority scoring, anonymous/identified submission, and supervisor dashboard. | FastAPI, Bedrock Claude 3, DynamoDB. |

---

## 4. Responsible AI & Industrial Safety Guarantees

In an industrial beverage packaging environment, an unverified AI recommendation could cause machinery damage or occupational hazards. This platform implements 4 strict safety barriers:

1. **Mandatory Document Grounding:** The assistant is mathematically restricted to the approved text chunks passed inside `<approved_procedures>` tags. It is instructed to reject answering if data is missing.
2. **Exact Citations:** Every operational output contains the document source identifier and chunk index (`[Fuente: manual_embotellado.txt | Fragmento: 0]`).
3. **Prompt Injection Defense:** Strict XML delimitation between system instructions and operator prompts prevents jailbreaks or unauthorized directive overrides.
4. **Human Supervisor Escalation:** Critical interventions (electrical LOTO, steam, high pressure) trigger an automated escalation event in DynamoDB for human verification.

---

## 5. Cost Engineering Framework

This platform is engineered to operate strictly within a **0 - 5 EUR / month** development budget:
- **No permanent servers:** Zero EC2 instances and zero NAT Gateways.
- **No provisioned databases:** Amazon DynamoDB operates exclusively in `PAY_PER_REQUEST` mode (25 GB free tier storage).
- **No provisioned vector clusters:** Vector search runs serverless inside Lambda memory and encrypted S3 indexes instead of costly OpenSearch clusters ($700/mo savings).
- **Pay-per-Token AI:** Amazon Bedrock invokes models purely on-demand with synthetic datasets and tight token limits.
- **Automated Budgets:** AWS Budgets configured with strict alert thresholds at $1.00, $1.60, and $2.00 USD.

---

## 6. Enterprise Scaling & Multi-Tier Production Proposals

For organizations adopting this system at scale (such as **Damm** moving beyond the MetròpolisFPLab pilot to full multi-plant production), a comprehensive 3-tier enterprise professionalization proposal is available in [`docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md`](docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md):

* **Tier 1 — Lean Serverless (~32 EUR/month):** 100% Serverless Pay-per-Use, Bedrock Guardrails, in-memory vector search with S3 + KMS, DynamoDB On-Demand, Cognito + MFA, GuardDuty and Security Hub. Ideal for pilot line validation with zero idle cost.
* **Tier 2 — Industrial Hybrid (~285 EUR/month):** Private VPC with Site-to-Site VPN, AWS PrivateLink VPC Endpoints (zero public internet transit), Amazon Aurora Serverless v2 PostgreSQL with `pgvector`, Microsoft Entra ID (Azure AD) SSO federation via SAML/SCIM, and AWS WAF. Designed for production in 1-2 major factories (e.g. El Prat & Santa Coloma).
* **Tier 3 — Mission-Critical Multi-Plant (~1,315 - 2,380 EUR/month):** Multi-Account AWS Control Tower Landing Zone, Bedrock Knowledge Bases with Amazon OpenSearch Serverless (4 OCUs HA), AWS Direct Connect + Transit Gateway, AWS Network Firewall (Suricata), Bedrock Guardrails with grounding filters, Kinesis Firehose streaming to corporate SIEM (Splunk/Wazuh), CloudHSM (FIPS 140-2 Level 3) and Multi-Region Disaster Recovery (`eu-west-1` + `eu-central-1`) fulfilling European **NIS 2**, **ISO 27001**, and **ENS** regulations.

---

## 7. Centro de Documentacion Tecnica / Documentation Center

Toda la informacion estrategica, arquitectura y especificaciones del proyecto se encuentra estructurada en la carpeta [`docs/`](docs/):

- [`docs/EXECUTIVE_PRESENTATION.md`](docs/EXECUTIVE_PRESENTATION.md): Presentacion ejecutiva completa del proyecto para direccion, comite de innovacion y jurado MetròpolisFPLab.
- [`docs/FUNCTIONAL_SPECIFICATIONS.md`](docs/FUNCTIONAL_SPECIFICATIONS.md): Especificaciones funcionales exhaustivas de los Modulos A a G (incluyendo Kaizen, Ergonomia y Voz del Operario).
- [`docs/ARCHITECTURE_AND_RAG.md`](docs/ARCHITECTURE_AND_RAG.md): Arquitectura cloud en detalle, seleccion de servicios serverless y matematicas del motor RAG.
- [`docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md`](docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md): Estudio comparativo y economico detallado de los tres niveles empresariales (Tier 1, Tier 2 y Tier 3).
- [`docs/SECURITY_AND_COMPLIANCE.md`](docs/SECURITY_AND_COMPLIANCE.md): Modelo de amenazas, directivas de IA responsable (OWASP Top 10 LLM), controles criptograficos y aislamiento.
- [`docs/HANDOVER_GUIDE.md`](docs/HANDOVER_GUIDE.md): Guia de despliegue y transferencia formal para el equipo de Cloud & Ciberseguridad de Damm.

> [!NOTE] Nota sobre el Codigo Fuente
> Este repositorio publico actua como centro de documentacion, arquitectura y propuesta para la evaluacion del reto. Los modulos de codigo fuente del backend y manifiestos IaC de Terraform se gestionan en ramas tecnicas de desarrollo (`dev/full-code`) y repositorios privados de control de versiones, transferibles a Damm durante la fase de despliegue.

---

## 8. Compliance & Responsible Disclosure

* **Academic Program:** MetròpolisFPLab Open Innovation Challenge
* **Corporate Challenge:** Damm
* **Ethics & Compliance:** Strictly complies with OWASP Top 10 for LLMs, zero hardcoded credentials, and 100% synthetic operational data.
