# Security, Compliance & Data Governance — Damm KnowledgeOps

> [!IMPORTANT] Proposito de este Documento
> Este documento detalla la postura de seguridad, el gobierno del dato y los controles de cumplimiento normativo implementados en **Damm KnowledgeOps**. Explica formalmente por que este repositorio de investigacion es completamente seguro para su exposicion publica en carteras profesionales (GitHub/LinkedIn), garantizando la total inocuidad e inviolabilidad respecto a los activos reales de **Damm**.

---

## 1. Matriz de Seguridad: Que es Publico vs. Que se Mantiene Privado

Para compatibilizar la demostracion tecnica ante reclutadores con la proteccion absoluta de la confidencialidad de Damm, el repositorio opera bajo una estricta segregacion de activos:

| Categoria | Activo Corporativo Real de Damm (100% Protegido / Inexistente en Repo) | Implementacion en este Repositorio (Publico y Seguro) |
|---|---|---|
| **Infraestructura de Red** | Redes de fabrica (OT), rangos IP internos, routers, gateways industriales, VPNs. | **Air-Gapped Cloud:** Arquitectura Serverless en cuenta AWS aislada sin conexion a ninguna red fisica o corporativa. |
| **Sistemas de Control (SCADA/PLC)** | Automatas Siemens/Rockwell, buses Profinet/Modbus, pantallas HMI de planta. | **Zero Hardware Coupling:** Sistema puramente documental en modo lectura; sin integracion con PLCs ni actuadores fisicos. |
| **Documentacion y Manuales** | Planos tecnicos confidenciales, fichas de calibracion internas, especificaciones de planta. | **Dataset Sintetico:** 100% de manuales generados por script (`generate_synthetic_docs.py`) basados en especificaciones genericas OEM. |
| **Recetas y Propiedad Intelectual** | Formulaciones de cerveza, proporciones de malta/lupulo, curvas de maceracion y fermentacion. | **Exclusion Total:** Ninguna mencion a ingredientes, recetas, quimica cervecera o metodos de elaboracion propietarios. |
| **Identidad y Personal** | Nombres de empleados, correos corporativos `@damm.com`, turnos, registros disciplinarios. | **Directorio Efimero de Pruebas:** Cuentas simuladas en Amazon Cognito (`op_alex`, `supervisor_demo`) con correos de pruebas ficticios. |
| **Credenciales y Secretos** | API Keys de produccion, claves IAM, certificados TLS corporativos, contrasenas. | **Zero Hardcoded Secrets:** Sin claves ni IDs fijos; Terraform usa `aws_caller_identity`; escaneo continuo por Gitleaks. |
| **Identificadores de Cuenta Cloud** | ID de cuenta AWS de Damm, ARNs de KMS corporativos, VPC IDs productivas. | **Parametrizacion Completa:** Modulos Terraform portables sin IDs harcodeados, listos para despliegue parametrizado. |

---

## 2. Inmunidad Frente a Reconocimiento y Ciberataques (Reconnaissance Defense)

Si un atacante externo analiza este repositorio publico buscando vectores para vulnerar a Damm, se encontrara con un entorno disenado para ser un **punto ciego (dead end)**:

1. **Ausencia de Metadatos de Infraestructura Interna:**
   - No se publican nombres de dominios internos (`*.corp.damm.es`), endpoints de intranets ni configuraciones de proxy inverso vinculadas a redes reales.
   - El archivo `.gitignore` previene la subida accidental de archivos de estado de Terraform (`*.tfstate`), que podrian contener identificadores de infraestructura.

2. **Aislamiento Criptografico en AWS:**
   - Todos los datos en reposo (DynamoDB y S3) se cifran mediante una clave de cliente gestionada (KMS CMK) creada en el entorno de desarrollo del creador.
   - La transferencia a produccion descrita en `HANDOVER_GUIDE.md` instruye a Damm a aprovisionar su propia clave KMS dentro de su cuenta corporativa, manteniendo el control criptografico total.

3. **Prevencion de Inyecciones y Fugas en el Asistente:**
   - La API de Amazon Bedrock se invoca mediante el rol IAM de ejecucion de Lambda, sin exponer API keys en codigo cliente.
   - La sanitizacion estricta de prompts previene ataques de extraccion de contexto (Prompt Leaking) o evasion de instrucciones (Jailbreaking).

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

## 5. Pipeline DevSecOps Automatizado

Cada cambio en el codigo fuente pasa por 4 fases de seguridad automatizadas en GitHub Actions antes de ser aceptado:

```
[ Git Push ]
     │
     ├── 1. Gitleaks       --> Deteccion de credenciales, access keys y certificados
     ├── 2. Semgrep SAST   --> Analisis estatico de codigo Python/FastAPI (CWE/OWASP)
     ├── 3. Trivy FS       --> Escaneo de vulnerabilidades en dependencias (CVE)
     └── 4. Checkov IaC    --> Auditoria de seguridad en manifiestos Terraform
```

---

## 6. Declaracion de Transferencia Segura

Este diseno permite que **Damm traslade y despliegue el sistema al 100% dentro de su propio tenant de AWS**:
* Los manifiestos de Terraform estan completamente parametrizados mediante variables (`aws_region`, `environment`, `project_name`).
* No existen identificadores de cuenta de AWS hardcodeados; Terraform utiliza la llamada dinamica `data.aws_caller_identity.current.account_id`.
* En un entorno de produccion dentro de Damm, los buckets sinteticos se reemplazan simplemente cargando la documentacion tecnica corporativa real validada por sus propios ingenieros.

---

## 7. Contacto de Divulgacion Responsable (Responsible Disclosure)

Si un miembro del equipo de ciberseguridad de Damm o un investigador de seguridad detecta cualquier discrepancia o aspecto susceptible de mejora en este prototipo academico:

- **Canal de Notificacion:** A traves de GitHub Issues de este repositorio o via correo electronico indicado en el perfil del autor.
- **Compromiso de Respuesta:** Revision y mitigacion inmediata en menos de 24 horas.
