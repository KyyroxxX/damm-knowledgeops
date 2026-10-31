# Damm KnowledgeOps — Intelligent Industrial Knowledge Management & Training Platform

[![AWS Cloud-Native](https://img.shields.io/badge/AWS-Cloud--Native%20Serverless-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Amazon Bedrock](https://img.shields.io/badge/AI-Amazon%20Bedrock%20%7C%20Claude%203.5-7B2CBF)](https://aws.amazon.com/bedrock/)
[![Backend](https://img.shields.io/badge/Backend-Python%203.11%20%7C%20FastAPI%20%7C%20Lambda-3776AB?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Next.js%2014%20%7C%20TypeScript%20%7C%20Tailwind-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Database](https://img.shields.io/badge/Database-Amazon%20DynamoDB%20On--Demand-4053D6?logo=amazondynamodb&logoColor=white)](https://aws.amazon.com/dynamodb/)
[![IaC](https://img.shields.io/badge/IaC-HashiCorp%20Terraform-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![DevSecOps](https://img.shields.io/badge/DevSecOps-Gitleaks%20%7C%20Semgrep%20%7C%20Trivy%20%7C%20Checkov-blueviolet?logo=github-actions&logoColor=white)](https://github.com/features/actions)

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
| AWS Serverless Backend (eu-west-1)                                                                    |
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

## 4. Cost Engineering Framework

This platform is engineered to operate strictly within a **0 - 5 EUR / month** development budget:
- **No permanent servers:** Zero EC2 instances and zero NAT Gateways.
- **No provisioned databases:** Amazon DynamoDB operates exclusively in `PAY_PER_REQUEST` mode (25 GB free tier storage).
- **No provisioned vector clusters:** Vector search runs serverless inside Lambda memory and encrypted S3 indexes instead of costly OpenSearch clusters ($700/mo savings).
- **Pay-per-Token AI:** Amazon Bedrock invokes models purely on-demand with synthetic datasets and tight token limits.
- **Automated Budgets:** AWS Budgets configured with strict alert thresholds at $1.00, $1.60, and $2.00 USD.

---

## 5. Repository Structure

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
│   └── tests/                   # Pytest automated test suite
├── frontend/                    # Next.js 14 App Router (TypeScript + Tailwind CSS)
├── infrastructure/
│   └── terraform/               # Declarative IaC manifests
│       ├── api.tf               # API Gateway HTTP API & backend Lambda
│       ├── cognito.tf           # Cognito User Pool, Client & RBAC groups
│       ├── database.tf          # DynamoDB tables (documents, incidents, training)
│       ├── ingestion.tf         # S3 document processing Lambda trigger
│       ├── observability.tf     # CloudWatch log groups (14-day retention) & alarms
│       ├── providers.tf         # AWS provider definition (eu-west-1)
│       └── storage.tf           # S3 raw/processed buckets & KMS customer-managed key
├── docs/                        # Architecture guides, threat models & handover procedures
├── .gitignore                   # Strict security exclusions (no keys, no .env, no state files)
└── README.md                    # Project documentation
```

---

## 6. Academic & Challenge Context

* **Program:** MetròpolisFPLab Innovation Challenge
* **Corporate Partner:** Damm
* **Project:** Damm KnowledgeOps
* **Status:** Under Active Development
