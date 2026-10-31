import json
import math
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='eu-west-1')
s3 = boto3.client('s3')

EMBEDDING_MODEL_ID = 'amazon.titan-embed-text-v2:0'
SIMILARITY_THRESHOLD = 0.65

def get_query_embedding(query_text: str) -> list[float]:
    payload = json.dumps({"inputText": query_text})
    response = bedrock.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=payload,
        contentType='application/json',
        accept='application/json'
    )
    result = json.loads(response['body'].read())
    return result['embedding']

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
    return dot_product / (magnitude_v1 * magnitude_v2)

def retrieve_relevant_chunks(query: str, approved_docs_keys: list[str], processed_bucket: str, top_k: int = 3) -> list[dict]:
    query_vector = get_query_embedding(query)
    all_candidate_chunks = []

    for key in approved_docs_keys:
        try:
            resp = s3.get_object(Bucket=processed_bucket, Key=key)
            chunks = json.loads(resp['Body'].read().decode('utf-8'))
            all_candidate_chunks.extend(chunks)
        except Exception as e:
            print(f"Error loading {key}: {str(e)}")

    scored_chunks = []
    for item in all_candidate_chunks:
        score = cosine_similarity(query_vector, item['embedding'])
        if score >= SIMILARITY_THRESHOLD:
            scored_chunks.append({
                "doc_name": item['doc_name'],
                "chunk_index": item['chunk_index'],
                "text": item['text'],
                "score": round(score, 4)
            })

    scored_chunks.sort(key=lambda x: x['score'], reverse=True)
    return scored_chunks[:top_k]
