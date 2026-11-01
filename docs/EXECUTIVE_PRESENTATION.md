# Presentacion Ejecutiva del Proyecto: Damm KnowledgeOps

> [!IMPORTANT] Alcance de la Presentacion
> Documento de presentacion de la solucion propuesta para el reto de innovacion abierta **MetròpolisFPLab** presentado por **Damm**.
> Sintetiza la vision estrategica, la resolucion de la problematica industrial, los modulos funcionales (incluyendo la voz del operario y ergonomia), la arquitectura cloud serverless y el modelo de escalado por tiers.

---

## 1. Contexto Empresarial y Reto Planteado

### El Contexto en Planta Industrial (Ej. Fabrica de El Prat de Llobregat):
La elaboracion y envasado continuo de cerveza a escala masiva demanda lineas automatizadas de altisima velocidad (llenadoras, taponadoras, etiquetadoras, encajonadoras y paletizadoras). En este entorno altamente competitivo, dos retos impactan directamente en la cuenta de resultados y en el clima laboral:

1. **Relevo Generacional y Fuga del Conocimiento Tacito:**
   Los operarios y mecanicos senior acumulan decadas de experiencia resolviendo averias complejas "por sonido, vibracion y ojo clinico". Cuando estos profesionales se jubilan o cambian de turno, ese conocimiento no se encuentra documentado formalmente y se pierde.
2. **Coste Critico de las Paradas no Planificadas:**
   Cada minuto de linea parada en embotellado supone miles de euros de lucro cesante y mermas de producto. Los operarios noveles tardan excesivo tiempo en localizar manuales tecnicos de 400 paginas o diagnosticar el codigo de error exacto.
3. **Ergonomia, Seguridad y la "Voz del Operario" (Kaizen Continuo):**
   Quienes mejor conocen las ineficiencias ergonomicas y riesgos potenciales son los trabajadores de linea (ej. posturas forzadas repetitivas, estiramientos de brazo innecesarios, valvulas de dificil acceso). Históricamente, las sugerencias no tenian un cauce digital agil, estructurado ni confidencial para llegar a la direccion tecnica con priorizacion objetiva.

---

## 2. La Solucion: Damm KnowledgeOps

**Damm KnowledgeOps** es una plataforma cloud-native inteligente disenada para unificar el conocimiento operativo, acelerar la capacitacion, asistir en la resolucion de incidencias y dar voz estructurada a la plantilla de fabricas.

```
+===================================================================================================+
|                                  DAMM KNOWLEDGEOPS PLATFORM                                       |
+===================================================================================================+
|                                                                                                   |
|   [ 1. CAPACITACION ]         [ 2. RESOLUCION AVERIAS ]         [ 3. VOZ DEL OPERARIO & KAIZEN ]  |
|   Rutas de aprendizaje        Asistente RAG industrial          Canal ergonomia y mejoras         |
|   Quizzes procedurales        Citacion estricta manuales        Opcion anonima o identificada     |
|   Onboarding acelerado        Anti-alucinacion y seguridad      Filtro troll y scoring por IA     |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
|   [ NUCLEO DE SEGURIDAD & IA RESPONSABLE: AMAZON BEDROCK + GUARDRAILS + ZERO PRODUCTION DATA ]   |
+===================================================================================================+
```

---

## 3. Modulos Funcionales Principales

### Modulo A: Identidad y Gobierno RBAC (Cognito)
- Segregacion por perfiles de usuario: `Employee` (operario), `Supervisor` (jefe de turno/linea), `Expert` (ingeniero validador) y `Admin`.
- Autenticacion segura mediante JWT y soporte para federacion corporativa (Microsoft Entra ID / SAML).

### Modulo B: Ingestion y Gestion del Conocimiento
- Ingestion controlada de manuales tecnicos (PDF/TXT) en Amazon S3 bajo cifrado KMS CMK.
- Extraccion, segmentacion semantica y vectorizacion (Titan Embeddings v2).
- Flujo de **Doble Aprobacion Humana**: ningun fragmento esta activo hasta que un `Expert` lo valida.

### Modulo C: Asistente Conversacional Industrial Anti-Alucinacion
- Interfaz en lenguaje natural orientada a operarios en linea (tablets industriales).
- **Grounding matematico estricto**: el modelo unicamente responde en base a los fragmentos aprobados inyectados, citando documento y seccion.
- Si falta informacion o la consulta involucra riesgos criticos (ej. alta tension o vapor), el asistente se abstiene y escala al responsable humano.

### Modulo D: Resolucion Guiada de Averias
- Catalogo de incidencias por equipo y codigo de alarma.
- Pasos de comprobacion secuenciales para diagnósticos rapidos.
- Registro historico para retroalimentar la base de conocimiento de planta.

### Modulo E: Formacion Operativa y Evaluacion Continua
- Rutas formativas interactivas por puesto de trabajo.
- Quizzes automatizados generados a partir de los procedimientos operativos estandar (SOPs).

### Modulo F: Auditoria y DevSecOps
- Registro inmutable de consultas y acciones en Amazon CloudWatch / DynamoDB.
- Control exhaustivo de costes mediante alertas preventivas de facturacion.

### Modulo G: Kaizen, Ergonomia y Voz del Operario (Novedad Destacada)
- Canal conversacional independiente donde los operarios pueden proponer mejoras de su entorno laboral (ergonomia, riesgos de sobreesfuerzo, accesibilidad, optimizacion de movimientos).
- **Eleccion de Privacidad**: El operario decide en cada propuesta si desea enviar su nombre o mantenerla 100% anonima.
- **Filtrado Inteligente con Bedrock (Claude 3 Haiku)**:
  - Deteccion y descarte automatico de spam, quejas vacias o contenido improcedente ("trolls").
  - Categorizacion automatica: `ERGONOMICS_HEALTH`, `SAFETY_HAZARD`, `OPERATIONAL_EFFICIENCY`.
  - Priorizacion automatica (`HIGH`, `MEDIUM`, `LOW`) segun impacto en la salud y viabilidad tecnica.
- **Panel de Revision para Supervisores**: Vista consolidada donde los responsables analizan propuestas filtradas y ordenadas por prioridad para su ejecucion.
- **Campanas Activas**: Soporte para lanzar campanas periodicas desde Damm (ej. "Mes de la Ergonomia en Envasado").

---

## 4. Arquitectura Cloud Serverless y Principios Zero Trust

La plataforma se despliega como una arquitectura 100% Serverless en AWS:

- **Coste Cero en Reposo (Scale to Zero)**: Sin servidores EC2 encendidos ni clusters sobredimensionados; el coste de computo solo se genera durante la atencion de peticiones.
- **Almacenamiento Cifrado**: Cifrado en reposo con claves KMS CMK y cifrado en transito obligatorio TLS 1.3.
- **Aislamiento de Produccion (Zero Production Data)**: El entorno de demostracion utiliza unicamente manuales y datos sinteticos basados en especificaciones genericas de maquinaria.

---

## 5. Ingenieria de Costes y Propuestas de Escalado

Para el desarrollo y validacion inicial, la plataforma opera bajo un presupuesto estricto de **0 a 5 EUR / mes**.

Para la adopcion formal en las plantas de Damm, se estructuran 3 propuestas de escalado:

1. **Tier 1 — Lean Serverless (~32 EUR/mes):**
   - 100% Serverless Pay-per-Use, Bedrock Guardrails, busqueda vectorial en memoria con S3 KMS, DynamoDB On-Demand y Cognito.
   - Ideal para lineas piloto o aulas de formacion.
2. **Tier 2 — Industrial Hybrid (~285 EUR/mes):**
   - VPC privada con VPN a fabricas, endpoints PrivateLink (cero transito por Internet publico), Aurora Serverless v2 PostgreSQL con `pgvector`, federacion SSO con Microsoft Entra ID y AWS WAF.
   - Ideal para 1-2 plantas productivas (El Prat y Santa Coloma).
3. **Tier 3 — Mission-Critical Multi-Plant (~1.315 - 2.380 EUR/mes):**
   - Landing Zone multi-cuenta con AWS Control Tower, Bedrock Knowledge Bases con OpenSearch Serverless, AWS Direct Connect redundante, AWS Network Firewall, exportacion a SIEM (Splunk/Wazuh), CloudHSM FIPS 140-2 Nivel 3 y Disaster Recovery multi-region.
   - Cumplimiento normativo europeo: **NIS 2**, **ISO 27001** y **ENS**.

---

## 6. Impacto y Valor Aportado a Damm

- **Reduccion del MTTR (Mean Time to Repair)**: Disminucion de hasta un 35% en el tiempo de diagnostico de averias complejas.
- **Reduccion de la Curva de Onboarding**: Capacitacion de nuevos operarios hasta un 50% mas rapida mediante guias interactivas.
- **Prevencion de Bajas Laborales por Sobreesfuerzo**: Canal directo de deteccion temprana de riesgos ergonomicos antes de que deriven en lesiones musculoesqueleticas.
- **Gobernanza y Cumplimiento**: Eliminacion del riesgo de fugas de propiedad industrial mediante barreras matematicas y perimetrales en IA.
