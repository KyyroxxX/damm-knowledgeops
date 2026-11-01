import os
import json
import time
import boto3
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter(prefix="/api/v1/proposals", tags=["proposals"])

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='eu-west-1')

PROPOSALS_TABLE = os.environ.get('PROPOSALS_TABLE', 'damm-kops-proposals')
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'

AI_EVALUATOR_PROMPT = """Eres el Evaluador Inteligente de Salud Laboral, Ergonomia y Mejora Continua (Kaizen) de Damm KnowledgeOps.
Tu funcion es analizar propuestas, quejas ergonomicas y sugerencias de mejora de los operarios de fabrica.

Debes realizar un analisis riguroso y devolver OBLIGATORIAMENTE un unico objeto JSON valido con la siguiente estructura:
{
  "is_legitimate": true|false,
  "rejection_reason": "Motivo si es broma, spam, insulto o sin sentido; null si es valida",
  "category": "ERGONOMICS_HEALTH" | "SAFETY_HAZARD" | "OPERATIONAL_EFFICIENCY" | "MAINTENANCE_PREVENTIVE" | "WORKPLACE_ENVIRONMENT",
  "priority": "HIGH" | "MEDIUM" | "LOW",
  "priority_reasoning": "Explicacion objetiva de la prioridad asignada",
  "feasibility": "FEASIBLE" | "REQUIRES_ENGINEERING_STUDY" | "NOT_FEASIBLE",
  "feasibility_analysis": "Evaluacion tecnica de como podria resolverse en planta",
  "summary_for_supervisor": "Resumen ejecutivo de 2 lineas claro y directo para el responsable de planta",
  "recommended_action": "Accion concreta inmediata sugerida (ej. instalar plataforma regulable, recolocar contenedor, etc.)"
}

CRITERIOS DE PRIORIDAD:
- HIGH: Todo lo que implique dolor corporal, malas posturas repetitivas (ergonomia), sobreesfuerzos lumbares/cervicales, o riesgos de seguridad y atrapamiento.
- MEDIUM: Ineficiencias operativas notables, desplazamientos innecesarios o mantenimiento preventivo.
- LOW: Mejoras menores de confort que no afectan a la salud ni a la operacion critica.

Si el mensaje es ofensivo, una broma absurda o spam que no tiene que ver con el trabajo, marca is_legitimate: false y prioridad LOW.

PROTECCION DE PRIVACIDAD:
Si se indica que la propuesta es anonima, NUNCA incluyas nombres propios ni referencias a personas concretas en summary_for_supervisor ni en recommended_action."""

class ProposalSubmitRequest(BaseModel):
    user_id: Optional[str] = "anonimo"
    author_name: Optional[str] = None
    is_anonymous: bool = True  # Opcion del trabajador: Anonimo para evitar represalias o Identificado para reconocimiento
    department: str = "envasado"
    workstation: Optional[str] = "linea_general"
    proposal_text: str = Field(..., min_length=5, max_length=2000)

class ProposalReviewRequest(BaseModel):
    status: str  # APPROVED, IN_PROGRESS, IMPLEMENTED, REJECTED
    supervisor_notes: str

def analyze_proposal_with_ai(text: str, department: str, workstation: str, is_anonymous: bool = True) -> dict:
    prompt_content = f"""Propuesta del operario:
Departamento: {department}
Puesto de trabajo / Maquina: {workstation}
Modalidad de privacidad: {"ANONIMA (No revelar nombres)" if is_anonymous else "IDENTIFICADA"}
Mensaje:
{text}"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.1,
        "system": AI_EVALUATOR_PROMPT,
        "messages": [
            {"role": "user", "content": prompt_content}
        ]
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response['body'].read())
        raw_reply = result['content'][0]['text'].strip()

        # Extraer JSON de la respuesta
        start = raw_reply.find('{')
        end = raw_reply.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(raw_reply[start:end])
    except Exception as e:
        print(f"Error analizando propuesta con Bedrock: {e}")

    # Fallback determinista en caso de fallo
    return {
        "is_legitimate": True,
        "rejection_reason": None,
        "category": "ERGONOMICS_HEALTH" if any(w in text.lower() for w in ["brazo", "espalda", "agachar", "dolor", "postura"]) else "OPERATIONAL_EFFICIENCY",
        "priority": "HIGH" if any(w in text.lower() for w in ["danyo", "dano", "dolor", "peligro", "espalda"]) else "MEDIUM",
        "priority_reasoning": "Evaluacion de contingencia por heuristica de palabras clave",
        "feasibility": "FEASIBLE",
        "feasibility_analysis": "Requiere revision directa por el supervisor de turno",
        "summary_for_supervisor": text[:150] + "...",
        "recommended_action": "Inspeccion presencial del puesto de trabajo"
    }

@router.post("/submit")
def submit_proposal(data: ProposalSubmitRequest):
    table = dynamodb.Table(PROPOSALS_TABLE)
    ts = int(time.time())
    prop_id = f"PROP#{ts}"

    # Evaluacion con Inteligencia Artificial teniendo en cuenta privacidad
    ai_evaluation = analyze_proposal_with_ai(
        data.proposal_text,
        data.department,
        data.workstation,
        is_anonymous=data.is_anonymous
    )

    status = "REJECTED_TROLL" if not ai_evaluation.get("is_legitimate", True) else "SUBMITTED"
    priority = ai_evaluation.get("priority", "MEDIUM")

    # Tratamiento de identidad segun la eleccion del trabajador
    if data.is_anonymous:
        author_display = "Operario Anonimo"
        stored_user_id = "ANONYMOUS"
    else:
        author_display = data.author_name or data.user_id or "Operario Identificado"
        stored_user_id = data.user_id or "identificado"

    item = {
        "PK": prop_id,
        "SK": f"STATUS#{status}",
        "GSI1PK": f"DEPT#{data.department}",
        "GSI1SK": f"PRIORITY#{priority}#{ts}",
        "user_id": stored_user_id,
        "author_display": author_display,
        "is_anonymous": data.is_anonymous,
        "department": data.department,
        "workstation": data.workstation,
        "raw_text": data.proposal_text,
        "status": status,
        "category": ai_evaluation.get("category", "OPERATIONAL_EFFICIENCY"),
        "priority": priority,
        "priority_reasoning": ai_evaluation.get("priority_reasoning", ""),
        "feasibility": ai_evaluation.get("feasibility", "FEASIBLE"),
        "feasibility_analysis": ai_evaluation.get("feasibility_analysis", ""),
        "summary_for_supervisor": ai_evaluation.get("summary_for_supervisor", ""),
        "recommended_action": ai_evaluation.get("recommended_action", ""),
        "is_legitimate": ai_evaluation.get("is_legitimate", True),
        "created_at": ts
    }

    table.put_item(Item=item)

    return {
        "proposal_id": prop_id,
        "status": status,
        "priority": priority,
        "category": item["category"],
        "is_anonymous": data.is_anonymous,
        "author_display": author_display,
        "summary_for_supervisor": item["summary_for_supervisor"],
        "message": "Propuesta analizada y registrada exitosamente para revision de los responsables de planta."
    }

@router.get("/supervisor")
def list_proposals_for_supervisor(department: Optional[str] = None, priority: Optional[str] = None):
    table = dynamodb.Table(PROPOSALS_TABLE)

    if department:
        response = table.query(
            IndexName="GSI1",
            KeyConditionExpression="GSI1PK = :dept",
            ExpressionAttributeValues={":dept": f"DEPT#{department}"}
        )
        items = response.get("Items", [])
    else:
        response = table.scan(Limit=50)
        items = response.get("Items", [])

    # Filtrar trolls rechazados por defecto a menos que se pidan explicitamente
    filtered = [it for it in items if it.get("status") != "REJECTED_TROLL"]

    if priority:
        filtered = [it for it in filtered if it.get("priority") == priority]

    # Ordenar por prioridad (HIGH primero) y fecha mas reciente
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    filtered.sort(key=lambda x: (priority_order.get(x.get("priority", "LOW"), 3), -x.get("created_at", 0)))

    return {
        "total": len(filtered),
        "proposals": filtered
    }

@router.patch("/{proposal_id}/review")
def review_proposal(proposal_id: str, review: ProposalReviewRequest):
    table = dynamodb.Table(PROPOSALS_TABLE)
    ts = int(time.time())

    # Buscar la propuesta para obtener su clave primaria
    response = table.scan(
        FilterExpression="PK = :pk",
        ExpressionAttributeValues={":pk": proposal_id}
    )
    items = response.get("Items", [])
    if not items:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    current_item = items[0]
    old_sk = current_item["SK"]

    # Actualizar estado
    table.delete_item(Key={"PK": proposal_id, "SK": old_sk})
    current_item["SK"] = f"STATUS#{review.status}"
    current_item["status"] = review.status
    current_item["supervisor_notes"] = review.supervisor_notes
    current_item["reviewed_at"] = ts

    table.put_item(Item=current_item)

    return {
        "proposal_id": proposal_id,
        "new_status": review.status,
        "message": "Estado de propuesta actualizado por el supervisor"
    }

@router.get("/campaign/active")
def get_active_campaign():
    return {
        "campaign_id": "CAMP-2026-Q4",
        "title": "Campana Kaizen & Ergonomia: Tu Salud y Comodidad en Planta Importan",
        "description": "Desde la direccion de Damm te animamos a compartir cualquier incomodidad fisica, malas posturas o mejoras en tu puesto de envasado y mantenimiento. La IA evaluara tu propuesta de forma constructiva para implementar mejoras inmediatas.",
        "reward_note": "Las mejores propuestas ergonomicas implantadas reciben reconocimiento en el Comite de Seguridad y Salud.",
        "end_date": "2026-12-31"
    }
