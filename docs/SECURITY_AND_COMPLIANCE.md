# Security, Compliance & Data Governance — Damm KnowledgeOps

> [!IMPORTANT] Proposito de este Documento
> Este documento detalla la postura de seguridad, el gobierno del dato y los controles de cumplimiento normativo implementados en **Damm KnowledgeOps**. Explica formalmente por que este repositorio de investigacion es completamente seguro para su exposicion publica y como garantiza la total inocuidad respecto a los activos reales de **Damm**.

---

## 1. Politica de Datos Sinteticos (Zero Production Data)

Para cumplir con los estandares eticos de innovacion abierta en el reto **MetròpolisFPLab**:

1. **Aislamiento Total de Activos:** Este proyecto **no tiene conexion con ninguna red, base de datos, API interna ni entorno de produccion de Damm**.
2. **Documentacion 100% Simulada:** Todos los procedimientos operativos (SOP), codigos de error de maquinaria (e.g. lineas de embotellado Krones, transportadores de palets, sistemas CIP de limpieza) y preguntas de evaluacion son **generados sinteticamente** o extraidos de manuales genericos publicos de fabricantes de maquinaria industrial.
3. **Ausencia de Propiedad Intelectual Privada:** No se incluyen recetas de elaboracion cervecera, proporciones de materias primas, parametros de fermentacion confidenciales ni planos industriales propietarios.
4. **Datos de Personal Ficticios:** No se utilizan nombres, correos electronicos ni identificadores de empleados reales de Damm. Todos los usuarios de prueba corresponden a cuentas sinteticas de laboratorio (`op_alex`, `supervisor_demo`, etc.).

---

## 2. Prevencion de Fugas de Informacion y Secretos

El repositorio implementa una estrategia multicapa para garantizar que ninguna credencial pueda ser expuesta:

```
[ Desarrollador ] ---> [ .gitignore Estricto ] ---> [ Gitleaks (Pre-Commit / CI) ] ---> [ GitHub Public ]
                               |                                 |
                     Bloquea *.env, *.pem,             Analiza entropia y
                     *.key, *.tfstate, .aws/           patrones de API keys
```

### Controles Automatizados en CI/CD:
* **Gitleaks:** Escaneo criptografico de patrones de claves privadas, access keys de AWS y tokens de Cognito en cada commit.
* **Semgrep SAST:** Analisis estatico del codigo fuente para prevenir inyecciones NoSQL en DynamoDB y vulnerabilidades en FastAPI.
* **Trivy:** Escaneo de dependencias en `requirements.txt` frente a bases de datos de vulnerabilidades conocidas (CVE).
* **Checkov:** Auditoria estatica de seguridad sobre los manifiestos de Terraform (garantizando bloqueo de acceso publico en S3 y cifrado KMS).

---

## 3. Modelo de Amenazas de IA (OWASP Top 10 for LLM Applications)

| Vector de Riesgo | Amenaza Potencial | Mitigacion Arquitectonica en Damm KnowledgeOps |
|---|---|---|
| **LLM01: Inyeccion de Prompts** | Un usuario intenta manipular el modelo para que emita ordenes daninas en planta. | **Delimitacion Estricta XML:** El contexto recuperado y la consulta del tecnico se inyectan en etiquetas separadas (`<approved_procedures>` vs `<technician_question>`). El prompt de sistema tiene prioridad inmutable. |
| **LLM02: Manejo Inseguro de Salidas** | El modelo genera respuestas con scripts o caracteres de control maliciosos. | **Sanitizacion en Renderizado:** El frontend Next.js escapa de forma segura el markdown y bloquea la ejecucion de scripts HTML arbitrarios. |
| **LLM03: Envenenamiento de Datos** | Un atacante sube manuales falsos para inducir fallos en la maquinaria. | **Flujo de Doble Aprobacion:** Ningun manual subido a S3 se indexa vectorialmente hasta que un usuario autenticado con el rol `Expert` firma el estado `approved` en DynamoDB. |
| **LLM06: Divulgacion de Informacion Sensible** | El LLM revela secretos o datos internos que estaban dentro de los manuales. | **Filtro de Pre-Ingesta:** Expresiones regulares que detectan y anonimizan IPs, contrasenas y tokens antes del proceso de embedding en Titan v2. |
| **LLM08: Exceso de Agencia** | El asistente ejecuta acciones no autorizadas en PLCs o actuadores fisicos de fabrica. | **Modo de Solo Consulta (Read-Only):** El asistente es puramente consultivo; no dispone de integraciones directas con sistemas SCADA o PLCs. Toda accion fisica en planta requiere intervencion humana presencial. |

---

## 4. Controles Criptograficos y de Acceso

* **Cifrado en Reposo:** Todos los objetos almacenados en Amazon S3 y las tablas de Amazon DynamoDB se cifran mediante claves gestionadas por el cliente (CMK) en **AWS Key Management Service (KMS)** con rotacion automatica anual de claves.
* **Cifrado en Transito:** Se aplica una politica de bucket estricta que deniega cualquier conexion que no utilice **TLS 1.2 o TLS 1.3** (`aws:SecureTransport = false`).
* **Control de Acceso Basado en Roles (RBAC):** Amazon Cognito User Pools emite tokens firmados criptograficamente con claims de pertenencia a grupo (`Employee`, `Supervisor`, `Expert`, `Admin`). Los endpoints de API Gateway y FastAPI verifican estos tokens antes de ejecutar cualquier logica de negocio.

---

## 5. Declaracion de Transferencia Segura

Este diseno permite que **Damm traslade y despliegue el sistema al 100% dentro de su propio tenant de AWS**:
* Los manifiestos de Terraform estan completamente parametrizados mediante variables (`aws_region`, `environment`, `project_name`).
* No existen identificadores de cuenta de AWS hardcodeados; Terraform utiliza la llamada dinamica `data.aws_caller_identity.current.account_id`.
* En un entorno de produccion dentro de Damm, los buckets sinteticos se reemplazan simplemente cargando la documentacion tecnica corporativa real validada por sus propios ingenieros.
