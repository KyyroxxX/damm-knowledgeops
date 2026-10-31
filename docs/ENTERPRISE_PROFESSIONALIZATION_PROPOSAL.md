# Propuestas de Profesionalizacion y Escalado Empresarial — Damm KnowledgeOps

> [!IMPORTANT] Marco Estrategico de Escalado
> Este documento define tres propuestas tecnicas y economicas escalonadas (**Tier 1**, **Tier 2** y **Tier 3**) para adaptar **Damm KnowledgeOps** a las necesidades operativas, de red y presupuestarias de **Damm**.
>
> Permite a los responsables de IT, Operaciones y Ciberseguridad de Damm seleccionar el nivel de servicio adecuado segun la fase del proyecto: desde una prueba piloto acotada con coste minimo hasta el despliegue multi-planta de mision critica conforme a la directiva europea **NIS 2**, **ISO 27001** y el **Esquema Nacional de Seguridad (ENS)**.

---

## 1. Resumen Comparativo de los 3 Niveles de Profesionalizacion

```
========================================================================================================================
NIVEL / PROPUESTA             PRESUPUESTO ESTIMADO    PERFIL DE DESPLIEGUE                    MOTOR VECTORIAL & RED
========================================================================================================================
Tier 1: Lean Serverless       ~15 - 45 EUR / mes      Prueba piloto en 1 linea o academia     Lambda in-memory + S3 KMS
                                                      (100% Serverless Pay-per-Use)          Red AWS Cloud nativa

Tier 2: Industrial Hybrid     ~280 - 580 EUR / mes    Produccion en 1-2 plantas reales        Aurora Serverless v2 pgvector
                                                      (El Prat / Santa Coloma)               VPC privada + VPN + PrivateLink

Tier 3: Mission-Critical      ~1.400 - 3.200 EUR/mes  Corporativo global multi-planta         OpenSearch Serverless (4 OCUs HA)
                                                      (Cumplimiento NIS 2 / ISO 27001)       Direct Connect + CloudHSM + DR
========================================================================================================================
```

---

## 2. Detalle Tecnico de Cada Propuesta

### TIER 1: Lean Enterprise / Cloud-Native Serverless
*Presupuesto mensual estimado:* **~15 - 45 EUR / mes** (~$20 - 50 USD/mes)  
*Alcance ideal:* Validación operativa en 1 línea de envasado, centro de formación técnica o prueba de concepto avanzada dentro del tenant de Damm.

#### Características Principales:
1. **Arquitectura 100% Serverless Pay-per-Use:**
   - **AWS Lambda (Python 3.11 + FastAPI + Mangum):** Facturación por milisegundo de ejecución; coste $0.00 en reposo.
   - **Amazon API Gateway HTTP API:** Tráfico cifrado TLS 1.3 con autorizador nativo JWT.
   - **Amazon DynamoDB (Modo On-Demand):** Tablas de incidentes, metadatos y capacitaciones sin provisionamiento fijo (incluido en Free Tier de 25 GB).
2. **Seguridad e IA Responsable Activada:**
   - **Amazon Bedrock Guardrails:** Filtro de denegación para fórmulas secretas de elaboración cervecera, enmascaramiento automático de PII (nombres, correos, teléfonos) y bloqueo de ataques de prompt injection ($0.75 USD por cada 1.000 unidades de texto; <$0.50/mes).
   - **Modelos Bedrock Serverless:** Amazon Titan Embeddings v2 (1024d) + Claude 3 Haiku (rápido y económico) con opción de escalado a Claude 3.5 Sonnet para consultas complejas.
   - **Motor Vectorial en Memoria:** Cálculo de similitud coseno en memoria de Lambda persistiendo fragmentos cifrados en S3 bajo clave KMS CMK con rotación automática anual.
3. **Gobierno y Auditoría:**
   - **Amazon Cognito User Pools:** Directorio con MFA obligatorio (primeros 50.000 usuarios activos mensuales gratuitos).
   - **AWS IAM Identity Center (SSO):** Activación nativa gratuita para acceso administrativo de técnicos.
   - **AWS GuardDuty + AWS Security Hub:** Supervisión continua de postura de seguridad y detección de amenazas.
   - **CloudWatch Logs:** Retención estricta de 14 días para evitar acumulación de costes de almacenamiento de logs.

#### Desglose Financiero Tier 1:
- Amazon Bedrock (Embeddings + Inferencia ~15.000 consultas/mes): ~$15.00 USD
- Amazon Bedrock Guardrails (~15.000 evaluaciones): ~$1.50 USD
- AWS Lambda + API Gateway HTTP: ~$3.00 USD
- Amazon DynamoDB + S3 + KMS: ~$4.00 USD
- CloudWatch + GuardDuty / Security Hub (tras Free Trial): ~$12.00 USD
- **Total Tier 1:** **~$35.50 USD / mes (~32.00 EUR / mes)**

---

### TIER 2: Industrial Hybrid / Private Connected Plant
*Presupuesto mensual estimado:* **~280 - 580 EUR / mes** (~$300 - 620 USD/mes)  
*Alcance ideal:* Producción en 1 o 2 fábricas principales (ej. El Prat de Llobregat y Santa Coloma) con requerimientos corporativos de aislamiento de red y conexión con la WAN de planta.

#### Características Principales:
1. **Red Privada Híbrida Aislada (Zero Internet Egress):**
   - **VPC Privada con Subredes Segregadas:** Las funciones Lambda ejecutan dentro de subredes privadas sin salida a Internet.
   - **AWS PrivateLink (VPC Interface Endpoints):** Interfaces de red elásticas (ENI) privadas para invocar Bedrock, KMS y Secrets Manager sin que el tráfico salga de la red de AWS.
   - **Gateway Endpoints:** Enrutamiento privado gratuito directo a S3 y DynamoDB.
   - **AWS Site-to-Site VPN:** Túnel IPsec redundante que conecta la VPC con la red de planta de las fábricas de Damm.
2. **Motor Vectorial Transaccional:**
   - **Amazon Aurora Serverless v2 PostgreSQL con `pgvector`:** Base de datos relacional y vectorial con escalado elástico de 0.5 a 2 ACUs (Aurora Capacity Units). Permite consultas SQL combinadas con búsqueda por similitud vectorial y backups automáticos continuos sin pagar la cuota fija mínima de OpenSearch.
3. **Identidad Corporativa y Protección Web:**
   - **Federación SAML 2.0 / SCIM:** Integración directa con **Microsoft Entra ID** (antiguo Azure AD / Office 365 de Damm) para aprovisionamiento y desprovisionamiento automático de operarios.
   - **AWS WAF:** Desplegado en CloudFront con reglas administradas de AWS contra inyecciones SQL, vulnerabilidades web y rate limiting.

#### Desglose Financiero Tier 2:
- Amazon Bedrock (Inferencia + Guardrails para ~50.000 consultas/mes): ~$60.00 USD
- Amazon Aurora Serverless v2 PostgreSQL (pgvector, 0.5 a 1 ACU medio): ~$55.00 USD
- VPC Endpoints (PrivateLink para Bedrock y KMS) + Site-to-Site VPN: ~$75.00 USD
- AWS WAF + CloudFront: ~$25.00 USD
- Lambda, DynamoDB, S3 y KMS: ~$20.00 USD
- GuardDuty + Security Hub + CloudWatch Logs (retención 30 días): ~$45.00 USD
- AWS Developer Support Plan: ~$29.00 USD
- **Total Tier 2:** **~$309.00 USD / mes (~285.00 EUR / mes)**

---

### TIER 3: Mission-Critical Multi-Plant / NIS 2 & High Availability
*Presupuesto mensual estimado:* **~1.400 - 3.200 EUR / mes** (~$1.500 - 3.500 USD/mes)  
*Alcance ideal:* Despliegue corporativo global para toda la red de fábricas, centros logísticos y oficinas de Damm, con disponibilidad del 99.99% y cumplimiento regulatorio estricto (**NIS 2**, **ISO 27001**, **Esquema Nacional de Seguridad - ENS**).

#### Características Principales:
1. **Gobernanza Multi-Cuenta y Red de Alta Velocidad:**
   - **AWS Control Tower / Organizations:** Segmentación estricta de cuentas AWS (`Identity`, `Security-Tooling`, `Log-Archive`, `Shared-Network`, `Production-Core`).
   - **AWS Direct Connect (1 Gbps redundante):** Conexión de fibra dedicada directa entre las fábricas y AWS, gestionada mediante **AWS Transit Gateway**.
   - **AWS Network Firewall:** Inspección de tráfico en capa de red mediante firmas y reglas IDS/IPS basadas en Suricata.
2. **Búsqueda Vectorial Empresarial de Alta Densidad:**
   - **Amazon Bedrock Knowledge Bases + OpenSearch Serverless:** 4 OCUs base dedicadas en alta disponibilidad Multi-AZ. Indexación masiva de miles de manuales técnicos, esquemas de maquinaria y partes de mantenimiento. Búsqueda híbrida (Dense Vector + Sparse BM25) con modelo de reordenación **Cohere Rerank v3**.
   - **Digitalización Multimodal con Amazon Textract:** Procesamiento de diagramas técnicos antiguos escaneados.
3. **Ciberseguridad Avanzada, SIEM y Criptografía HSM:**
   - **Streaming a SIEM Corporativo:** Exportación continua en tiempo real de trazas de CloudTrail, WAF y Lambda hacia el SIEM de Damm (**Splunk**, **Wazuh Enterprise** o **Datadog**) vía **Amazon Kinesis Data Firehose**.
   - **AWS CloudHSM (FIPS 140-2 Nivel 3):** Claves KMS respaldadas en módulos de seguridad de hardware dedicados, garantizando la soberanía criptográfica total de los procedimientos de Damm.
   - **Amazon Bedrock Guardrails Avanzados:** Filtros de alucinación matemáticos con bloqueo ante umbrales de fundamentación inferiores al 85%.
4. **Resiliencia Extrema y Contingencia de Planta:**
   - **Disaster Recovery Multi-Región Activa/Pasiva:** Replicación continua entre `eu-west-1` (Irlanda) y `eu-central-1` (Frankfurt) con RPO < 1 minuto y RTO < 15 minutos.
   - **Nodo Local de Contingencia (AWS Outposts / IoT Greengrass):** Servidor local en fábrica que almacena procedimientos de emergencia y LOTO para permitir diagnósticos críticos sin conexión a Internet WAN.

#### Desglose Financiero Tier 3:
- Bedrock Knowledge Bases + OpenSearch Serverless (4 OCUs HA): ~$700.00 USD
- Amazon Bedrock (Inferencia a gran escala ~150.000 consultas/mes): ~$250.00 USD
- AWS Transit Gateway + VPC Endpoints + Network Firewall: ~$220.00 USD
- AWS CloudHSM (1 módulo de hardware dedicado de alta seguridad): ~$1.152.00 USD (opcional según exigencia de auditoría militar/farmacéutica; prescindible para ahorrar ~$1.150 USD usando KMS CMK estándar)
- AWS WAF Enterprise (Bot Control + IP Reputation) + CloudFront: ~$45.00 USD
- Kinesis Firehose + GuardDuty + Security Hub + CloudWatch Logs: ~$110.00 USD
- AWS Business Support (Soporte 24/7 de ingenieros AWS, SLA 1h): ~$100.00 USD
- **Total Tier 3 (con CloudHSM dedicado):** **~$2.577.00 USD / mes (~2.380.00 EUR / mes)**
- **Total Tier 3 (con KMS CMK estándar sin CloudHSM):** **~$1.425.00 USD / mes (~1.315.00 EUR / mes)**

---

## 3. Matriz Comparativa de Capacidades por Tier

| Capacidad | Tier 1: Lean Serverless | Tier 2: Industrial Hybrid | Tier 3: Mission-Critical |
|---|---|---|---|
| **Presupuesto Mensual** | ~32 € / mes | ~285 € / mes | ~1.315 - 2.380 € / mes |
| **SLA de Disponibilidad** | 99.9% (Multi-AZ estándar) | 99.95% | 99.99% (Multi-Región DR) |
| **Aislamiento de Red** | HTTPS / TLS 1.3 | VPC Privada + VPN + PrivateLink | Direct Connect + Transit Gateway + Network Firewall |
| **Motor Vectorial** | S3 + Lambda in-memory | Aurora Serverless v2 (pgvector) | OpenSearch Serverless (Vector Engine) |
| **Gobernanza de IA** | Bedrock Guardrails (PII/Secretos) | Bedrock Guardrails + Grounding | Guardrails Avanzado + Cohere Rerank + Textract |
| **Identidad** | Cognito User Pool + MFA | SSO Federado (Entra ID via SAML) | SAML 2.0 + SCIM + Acceso Condicional Intune |
| **Integración SIEM** | CloudWatch Logs (14 días) | CloudWatch Logs (30 días) | Kinesis Firehose -> Splunk / Wazuh / Datadog |
| **Criptografía** | AWS KMS CMK con rotación | AWS KMS CMK con rotación | KMS Multi-Region o AWS CloudHSM (FIPS 140-2 L3) |
| **Resiliencia Local** | Requiere conexión a Internet | Requiere enlace VPN de planta | Nodo Edge en planta (Greengrass/Outposts) |

---

## 4. Retorno de Inversión (Business Case) para la Dirección de Damm

Cualquiera de los tres tiers presenta un retorno de inversión inmediato cuando se compara con los costes reales de inactividad de una fábrica de bebidas:

- **Coste de Parada de Línea:** Una línea de embotellado de alta velocidad en Damm produce decenas de miles de botellas por hora. Una parada no programada por una avería mecánica o eléctrica no diagnosticada supone costes estimados de **10.000 a 45.000 EUR por hora**.
- **Amortización:** Si la plataforma permite a un operario resolver una avería un 20% más rápido gracias a los diagramas guiados y manuales indexados, **la mitigación de una sola parada de 30 minutos amortiza el coste operativo anual completo de cualquiera de los tres tiers**.
