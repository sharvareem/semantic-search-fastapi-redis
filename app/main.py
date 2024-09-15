from fastapi import FastAPI, HTTPException, Request
from typing import List
import time
import redis
import json
from app.utils import get_cached_response, cache_response, rate_limit_user, get_embedding, cosine_similarity

# Initialize FastAPI app and Redis client
app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# /health endpoint
@app.get("/health")
def health_check():
    print("Health check endpoint called")
    return {"status": "API is active"}

# /search endpoint
@app.post("/search")
async def search(request: Request, text: str, top_k: int = 5, threshold: float = 0.75, user_id: str = "default_user"):
    start_time = time.time()
    print(f"Search request received with text: {text}, top_k: {top_k}, threshold: {threshold}, user_id: {user_id}")
    
    # Check rate limit
    if not rate_limit_user(redis_client, user_id):
        print(f"Rate limit exceeded for user: {user_id}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    print(f"Rate limit check passed for user: {user_id}")
    
    # Check for cached response
    cached_result = get_cached_response(redis_client, text)
    if cached_result:
        print(f"Cache hit for text: {text}")
        return cached_result
    print(f"Cache miss for text: {text}")
    
    # Generate embedding for the query text
    query_embedding = get_embedding(text)
    print(f"Generated query embedding for text: {text}")
    
    # Search in Redis vector store and find top_k matches
    all_results = []
    for key in redis_client.scan_iter("doc_*"):  # Iterate through all documents in Redis
        doc_embedding = json.loads(redis_client.hget(key, "embedding"))
        similarity = cosine_similarity(query_embedding, doc_embedding)
        print(f"Calculated similarity for doc_id: {key}, similarity: {similarity}")
        
        if similarity >= threshold:
            all_results.append({
                "doc_id": key,
                "similarity": similarity,
                "chunk": redis_client.hget(key, "chunk").decode("utf-8")
            })
            print(f"Doc added to results: {key}")
    
    # Sort results based on similarity and get the top_k results
    all_results = sorted(all_results, key=lambda x: x["similarity"], reverse=True)[:top_k]
    print(f"Top {top_k} results retrieved")
    
    response = {
        "query": text,
        "results": all_results,
        "inference_time": time.time() - start_time
    }
    print(f"Response generated: {response}")

    # Cache the response
    cache_response(redis_client, text, response)
    print(f"Response cached for text: {text}")

    return response

# Dockerize the FastAPI app
