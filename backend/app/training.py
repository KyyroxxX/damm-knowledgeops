import os
import time
import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/training", tags=["training"])
dynamodb = boto3.resource('dynamodb')
TRAINING_TABLE = os.environ.get('TRAINING_TABLE', 'damm-kops-training')

class AssessmentSubmit(BaseModel):
    user_id: str
    module_id: str
    score: int
    max_score: int

@router.get("/modules")
def list_training_modules(department: str = "envasado"):
    modules = [
        {
            "module_id": "MOD-01",
            "title": "Seguridad Operacional y Parada de Emergencia",
            "department": department,
            "estimated_minutes": 25,
            "doc_reference": "manual_seguridad_loto.pdf"
        },
        {
            "module_id": "MOD-02",
            "title": "Operacion y Calibracion de Llenadora Krones",
            "department": department,
            "estimated_minutes": 45,
            "doc_reference": "manual_llenadora_krones.pdf"
        }
    ]
    return {"department": department, "modules": modules}

@router.post("/assessments/submit")
def submit_assessment(data: AssessmentSubmit):
    table = dynamodb.Table(TRAINING_TABLE)
    ts = int(time.time())
    percentage = round((data.score / data.max_score) * 100, 2)
    passed = percentage >= 75.0
    
    item = {
        "PK": f"USER#{data.user_id}",
        "SK": f"MODULE#{data.module_id}#{ts}",
        "module_id": data.module_id,
        "score": data.score,
        "max_score": data.max_score,
        "percentage": str(percentage),
        "passed": passed,
        "completed_at": ts
    }
    table.put_item(Item=item)
    return {"status": "recorded", "passed": passed, "percentage": percentage}

@router.get("/progress/{user_id}")
def get_user_progress(user_id: str):
    table = dynamodb.Table(TRAINING_TABLE)
    response = table.query(
        KeyConditionExpression="PK = :u",
        ExpressionAttributeValues={":u": f"USER#{user_id}"}
    )
    return {"user_id": user_id, "history": response.get("Items", [])}
