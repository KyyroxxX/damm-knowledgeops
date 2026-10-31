# Architecture & Industrial RAG Engine — Damm KnowledgeOps

> [!NOTE] Resumen de Diseno Arquitectonico
> Este documento profundiza en las decisiones tecnicas, la seleccion de servicios AWS, la ingenieria de costes y el funcionamiento matematico del motor RAG (Retrieval-Augmented Generation) implementado en **Damm KnowledgeOps**.

---

## 1. Justificacion de Decisiones Arquitectonicas

### 1.1. Por que Serverless frente a Contenedores o Instancias Permanentes
- **Coste Cero en Reposo (Scale to Zero):** Las plantas de produccion operan en turnos intensivos, pero los entornos de capacitacion y resolucion de averias sufren picos y valles de demanda. Mantener instancias EC2 o un cluster ECS Fargate acarrearia costes fijos continuos. Con **AWS Lambda + Amazon API Gateway HTTP API**, el coste en inactividad es exactamente $0.00 USD.
- **Mantenimiento Operativo Minimo:** Sin parches de sistema operativo, sin gestion de AMIs ni configuracion de autoscaling groups.

### 1.2. Por que S3 + Similitud Coseno en Memoria frente a Amazon OpenSearch
- **Optimizacion Financiera Extrema:** Un cluster de OpenSearch Serverless u OpenSearch provisionado impone un gasto minimo de ~$700 USD/mes solo por las OpenSearch Compute Units (OCUs) base.
- **Rendimiento Industrial Probado:** Para una biblioteca de planta de hasta 50.000 fragmentos (chunks) de texto, el cálculo vectorial en memoria mediante producto escalar normalizado en Python toma **menos de 40 milisegundos**.
- **Almacenamiento Cifrado en S3:** Los vectores se persisten en formato JSON comprimido en Amazon S3 bajo cifrado KMS CMK, reduciendo el coste de almacenamiento vectorial a centimos de euro al mes.

### 1.3. Por que Amazon DynamoDB en Modo On-Demand (`PAY_PER_REQUEST`)
- **Libre de Provisionamiento:** Elimina la necesidad de planificar unidades de capacidad de lectura/escritura (RCU/WCU).
- **Capa Gratuita de AWS (Free Tier):** Incluye permanentemente 25 GB de almacenamiento y 2.5 millones de lecturas/escrituras mensuales, permitiendo que la persistencia de incidentes y evaluaciones sea 100% gratuita durante el desarrollo y pruebas.

---

## 2. Flujo Integral de Ingesta y Recuperacion RAG

```
[ Manual Tecnico PDF / TXT ]
             │
             ▼
   [ S3 Bucket raw-docs ]  (Cifrado KMS CMK)
             │
             │ (S3 Event Notification: ObjectCreated)
             ▼
   [ Lambda Ingestion Worker ]
             │
             ├── 1. Chunking Semantico (500 palabras, solapamiento de 50)
             ├── 2. Filtro de Pre-Ingesta (Sanitizacion de regex y tokens)
             ├── 3. Amazon Bedrock: amazon.titan-embed-text-v2:0 (Vector 1024d)
             │
             ▼
   [ S3 Bucket processed-docs ] (Vectores + Metadatos)
             │
             ▼
   [ DynamoDB Status ] (Estado: PENDING_EXPERT_APPROVAL)
             │
             │ (Aprobacion firmada por rol Expert)
             ▼
       [ Estado: APPROVED ]
```

---

## 3. Mitigacion de Alucinaciones y Escalado a Humanos

En entornos industriales con maquinaria rotativa de alta velocidad, calderas de vapor y amoniaco para refrigeracion, una recomendacion incorrecta del asistente puede provocar accidentes graves o paradas de linea de miles de euros por minuto.

Para garantizar la seguridad operacional:

1. **Inyeccion Contextual Estricta:**
   El modelo LLM recibe el contexto encerrado entre etiquetas XML `<approved_procedures>`.
2. **Prioridad del Prompt de Sistema:**
   El prompt de sistema instruye al modelo a rechazar cualquier instruccion dentro de `<technician_question>` que contradiga las normas de seguridad.
3. **Escalado Automatico:**
   Si la consulta involucra procedimientos de alto riesgo (consignacion LOTO, apertura de valvulas a presion, intervenciones electricas >400V) o la similitud de los fragmentos recuperados es inferior a 0.70, el backend registra un evento de escalado en DynamoDB y devuelve:
   > *"No se dispone de un procedimiento validado con confianza suficiente para esta accion. Por protocolo de seguridad de planta, la consulta ha sido derivada al responsable experto del turno."*
