import os
import time
import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])
dynamodb = boto3.resource('dynamodb')
INCIDENTS_TABLE = os.environ.get('INCIDENTS_TABLE', 'damm-kops-incidents')

class IncidentCreate(BaseModel):
    machine_id: str
    department: str
    title: str
    description: str
    severity: str  # P1, P2, P3, P4

class IncidentResolve(BaseModel):
    resolution_steps: str
    promote_to_sop: bool = False

@router.post("")
def register_incident(data: IncidentCreate):
    table = dynamodb.Table(INCIDENTS_TABLE)
    ts = int(time.time())
    inc_id = f"INC#{ts}"
    
    item = {
        "PK": inc_id,
        "SK": "STATUS#OPEN",
        "GSI1PK": f"MACHINE#{data.machine_id}",
        "GSI1SK": "STATUS#OPEN",
        "machine_id": data.machine_id,
        "department": data.department,
        "title": data.title,
        "description": data.description,
        "severity": data.severity,
        "status": "OPEN",
        "created_at": ts
    }
    table.put_item(Item=item)
    return {"incident_id": inc_id, "status": "OPEN"}

@router.get("")
def list_incidents(machine_id: str = None):
    table = dynamodb.Table(INCIDENTS_TABLE)
    if machine_id:
        response = table.query(
            IndexName="GSI1",
            KeyConditionExpression="GSI1PK = :m",
            ExpressionAttributeValues={":m": f"MACHINE#{machine_id}"}
        )
    else:
        response = table.scan(Limit=20)
    return {"incidents": response.get("Items", [])}

@router.post("/{incident_id}/resolve")
def resolve_incident(incident_id: str, data: IncidentResolve):
    table = dynamodb.Table(INCIDENTS_TABLE)
    new_status = "PENDING_SOP_REVIEW" if data.promote_to_sop else "RESOLVED"
    
    table.update_item(
        Key={"PK": incident_id, "SK": "STATUS#OPEN"},
        UpdateExpression="SET #st = :s, resolution_steps = :r, resolved_at = :t",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={
            ":s": new_status,
            ":r": data.resolution_steps,
            ":t": int(time.time())
        }
    )
    return {"incident_id": incident_id, "status": new_status}
