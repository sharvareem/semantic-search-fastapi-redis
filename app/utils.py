import redis
import openai
import json
import numpy as np
from typing import List 

openai_api_key = "test_key"  # Replace with your OpenAI API key


# Function to get cached response if available
def get_cached_response(redis_client: redis.Redis, text: str):
    cached_response = redis_client.get(f"cache:{text}")
    if cached_response:
        return json.loads(cached_response)
    return None

# Function to cache response for future queries
def cache_response(redis_client: redis.Redis, text: str, response: dict, ttl: int = 3600):
    redis_client.setex(f"cache:{text}", ttl, json.dumps(response))

# Function to implement rate-limiting per user
def rate_limit_user(redis_client: redis.Redis, user_id: str, limit: int = 5, ttl: int = 3600):
    user_key = f"user:{user_id}"
    request_count = redis_client.get(user_key)
    
    if request_count and int(request_count) >= limit:
        return False
    
    if request_count:
        redis_client.incr(user_key)
    else:
        redis_client.setex(user_key, ttl, 1)
    
    return True

# Function to get embedding from OpenAI
def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# Function to calculate cosine similarity between two vectors
def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
