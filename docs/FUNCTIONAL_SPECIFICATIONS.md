# Especificaciones Funcionales — Damm KnowledgeOps

> [!NOTE] Objeto del Documento
> Especificacion detallada de los modulos funcionales de la plataforma **Damm KnowledgeOps**, describiendo flujos de usuario, parametros de entrada, logica de negocio y salidas esperadas.

---

## Modulo A: Identidad, Gobierno y RBAC

### Perfiles y Niveles de Acceso:
1. **Employee (Operario / Tecnico de Planta):**
   - Acceso al Asistente Conversacional para consulta de procedimientos.
   - Acceso a guias interactivas de resolucion de averias.
   - Realizacion de modulos de capacitacion y quizzes.
   - Envio de propuestas en el canal Kaizen / Ergonomia (con opcion anonima o identificada).
2. **Supervisor (Jefe de Turno / Responsable de Linea):**
   - Todo lo anterior.
   - Visualizacion y gestion del panel de propuestas de operarios (ordenadas por prioridad y viabilidad).
   - Aprobacion o descarte de propuestas Kaizen con justificacion tecnica.
   - Lanzamiento de campanas de participacion operaria.
   - Recepcion de escalados de seguridad cuando el asistente se abstiene en consultas de alto riesgo.
3. **Expert (Ingeniero Especialista / Validador Tecnico):**
   - Todo lo anterior.
   - Aprobacion formal de nuevos manuales y procedimientos operativos estandar (SOPs) subidos a la base de conocimiento antes de su publicacion.
4. **Admin (Administrador de Plataforma / Ciberseguridad):**
   - Gestion integral de usuarios, politicas de retencion de logs y configuracion de Bedrock Guardrails.

---

## Modulo B: Ingestion y Gestion del Conocimiento Industrial

### Flujo de Trabajo:
1. Carga de manuales en formato PDF o TXT al repositorio seguro.
2. Procesamiento y segmentacion semantica (chunking de 500 palabras con solapamiento de 50).
3. Generacion de representaciones vectoriales densas (Amazon Titan Embeddings v2 de 1024 dimensiones).
4. Asignacion automatica de estado `PENDING_EXPERT_APPROVAL` en metadatos.
5. Revision y firma criptografica por un usuario con rol `Expert`.
6. Publicacion en el indice activo bajo estado `APPROVED`.

---

## Modulo C: Asistente Conversacional Grounded (Anti-Alucinacion)

### Garantias de Fiabilidad:
- **Grounding Restrictivo:** El modelo de lenguaje (Amazon Bedrock Claude 3 / 3.5) responde estrictamente dentro del contexto de procedimientos aprobados.
- **Citacion Obligatoria:** Cada respuesta tecnica incluye la identificacion del documento, seccion y fragmento de origen.
- **Abstencion Segura:** Si la similitud coseno es inferior al umbral minimo o si la intervencion entraña peligro de alta gravedad (ej. consignacion electrica LOTO, fluidos a presion), el sistema declina responder y escala la incidencia al supervisor.

---

## Modulo D: Resolucion Guiada de Averias (Troubleshooting)

### Capacidades:
- Busqueda rapida por codigo de averia o sintoma mecanico/electrico.
- Arbol de decisiones con verificaciones secuenciales ("Si la presion es < 2 bar, verificar valvula V-12").
- Registro de resolucion y enriquecimiento continuo de la base de conocimiento con lecciones aprendidas.

---

## Modulo E: Formacion Operativa y Evaluacion Continua

### Capacidades:
- Itinerarios formativos adaptados al tipo de linea (embotellado vidrio, lata, barril).
- Generacion dinamica de cuestionarios a partir de manuales reales.
- Registro historico del grado de capacitacion y competencias adquiridas.

---

## Modulo F: Auditoria, Seguridad y Control de Costes

### Capacidades:
- Trazabilidad completa de consultas para auditorias de calidad y seguridad industrial.
- Monitorizacion de alertas y cumplimiento de directivas de ciberseguridad.
- Alertas automaticas de facturacion para mantener el presupuesto controlado.

---

## Modulo G: Kaizen, Ergonomia y Voz del Operario

### Justificacion:
En una fabrica cervecera de alta produccion, las mejoras mas efectivas en seguridad, salud laboral y eficiencia nacen de los operarios que operan la maquinaria dia a dia. Este modulo proporciona un canal digital directo, amigable y estructurado.

### Flujo Operativo:
1. **Canal Independiente:** El operario interactua en un chat especifico dedicado a la mejora del puesto de trabajo, separado del asistente tecnico de averias.
2. **Eleccion de Identidad:**
   - Modo Anonimo (`is_anonymous = true`): No se registra nombre, usuario ni correo; se respeta la privacidad total para propuestas delicadas.
   - Modo Identificado (`is_anonymous = false`): Se registra la identidad del empleado para reconocer su iniciativa o consultar detalles adicionales.
3. **Filtro y Evaluacion Inteligente con Bedrock:**
   - La IA analiza la propuesta para verificar que no se trate de contenido troll, spam o lenguaje inapropiado.
   - Clasifica la categoria: `ERGONOMICS_HEALTH` (ej. posturas forzadas, dolores lumbares, alcances lejanos), `SAFETY_HAZARD` (riesgo de atrapamiento, suelo resbaladizo) o `OPERATIONAL_EFFICIENCY` (ahorro de pasos, reordenacion de herramientas).
   - Determina la viabilidad y asigna una prioridad tecnica: `HIGH`, `MEDIUM` o `LOW`.
4. **Dashboard de Supervisores:**
   - Los jefes de linea visualizan las propuestas ya depuradas y priorizadas.
   - Pueden marcar estados (`PENDING_REVIEW`, `ACCEPTED`, `REJECTED`, `IN_PROGRESS`, `IMPLEMENTED`) y dejar retroalimentacion.
5. **Campanas Corporativas de Participacion:**
   - Capacidad de activar campanas tematicas periodicas desde Damm (ej. "Campana de Reduccion de Sobreesfuerzos en Paletizado").
