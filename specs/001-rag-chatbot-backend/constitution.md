# Backend Constitution: RAG Chatbot

This document outlines the foundational principles and architectural guidelines for the RAG Chatbot backend. It serves as a single source of truth for design, implementation, and maintenance decisions.

## 1. Core Principles

*   **Modularity:** Components should be loosely coupled and highly cohesive, allowing for independent development, testing, and scaling.
*   **Scalability:** The architecture should support increased load and data volume without significant redesign. Serverless components should be preferred where applicable.
*   **Reliability:** The system must be resilient to failures, with robust error handling, monitoring, and recovery mechanisms.
*   **Security:** All data handling, API endpoints, and external integrations must adhere to best security practices (e.g., input validation, authentication, authorization, data encryption).
*   **Maintainability:** Code should be clean, well-documented, and follow established coding standards to facilitate understanding and future modifications.
*   **Performance:** Queries should be optimized for low latency, especially for user-facing interactions.
*   **Observability:** The system should provide sufficient logging, metrics, and tracing to monitor its health, performance, and diagnose issues effectively.

## 2. Architectural Decisions & Technology Stack

*   **API Framework:** FastAPI (Python) for building efficient, high-performance RESTful APIs.
    *   **Rationale:** Asynchronous support, Pydantic for data validation, automatic OpenAPI documentation.
*   **Vector Database:** Qdrant Cloud (Free Tier) for semantic search and efficient storage/retrieval of vector embeddings.
    *   **Rationale:** Specialized for vector similarity search, offers cloud solution, aligns with free-tier constraint.
*   **Relational Database:** Neon Serverless Postgres for metadata storage, session management, and potentially user preferences or analytics.
    *   **Rationale:** Serverless for cost efficiency, robust relational features, strong community support.
*   **LLM Integration:** OpenAI Agents/ChatKit SDKs for orchestrating LLM calls, function calling, and managing conversational flows.
    *   **Rationale:** Direct integration with OpenAI models, provides structured tools for agent development.
*   **Data Ingestion/Processing:** Python scripts for chunking, embedding generation, and loading data into Qdrant and Postgres.
    *   **Rationale:** Python's ecosystem for NLP and data handling.

## 3. Data Flow & Components

### 3.1 Ingestion Pipeline

1.  **Book Content:** Markdown files from the Docusaurus site (`website/docs/study/`).
2.  **Chunking:** Content will be divided into semantically meaningful chunks (e.g., paragraphs, sections) for vectorization.
3.  **Embedding Generation:** OpenAI's embedding models will generate vector representations for each chunk.
4.  **Vector Storage:** Chunks and their embeddings will be stored in Qdrant.
5.  **Metadata Storage:** Associated metadata (e.g., file path, chapter, section title, original text, page number if applicable) will be stored in Neon Postgres.

### 3.2 Chat Interaction Pipeline

1.  **User Query / Selected Text:** Input from the frontend.
2.  **FastAPI Endpoint:** Receives the user request.
3.  **Embedding Generation (Query):** User query is vectorized using the same OpenAI embedding model.
4.  **Vector Search (Qdrant)::** Top-k most relevant chunks are retrieved from Qdrant based on similarity to the query embedding.
5.  **Context Augmentation:** Retrieved chunks (and potentially relevant metadata from Postgres) form the context for the LLM.
6.  **LLM Call (OpenAI Agents/ChatKit):** The user query and augmented context are sent to the LLM.
7.  **Response Generation:** LLM generates a coherent answer.
8.  **Response to User:** FastAPI sends the LLM's response back to the frontend.

## 4. Coding Standards & Practices

*   **Python:** Adhere to PEP 8.
*   **Type Hinting:** Strictly use Python type hints for clarity and maintainability.
*   **Asynchronous Programming:** Utilize `async/await` patterns, especially in FastAPI handlers and I/O-bound operations.
*   **Environment Variables:** All sensitive information (API keys, database credentials) and configurable parameters must be managed via environment variables (`.env`).
*   **Testing:** Implement unit and integration tests for all core backend components and API endpoints.

## 5. Security Considerations

*   **API Key Management:** Store API keys securely (e.g., environment variables, secrets management services).
*   **Input Validation:** Validate all incoming API requests to prevent injection attacks and ensure data integrity.
*   **Access Control:** Implement appropriate authentication and authorization if multiple user roles or external access is needed. (Initial MVP might skip user auth for internal access).
*   **Data Minimization:** Only store necessary user data.

## 6. Deployment & Operations

*   **Containerization:** Dockerize the FastAPI application for consistent deployment environments.
*   **Logging:** Implement structured logging (e.g., JSON format) to a centralized logging system.
*   **Monitoring:** Track key metrics (e.g., API response times, error rates, LLM token usage, Qdrant/Postgres performance).
*   **CI/CD:** Automate testing, building, and deployment processes.