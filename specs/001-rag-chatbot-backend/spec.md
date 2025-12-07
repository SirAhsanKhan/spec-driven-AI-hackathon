# RAG Chatbot Backend Specification

## 1. System Overview

This document specifies the requirements for a Retrieval-Augmented Generation (RAG) chatbot system that enables users to ask questions about content from a specified web page. The system will scrape content from a provided URL, chunk the content, and utilize an OpenAI agent to process user queries with respect to the scraped content.

## 2. Functional Requirements

### 2.1 Content Processing Workflow
- The system shall accept a URL as input for content scraping
- The system shall scrape all relevant text content from the provided URL using appropriate web scraping techniques
- The system shall clean and preprocess the scraped content to remove HTML tags and irrelevant information
- The system shall divide the cleaned content into chunks of 512-1024 tokens using a semantic-aware chunking algorithm
- The system shall generate vector embeddings for each chunk using OpenAI's text-embedding-3-small model
- The system shall store the chunks and their embeddings in a SQLite database
- The system shall index the content in Qdrant Cloud for efficient similarity search

### 2.2 Query Processing
- The system shall accept user queries through a chat interface
- The system shall generate vector embeddings for the user query using the same embedding model
- The system shall perform similarity search in Qdrant Cloud to retrieve the most relevant content chunks
- The system shall use an OpenAI agent to process user queries with the retrieved context
- The system shall ground responses in the scraped content through retrieval-augmented generation
- The system shall provide source citations for information in its responses, linking back to the original content
- If a query is out of context or cannot be answered with the available content, the system shall respond with a predefined message indicating so

### 2.3 User Interface
- The system shall provide a chatbot UI integrated within the web application
- The system shall allow users to input their initial URL for content scraping
- The system shall provide visual feedback during content processing (e.g., progress indicator)
- The system shall allow users to input their queries in a conversational manner
- The system shall display responses in a chat-like format with clear distinction between user queries and system responses
- The system shall display source citations with links to the original content where applicable
- The system shall maintain conversation history in the UI during the session
- The system shall provide a clear way to start a new session or switch to a different URL
- The UI shall be responsive and work well on different screen sizes (desktop, tablet, mobile)

### 2.4 Data Management
- The system shall store chat history in browser's local storage
- The system shall not store any user data on the server-side
- The system shall maintain privacy of user interactions
- The system shall manage content databases per URL to optimize retrieval

## 3. Technical Specifications

### 3.1 Architecture
- Backend: FastAPI-based API server for processing requests
- AI Integration: OpenAI agent for question answering
- Database: SQLite for storing scraped content and chunks
- Frontend: React-based chat interface integrated into the website
- Vector Storage: Qdrant Cloud Free Tier for similarity search

### 3.2 API Endpoint Specifications
The system shall expose the following RESTful API endpoints:

- `POST /api/scrape` - Accepts a URL and initiates the content scraping and chunking process
  - Request body: { "url": "https://example.com" }
  - Response: { "status": "processing", "job_id": "unique_job_identifier" }

- `GET /api/scrape/{job_id}` - Checks the status of a scraping job
  - Response: { "status": "processing|completed|failed", "progress": 0-100 if processing }

- `POST /api/query` - Accepts a user query and returns a response based on the scraped content
  - Request body: { "query": "user's question", "url": "context identifier" }
  - Response: { "response": "answer from AI", "sources": ["source1", "source2", ...] }

- `GET /api/urls` - Returns a list of URLs that have been processed
  - Response: [{ "url": "https://example.com", "added_date": "timestamp" }]

- `DELETE /api/urls/{url_id}` - Deletes a previously processed URL and its associated content
  - Response: { "status": "deleted" }

### 3.3 OpenAI Agent Integration
- The system shall utilize OpenAI's GPT model for response generation
- The system shall implement system instructions that guide the agent to:
  - Only respond based on the provided context from scraped content
  - Provide accurate answers that are directly supported by the retrieved chunks
  - Cite sources by referencing the original content when providing information
  - Respond with a predefined message when queries are outside the scope of available content
  - Handle ambiguous queries by asking for clarification when needed
- The system shall format retrieved context chunks appropriately for the agent
- The system shall implement proper prompt engineering to ensure quality responses

### 3.4 Data Flow
1. System retrieves the pre-stored URL for content processing
2. System scrapes content from the URL
3. Content is chunked into 512-1024 token segments
4. Chunks are stored in the database with vector embeddings
5. User submits query through the chat interface
6. System retrieves relevant chunks based on query similarity
7. OpenAI agent generates response using retrieved context
8. Response is returned to the user with source citations

### 3.5 Error Handling
- Invalid URLs should result in appropriate error messages
- Content scraping failures should be handled gracefully
- Out-of-context queries should return predefined messages
- System errors should be logged appropriately

## 6. Non-Functional Requirements

### 6.1 Performance
- Performance targets are best effort and dependent on free-tier limits.
- Maximum acceptable response time: <3 seconds for 95% of queries
- System shall handle up to 10 concurrent users

### 6.2 Reliability
- System availability should be maintained during normal operations
- Graceful degradation when Qdrant Cloud Free Tier limits are reached
- Proper error handling and recovery mechanisms

### 6.3 Privacy
- All user data must be stored locally in the browser
- No server-side user tracking or authentication required
- No user data should be transmitted to external services beyond the API call for processing

## 7. Acceptance Criteria

- Chatbot answers questions accurately based on scraped content (>80% accuracy in testing)
- Retrieval-augmented generation properly cites source passages
- System handles up to 10 concurrent users without performance degradation
- Response time meets the specified targets
- User data remains private and is stored only in browser storage
- Out-of-context queries receive predefined error responses

## 8. Constraints

- Qdrant Cloud Free Tier limitations must be respected (storage, query limits)
- Designed for low-traffic: up to 5 regular users with max 10 concurrent users
- No user authentication or account system required
- User data stored client-side only (browser storage)

## Clarifications

### Session 2025-12-07

- Q: How should the pre-stored URL be managed? → A: Environment variable
- Q: How should API keys be managed? → A: Environment variables
- Q: How should the chatbot UI be integrated with Docusaurus? → A: As a React component
- Q: How should out-of-context queries be handled? → A: Predefined message

## 9. Additional Requirements

- The target URL will be configured via an environment variable at deployment time
- The system will retrieve the URL from environment variables at startup
- Content from the URL will be scraped once during initial setup and remain static
- The system will not automatically re-scrape content after the initial setup
- API keys for external services (OpenAI, Qdrant) will be managed through environment variables
- The application will validate the presence of required API keys at startup
- The chatbot UI will be implemented as a React component integrated into Docusaurus pages
- The UI component will follow the existing Docusaurus styling conventions
- When user queries are out of context or cannot be answered, the system will return a predefined message
- The predefined message will inform the user that the query cannot be answered based on the available content