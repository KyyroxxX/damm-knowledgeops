import json
import os
import hashlib
import boto3
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='eu-west-1')

DOCUMENTS_TABLE = os.environ.get('DOCUMENTS_TABLE', 'damm-kops-documents')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET')
EMBEDDING_MODEL_ID = 'amazon.titan-embed-text-v2:0'

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def generate_embedding(text: str) -> list[float]:
    payload = json.dumps({"inputText": text})
    response = bedrock.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=payload,
        contentType='application/json',
        accept='application/json'
    )
    response_body = json.loads(response['body'].read())
    return response_body['embedding']

def handler(event, context):
    table = dynamodb.Table(DOCUMENTS_TABLE)
    
    for record in event.get('Records', []):
        src_bucket = record['s3']['bucket']['name']
        src_key = unquote_plus(record['s3']['object']['key'])
        
        allowed_exts = ('.txt', '.md', '.json')
        if not src_key.lower().endswith(allowed_exts):
            print(f"Skipping unsupported file extension: {src_key}")
            continue

        response = s3_client.get_object(Bucket=src_bucket, Key=src_key)
        raw_bytes = response['Body'].read()
        file_hash = hashlib.sha256(raw_bytes).hexdigest()
        text_content = raw_bytes.decode('utf-8', errors='replace')
        
        chunks = chunk_text(text_content)
        processed_chunks = []
        
        for idx, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)
            processed_chunks.append({
                "chunk_id": f"{file_hash}_{idx}",
                "doc_name": src_key,
                "chunk_index": idx,
                "text": chunk,
                "embedding": embedding
            })
            
        dest_key = f"vectors/{file_hash}.json"
        s3_client.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=dest_key,
            Body=json.dumps(processed_chunks),
            ContentType='application/json'
        )
        
        doc_id = f"DOC#{file_hash[:16]}"
        table.put_item(
            Item={
                "PK": doc_id,
                "SK": "METADATA#v1.0",
                "GSI1PK": "STATUS#pending_review",
                "GSI1SK": f"DEPARTMENT#general",
                "file_name": src_key,
                "sha256": file_hash,
                "chunk_count": len(chunks),
                "status": "pending_review",
                "storage_key": dest_key
            }
        )
        print(f"Successfully processed {src_key}: {len(chunks)} chunks generated.")

    return {"statusCode": 200, "body": json.dumps("Ingestion completed")}
