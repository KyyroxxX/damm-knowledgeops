# Damm KnowledgeOps — Intelligent Industrial Knowledge Management & Training Platform

[![AWS Cloud-Native](https://img.shields.io/badge/AWS-Cloud--Native%20Serverless-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Amazon Bedrock](https://img.shields.io/badge/AI-Amazon%20Bedrock%20%7C%20Claude%203.5-7B2CBF)](https://aws.amazon.com/bedrock/)
[![Backend](https://img.shields.io/badge/Backend-Python%203.11%20%7C%20FastAPI%20%7C%20Lambda-3776AB?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Next.js%2014%20%7C%20TypeScript%20%7C%20Tailwind-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Database](https://img.shields.io/badge/Database-Amazon%20DynamoDB%20On--Demand-4053D6?logo=amazondynamodb&logoColor=white)](https://aws.amazon.com/dynamodb/)
[![IaC](https://img.shields.io/badge/IaC-HashiCorp%20Terraform-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![DevSecOps](https://img.shields.io/badge/DevSecOps-Gitleaks%20%7C%20Semgrep%20%7C%20Trivy%20%7C%20Checkov-blueviolet?logo=github-actions&logoColor=white)](https://github.com/features/actions)

---

## AVISO LEGAL Y POLITICA DE DATOS SINTETICOS / LEGAL DISCLAIMER

> [!IMPORTANT] Marco del Proyecto y Seguridad de la Informacion
> **Castellano:**
> Este repositorio constituye una **propuesta tecnica, academica y de arquitectura cloud** desarrollada como solucion al reto de innovacion abierta **MetròpolisFPLab** presentado por **Damm**.
> - **Cero Datos Corporativos Reales:** Este repositorio **NO contiene, utiliza ni expone ninguna documentacion confidencial, secretos industriales, recetas de elaboracion, credenciales internas ni acceso a redes de Damm**.
> - **Entorno de Datos Sinteticos:** El 100% de los manuales tecnicos de maquinaria, codigos de averia, diagramas de troubleshooting y evaluaciones de operarios utilizados en este prototipo son **completamente sinteticos, ficticios o basados en especificaciones publicas genericas de fabricantes OEM**.
> - **Arquitectura Aislada:** La solucion esta disenada bajo el principio de *Customer-Owned Infrastructure*, concebida para que Damm pueda desplegarla de manera independiente dentro de su propia cuenta corporativa de AWS con sus propias claves KMS tras una transferencia formal.
>
> **English:**
> This repository represents an **academic cloud architecture and software engineering proposal** developed for the **MetròpolisFPLab** open innovation challenge presented by **Damm**.
> - **Zero Production Data Policy:** This repository does **NOT contain, access, or expose any confidential Damm systems, real production recipes, employee records, internal network endpoints, or private credentials**.
> - **Synthetic Dataset:** All machinery manuals, maintenance SOPs, error codes, and assessment quizzes used across this codebase are **100% synthetic, fictional, or derived from generic public OEM equipment specifications**.
> - **Air-Gapped Design:** The architecture follows strict zero-trust parameters, designed to be deployed independently inside Damm's private AWS account via parameterized Terraform modules upon formal handover.

---

## 1. Project Overview

**Damm KnowledgeOps** is an enterprise-grade cloud-native platform designed as a proposed solution for the **MetròpolisFPLab** innovation challenge presented by **Damm**.

The platform transforms tacit, fragmented industrial knowledge into structured, validated, and instantly accessible intelligence for plant operations:
1. **Accelerated Onboarding:** Interactive training paths and automated competency assessments for newly hired operators.
2. **Guided Incident Troubleshooting:** Step-by-step diagnostic workflows assisting maintenance technicians during unplanned line stops.
3. **Knowledge Preservation:** Systematic capture and validation of expert technician procedures before staff turnover or retirement.
4. **Zero-Hallucination Industrial RAG:** Domain-grounded conversational assistant that quotes approved procedures by document, section, and page, enforcing strict abstention and human escalation on safety-critical interventions.

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
|  +-------------------------------------------------------------------------------------------------+  |
|               |                                       |                                   |           |
|     [ Read/Write Metadata ]                 [ Vector Search ]                   [ RAG Inference ]     |
|               v                                       v                                   v           |
|  +-------------------------+             +--------------------------+    +-------------------------+  |
|  | Amazon DynamoDB         |             | Amazon S3 (Encrypted)    |    | Amazon Bedrock          |  |
|  | Mode: PAY_PER_REQUEST   |             | - raw-docs (KMS CMK)     |    | - Titan Embeddings v2   |  |
|  | - documents metadata    |             | - processed-docs         |    | - Claude 3.5 Sonnet     |  |
|  | - plant incidents       |             | S3 Trigger -> Lambda     |    | - Claude 3 Haiku        |  |
|  | - training progress     |             | text extraction & chunks |    +-------------------------+  |
|  +-------------------------+             +--------------------------+                                 |
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

## 6. Enterprise Scaling & Production Roadmap

For organizations adopting this system at scale (such as **Damm** moving beyond the MetròpolisFPLab pilot to full multi-plant production), a comprehensive enterprise scaling roadmap is available:

- **Enterprise Proposal & TCO:** Detailed in [`docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md`](file:///c:/Users/Creep/Documents/Git%20Repositorios/damm-knowledgeops/docs/ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md).
- **Hybrid Networking:** AWS Transit Gateway, AWS Direct Connect and AWS PrivateLink VPC Endpoints.
- **Corporate Identity:** SAML 2.0 / SCIM federation with Microsoft Entra ID (Azure AD) and Okta.
- **Bedrock Guardrails:** Managed PII masking, custom blocked topics (brewery formulas, IP) and automated hallucination filters.
- **Industrial Edge Resiliency:** Local offline fallback via AWS Outposts / IoT Greengrass for zero downtime during WAN outages.
- **SIEM Integration:** Real-time log streaming to Splunk, Wazuh Enterprise, or Datadog via Amazon Kinesis Firehose.

---

## 7. Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── devsecops.yml        # CI/CD security pipeline (Gitleaks, Semgrep, Trivy, Checkov)
├── backend/                     # Python 3.11 serverless backend
│   ├── app/
│   │   ├── assistant.py         # Bedrock inference & prompt safety layer
│   │   ├── incidents.py         # Industrial incident tracking & troubleshooting
│   │   ├── ingestion.py         # S3 document processing & Titan embeddings
│   │   ├── main.py              # FastAPI application entrypoint (Mangum ASGI)
│   │   ├── rag_engine.py        # Vector similarity search & metadata filtering
│   │   └── training.py          # Operator learning paths & assessment routes
│   ├── scripts/
│   │   └── generate_synthetic_docs.py # Generator for fictional plant procedures
│   └── tests/                   # Pytest automated test suite
├── frontend/                    # Next.js 14 App Router (TypeScript + Tailwind CSS)
├── infrastructure/
│   └── terraform/               # Declarative IaC manifests
│       ├── api.tf               # API Gateway HTTP API & backend Lambda
│       ├── cognito.tf           # Cognito User Pool, Client & RBAC groups
│       ├── database.tf          # DynamoDB tables (documents, incidents, training)
│       ├── ingestion.tf         # S3 document processing Lambda trigger
│       ├── observability.tf     # CloudWatch log groups (14-day retention) & alarms
│       ├── outputs.tf           # Terraform output parameters
│       ├── providers.tf         # AWS provider definition (eu-west-1)
│       ├── storage.tf           # S3 raw/processed buckets & KMS customer-managed key
│       └── variables.tf         # Parameterized environment variables
├── docs/                        # Architecture guides, threat models & handover procedures
│   ├── ARCHITECTURE_AND_RAG.md  # Deep dive into RAG vector math & cost optimizations
│   ├── ENTERPRISE_PROFESSIONALIZATION_PROPOSAL.md # Enterprise roadmap for Damm production
│   ├── HANDOVER_GUIDE.md        # Technical transfer guide for Damm's IT team
│   └── SECURITY_AND_COMPLIANCE.md # Security posture, threat model & compliance analysis
├── .gitignore                   # Strict security exclusions (no keys, no .env, no state files)
└── README.md                    # Project documentation
```

---

## 8. Compliance & Responsible Disclosure

* **Academic Program:** MetròpolisFPLab Open Innovation Challenge
* **Corporate Challenge:** Damm
* **Ethics & Compliance:** Strictly complies with OWASP Top 10 for LLMs, zero hardcoded credentials, and 100% synthetic operational data.
