
# 21BAI1558_ML Project
This repository contains the 21BAI1558_ML project, which implements a machine learning pipeline for document ingestion, processing, and semantic search using OpenAI's embedding API and Redis for vector-based retrieval. The project also provides a FastAPI-based search service, enabling users to query documents based on semantic similarity.

# Overview
This project demonstrates a full pipeline for document embedding and semantic search. The core functionalities include:

Document Chunking and Embedding: Documents are divided into smaller text chunks, and embeddings are generated using OpenAI’s API.
Storage in Redis: The embeddings and their corresponding text chunks are stored in Redis for fast retrieval.
Search Service: The search API allows users to input a query and returns the most relevant document chunks based on semantic similarity, leveraging cosine similarity for vector comparison.
This repository is designed to provide a scalable solution for document search using semantic embeddings, allowing for quick and efficient retrieval from a large collection of documents.

# Features
Document Chunking: Splits large documents into smaller, more manageable chunks.
Embedding Generation: Utilizes OpenAI’s state-of-the-art text embedding models to convert text into high-dimensional vectors.
Vector-Based Storage: Stores embeddings in Redis for fast and scalable similarity-based retrieval.
Search API: Provides a FastAPI-powered search endpoint to return top-k semantically relevant document chunks based on user queries.

# System Requirements
This project requires the following dependencies to run:

Python 3.7 or higher
Redis (used for storing document embeddings)
OpenAI API Key (for embedding generation)
Required Python Packages:
openai
redis
fastapi
uvicorn
typing
Installation
Step 1: Clone the Repository
First, clone the repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/21BAI1558_ML.git
cd 21BAI1558_ML
Step 2: Install Required Python Dependencies
Install the necessary Python packages using pip:

bash
Copy code
pip install -r requirements.txt
Step 3: Configure Redis
Ensure that Redis is installed and running on your system. Installation instructions can be found on the official Redis website.

Step 4: Set Up OpenAI API Key
Set your OpenAI API key in the ingestion script (ingestion.py) by replacing the placeholder with your actual API key.

# Usage
Document Ingestion
Before using the search API, documents must be ingested and stored in Redis. To ingest a document, run the ingestion script:

bash
Copy code
python ingestion.py
This script processes the document, divides it into smaller chunks, generates embeddings for each chunk, and stores both the chunks and their embeddings in Redis.

# Running the FastAPI Server
Once the documents have been ingested, you can start the FastAPI server by running:

bash
Copy code
uvicorn app.main:app --reload
This will start the server on http://localhost:8000.

# API Endpoints
Health Check
Endpoint: /health
Method: GET
Description: Returns the health status of the API.
Response:
json
Copy code
{ "status": "API is active" }
Semantic Search
Endpoint: /search
Method: POST
Parameters:
text: The query string for semantic search.
top_k: The number of top results to return (default: 5).
threshold: The similarity threshold for filtering results (default: 0.75).
user_id: Optional user identifier for rate-limiting purposes.
Response: A JSON object with the query, results, and inference time.
json
Copy code
{
    "query": "Artificial intelligence",
    "results": [
        { "doc_id": "doc_001", "similarity": 0.85, "chunk": "AI is intelligence..." }
    ],
    "inference_time": 0.1
}
Ingestion Process
The document ingestion process involves chunking a document into smaller parts (e.g., 500 characters per chunk), generating semantic embeddings for each chunk using OpenAI's embedding model, and storing these embeddings in Redis for later retrieval.

Steps:
Chunking: The document is split into smaller, manageable chunks to ensure optimal embedding generation.
Embedding Generation: For each chunk, an embedding is generated using OpenAI’s API, which converts the text into a high-dimensional vector representation.
Storage in Redis: The chunk and its embedding are stored in Redis, allowing for efficient vector-based searches.
Search Functionality
The search functionality is designed to retrieve semantically similar document chunks based on a user’s query. It works by converting the query into an embedding using the same OpenAI model, calculating cosine similarity between the query embedding and stored embeddings, and returning the most similar chunks.

# Workflow:
Query Submission: A user submits a search query via the /search endpoint.
Embedding Generation: The query is converted into an embedding.
Similarity Calculation: The cosine similarity between the query embedding and the stored embeddings is computed.
Results Return: The top-k most similar document chunks are returned, ordered by similarity.
Contributing
We welcome contributions from the community. If you would like to contribute to this project, please follow these guidelines:

# Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request, ensuring your code adheres to the coding standards.
Include tests, if applicable, to verify your changes.
For larger contributions, please consider opening an issue first to discuss your proposed changes.

# Contact Information
For questions, suggestions, or additional support, please contact the project maintainer at sharvaree2000@phoenixgen.com.

