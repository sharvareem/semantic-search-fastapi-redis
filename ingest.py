from openai import OpenAI
import redis
import json
from typing import List

# Initialize the OpenAI client with API key
openai_api_key = "test_key"  # Replace with your OpenAI API key
client = OpenAI(api_key=openai_api_key)

# Initialize Redis client (replace with your Redis details if necessary)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Function to chunk the text into smaller pieces
def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Chunks a text into parts of chunk_size.
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

# Function to get OpenAI embeddings for each chunk using the latest API format
def get_embedding(text: str, model="text-embedding-ada-002") -> List[float]:
    """
    Returns the embedding for a given text chunk using OpenAI embeddings.
    """
    text = text.replace("\n", " ")  # Ensure the text is suitable for the model
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# Function to insert document chunks into Redis with embeddings
def insert_document_in_redis(doc_id: str, text: str):
    """
    Insert a document's chunks and their embeddings into Redis.
    """
    # Chunk the document
    chunks = chunk_text(text)
    
    # For each chunk, generate embedding and store it in Redis
    for idx, chunk in enumerate(chunks):
        chunk_id = f"{doc_id}_chunk_{idx}"
        embedding = get_embedding(chunk)
        
        # Store the embedding in Redis (you can store it in JSON format)
        redis_client.hset(chunk_id, mapping={
            "chunk": chunk,
            "embedding": json.dumps(embedding)  # Store the embedding as a JSON string
        })
        print(f"Inserted chunk {idx} into Redis.")

# Example usage
if __name__ == "__main__":
    # Sample text taken from Wikipedia
    document_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence 
    displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": 
    any system that perceives its environment and takes actions that maximize its chance of achieving its goals. 
    Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic 
    "cognitive" functions that humans associate with the human mind, such as "learning" and "problem-solving".
    
    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from 
    the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is 
    frequently excluded from things considered to be AI, having become a routine technology. Modern machine 
    capabilities generally classified as AI include successfully understanding human speech, competing at the 
    highest level in strategic game systems (such as chess and Go), autonomously operating cars, intelligent 
    routing in content delivery networks, and military simulations.
    """

    # Insert the document into Redis
    insert_document_in_redis("doc_001", document_text)
