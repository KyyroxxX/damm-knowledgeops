# Propuesta de Profesionalizacion y Escalado Empresarial — Damm KnowledgeOps

> [!IMPORTANT] Proposito de esta Propuesta
> Este documento define la hoja de ruta de evolucion tecnica, arquitectura de seguridad avanzada y estimacion presupuestaria (TCO) para la transicion de **Damm KnowledgeOps** desde un prototipo de innovacion abierta (**MetròpolisFPLab**) hacia una plataforma corporativa en produccion, integrada en el tenant oficial de **Damm** y alineada con directivas de ciberseguridad industrial (**NIS 2**, **ISO 27001** y **Esquema Nacional de Seguridad - ENS**).

---

## 1. Resumen Ejecutivo de la Transicion

El prototipo actual ha sido optimizado con exito bajo una restriccion presupuestaria extrema (0 - 5 EUR/mes), validando la viabilidad tecnica del asistente RAG, la ingesta documental y los modulos de formacion e incidencias mediante servicios serverless puros.

Si **Damm** decide incorporar la solucion a su catalogo corporativo de sistemas de planta, la prioridad cambia de **minimizacion de costes** a **maximizacion de la seguridad, alta disponibilidad (99.99%), aislamiento de red y cumplimiento normativo**.

```
===================================================================================
FASE DE PROTOTIPO (MetròpolisFPLab)           FASE ENTERPRISE (Damm Corporate Tenant)
===================================================================================
- Cuenta AWS Sandbox aislada                  - AWS Organizations / Control Tower Landing Zone
- Presupuesto: 0 - 5 EUR/mes                  - Presupuesto operativo: ~1.200 - 3.200 EUR/mes
- Vectores en S3 + calculo en Lambda          - Amazon Bedrock Knowledge Bases + OpenSearch Serverless
- Cognito User Pool independiente             - SSO Federado con Microsoft Entra ID (Azure AD) / Okta
- Lambdas en red publica AWS                  - Lambdas en VPC privada con AWS PrivateLink Endpoints
- Logs en CloudWatch estandar                 - SIEM corporativo (Splunk / Wazuh / Datadog via Kinesis)
- Prompt engineering en codigo                - Amazon Bedrock Guardrails con filtro PII y recetas
- Cifrado KMS estandar                        - KMS Multi-Region con CloudHSM FIPS 140-2 Nivel 3
===================================================================================
```

---

## 2. Matriz Comparativa: Prototipo vs. Produccion Enterprise

| Dominio Arquitectonico | Prototipo Actual (Low-Cost) | Propuesta Enterprise Damm | Beneficio para Damm |
|---|---|---|---|
| **Estrategia Multi-Cuenta** | Cuenta AWS unica de desarrollo | Landing Zone (Control Tower) con cuentas separadas: `Identity`, `SecOps`, `SharedNet`, `Prod` | Aislamiento de impacto (Blast Radius) y cumplimiento SOC2. |
| **Identidad y Acceso** | Amazon Cognito User Pools (usuarios locales) | Federacion SAML 2.0 / SCIM con Microsoft Entra ID (Office 365 de Damm) | Control centralizado del ciclo de vida de operarios y baja automatica. |
| **Aislamiento de Red** | Serverless sin VPC (evita coste de NAT GW) | VPC privada con subredes aisladas conectadas a fabricas via **AWS Direct Connect / Transit Gateway** | Cero exposicion a Internet publica; trafico 100% confinado en la red Damm. |
| **Trafico a Servicios AWS** | Internet publica via HTTPS / TLS 1.3 | **AWS PrivateLink (VPC Endpoints)** para S3, DynamoDB, Bedrock y KMS | Cumplimiento estricto de politicas corporativas de no salida a Internet. |
| **Motor Vectorial (RAG)** | Similitud coseno en memoria en Lambda + S3 | **Amazon Bedrock Knowledge Bases** con **OpenSearch Serverless (Vector Engine)** o **Aurora pgvector** | Busqueda hibrida (vectorial + lexico BM25), reranking con Cohere y millones de vectores. |
| **Gobernanza de IA** | Prompt system con delimitadores XML | **Amazon Bedrock Guardrails** con deteccion de PII, bloqueo de secretos industriales y umbrales de alucinacion | Bloqueo nativo e inmutable de fugas de recetas, ingredientes y datos sensibles. |
| **Proteccion Perimetral** | API Gateway con CORS restrictivo | **AWS WAF Enterprise** en CloudFront con Managed Rules, Bot Control e IP Reputation | Mitigacion de ataques DDoS, escaneos automatizados y ataques de denegacion de servicio. |
| **Deteccion de Amenazas** | CloudWatch Alarms estandar | **Amazon GuardDuty** + **AWS Security Hub** + **Amazon Macie** (deteccion de datos sensibles en S3) | Deteccion continua de anomalias en identidades IAM, llamadas a APIs y volumenes S3. |
| **Criptografia** | AWS KMS CMK con rotacion anual | Claves KMS Multi-Region respaldadas por **AWS CloudHSM** (FIPS 140-2 Nivel 3) | Soberania criptografica total; nadie ajeno a Damm puede descifrar los manuales. |
| **Alta Disponibilidad** | Multi-AZ nativa en una region (`eu-west-1`) | Multi-AZ activa + Replicacion de Disaster Recovery en segunda region (`eu-central-1`) | RPO < 1 minuto, RTO < 15 minutos ante fallo regional total. |

---

## 3. Pilares de la Arquitectura Enterprise

### Pilar 1: Identidad Corporativa y Gobierno del Acceso (IAM & SSO)
1. **Federacion con el Directorio Corporativo de Damm:**
   - Sustitucion del registro manual de usuarios por una integracion federada via SAML 2.0 / OIDC con **Microsoft Entra ID** (antiguo Azure AD) o el proveedor de identidad corporativo de Damm.
   - Sincronizacion automatica de grupos mediante **SCIM (System for Cross-domain Identity Management)**: cuando un tecnico de planta cambia de linea o de centro de trabajo (e.g. de la fábrica de El Prat a Santa Coloma), sus permisos en Damm KnowledgeOps se actualizan instantaneamente.
2. **Autenticacion Multifactor Obligatoria (MFA):**
   - Aplicacion de politicas de acceso condicional de Damm (dispositivo corporativo gestionado por Intune, ubicacion de red de planta o autenticador FIDO2/TOTP).

### Pilar 2: Red Privada Hibrida y Aislamiento Absoluto (Zero-Trust Network)
1. **Conectividad con las Plantas Industriales:**
   - Conexion de la VPC de produccion con la red corporativa WAN de Damm mediante **AWS Direct Connect** o enlaces redundantes de **AWS Site-to-Site VPN** gestionados por **AWS Transit Gateway**.
2. **AWS PrivateLink (VPC Endpoints):**
   - Toda la comunicacion entre las funciones Lambda y los servicios AWS (Amazon S3, DynamoDB, Bedrock, KMS y Secrets Manager) se realiza a traves de endpoints de interfaz privados con direcciones IP de la propia VPC.
   - El trafico nunca sale a la red publica de Internet ni transita por gateways NAT.
3. **Inspeccion Centralizada de Trafico:**
   - Despliegue de **AWS Network Firewall** en una VPC de inspeccion compartida (Hub) para auditar cualquier conexion entrante o saliente con reglas basadas en Suricata (aprovechando la experiencia en Suricata adquirida en proyectos previos).

### Pilar 3: Motor RAG Empresarial y Guardrails Gestionados
1. **Amazon Bedrock Knowledge Bases con OpenSearch Serverless:**
   - Indexacion masiva y automatica de cientos de gigabytes de manuales tecnicos (PDFs complejos con tablas, esquemas tecnicos y fotografias de maquinaria).
   - Ingesta multimodal con extraccion de texto mediante **Amazon Textract** para digitalizar planos escaneados antiguos.
   - Mecanismo de busqueda hibrida (Dense Vector + Sparse BM25) combinado con un modelo de **Reranking (Cohere Rerank v3)** para garantizar que el fragmento con mayor precision tecnica encabece siempre el contexto.
2. **Amazon Bedrock Guardrails:**
   - **Filtro de Denegacion de Temas (Custom Denied Topics):** Bloqueo explicito de consultas sobre recetas de cerveza, formulaciones quimicas propietarias, costes de produccion o informacion financiera confidencial.
   - **Enmascaramiento de Datos Personales (PII):** Anonimizacion automatica de nombres de personas, telefonos y DNIs que pudieran figurar en actas de mantenimiento historicas.
   - **Filtro Anti-Hallucination & Grounding Check:** Si la respuesta generada por el LLM no esta respaldada matematicamente con un score de grounding superior al 85% sobre los manuales recuperados, la respuesta se bloquea y se emite la orden de escalado al experto humano.

### Pilar 4: Ciberseguridad Defensiva y Monitorizacion SIEM
1. **Centralizacion en el SIEM Corporativo:**
   - Exportacion de todos los eventos de auditoria de CloudTrail, logs de ejecucion de API Gateway y trazas de Lambda hacia el SIEM de Damm (Splunk, Wazuh Enterprise o Datadog) mediante **Amazon Kinesis Data Firehose**.
2. **Auditoria Continua de Postura de Seguridad (CSPM):**
   - **AWS Security Hub** activado con los estandares *CIS AWS Foundations Benchmark v3.0* y *AWS Foundational Security Best Practices*.
   - **Amazon GuardDuty** supervisando llamadas anomalas a las APIs de Bedrock, accesos inusuales a buckets S3 y ejecuciones sospechosas en Lambda.
3. **AWS WAF en Capa de Distribucion:**
   - CloudFront protegido con AWS WAF activando reglas administradas contra inyecciones SQL, vulnerabilidades conocidas de OWASP Top 10 y proteccion frente a bots.

### Pilar 5: Resiliencia de Planta y Contingencia Local (Edge Computing)
En una fabrica cervecera con ritmos de embotellado de miles de botellas por hora, un corte de fibra optica o caida del proveedor de telecomunicaciones no puede paralizar el soporte a averias criticas:
1. **Copia Local de Contingencia en Planta:**
   - Despliegue de un nodo **AWS Outposts Server** o gateway local con **AWS IoT Greengrass** en las plantas principales (e.g. El Prat de Llobregat).
   - Este nodo sincroniza periodicamente una base de datos vectorial local con los procedimientos de seguridad criticos (paradas de emergencia, protocolos LOTO, rearme de lineas Krones), permitiendo consultas en tiempo real desde tablets en planta incluso con caida total de Internet.

---

## 4. Analisis de Costes TCO (Total Cost of Ownership)

Para facilitar la aprobacion presupuestaria por parte del Comite de Direccion de Damm, se presenta el desglose mensual estimado para un entorno empresarial con 1.500 usuarios activos y soporte a 5 plantas industriales:

| Servicio AWS / Componente | Justificacion Empresarial | Coste Mensual Estimado |
|---|---|---|
| **Amazon Bedrock Knowledge Bases + OpenSearch Serverless** | 4 OCUs base (2 de indexacion, 2 de busqueda) para busqueda vectorial de alta velocidad y alta disponibilidad | ~700.00 USD |
| **Amazon Bedrock (Inferencia LLM & Embeddings)** | Claude 3.5 Sonnet (consultas complejas) + Haiku (clasificacion rapida) + Titan v2 (~150.000 consultas/mes) | ~250.00 USD |
| **AWS Lambda + Amazon API Gateway HTTP** | ~2.000.000 de invocaciones mensuales con tiempos de ejecucion de 500ms y 512MB RAM | ~25.00 USD |
| **Amazon DynamoDB (On-Demand)** | Persistencia de tickets de incidentes, trazabilidad y estado de capacitacion | ~15.00 USD |
| **Amazon S3 + AWS KMS CMK** | Almacenamiento de 500 GB de manuales tecnicos con cifrado dedicado y versionado | ~20.00 USD |
| **AWS Transit Gateway + VPC Endpoints (PrivateLink)** | 4 Interface Endpoints privados para trafico interno sin salir a Internet | ~90.00 USD |
| **AWS WAF + CloudFront** | Inspeccion perimetral de trafico, mitigacion DDoS y distribucion global TLS 1.3 | ~40.00 USD |
| **Amazon GuardDuty + Security Hub + CloudWatch Logs** | Deteccion continua de amenazas y retencion de trazas de auditoria durante 90 dias | ~80.00 USD |
| **AWS Support (Business Plan)** | Soporte 24/7 de ingenieros de AWS con SLA de respuesta de 1 hora para incidencias graves | ~100.00 USD |
| **TOTAL ESTIMADO MENSUAL** | **Infraestructura Enterprise Completa, Privada y de Alta Disponibilidad** | **~1.320.00 USD / mes** |

> [!TIP] Retorno de Inversion (ROI) para Damm
> En una planta cervecera de gran volumen, **una sola hora de parada no planificada en una linea de envasado puede suponer perdidas operativas de entre 10.000 y 45.000 EUR**. Reducir el tiempo medio de resolucion de averias (MTTR) en solo un 15% mediante diagnostico asistido amortiza el coste anual completo de la plataforma en la primera intervencion mitigada.

---

## 5. Plan de Ejecucion del Traspaso (Handover Roadmap)

```
[ Semana 1-2 ] --> Provision de Cuentas en AWS Organizations de Damm & Federacion Entra ID
[ Semana 3-4 ] --> Despliegue de Red Hibrida (Transit Gateway, VPC Endpoints & PrivateLink)
[ Semana 5-6 ] --> Migracion de Datos Sinteticos a Documentacion Real de Planta (Krones, Sidel, etc.)
[ Semana 7-8 ] --> Configuracion de Amazon Bedrock Guardrails con Politicas de Seguridad de Damm
[ Semana 9-10] --> Pruebas de Carga, Auditoria de Seguridad Red Team e Integracion SIEM
[ Semana 11  ] --> Formacion a Supervisores de Planta y Go-Live Oficial en Planta Piloto
```
