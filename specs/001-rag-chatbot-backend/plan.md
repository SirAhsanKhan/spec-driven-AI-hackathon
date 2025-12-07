# RAG Chatbot Backend Implementation Plan

## Technical Context

The RAG (Retrieval-Augmented Generation) chatbot backend will be built to process pre-stored URLs, scrape their content, chunk it, and enable users to ask questions about that content through an AI-powered interface. This system needs to integrate with external services (OpenAI, Qdrant Cloud) while maintaining privacy and performance standards as specified in the constitution and feature spec.

### Architecture Overview
- Backend Framework: FastAPI for high-performance API development
- AI/ML Framework: OpenAI agents SDK for LLM integration
- Vector Database: Qdrant Cloud Free Tier for efficient similarity search
- Content Database: SQLite for storing book content
- Embeddings: OpenAI text-embedding-3-small model
- Frontend: To be integrated with existing Docusaurus website
- URL Configuration: Managed via environment variable at deployment

### System Components
1. Content Scraper - for extracting text from pre-stored URL (from environment variable)
2. Content Chunker - for splitting content into appropriate token sizes
3. Embedding Generator - for creating vector representations of content
4. Vector Storage Manager - for storing and retrieving embeddings
5. Query Processor - for handling user queries and context retrieval
6. OpenAI Agent Interface - for generating responses based on context
7. API Layer - for managing requests and responses
8. Frontend Integration - for chatbot UI

### Dependencies
- Python 3.9+
- FastAPI
- OpenAI Python library
- Qdrant client library
- SQLite
- BeautifulSoup (or similar) for web scraping
- Frontend: React, TypeScript (for potential new UI components)

### Current Unknowns (NEEDS CLARIFICATION)
- What is the expected volume of content to be processed? Understanding the scale of content (number of pages, total text size) is important for performance planning and resource allocation.
- What specific frontend framework is currently in use with Docusaurus? Need to understand the current website stack to plan for proper integration of the chatbot UI component.
- What is the expected concurrent user load? Understanding if the system will approach the 10-concurrent user constraint will affect performance optimization priorities.
- How should the system handle Qdrant Cloud Free Tier limitations? Need to plan for potential limitations in storage, queries, or rate limits that could affect the user experience.

## Constitution Check

This implementation plan is evaluated against the RAG Chatbot Development Constitution:

### I. Accuracy
- Plan includes integration with OpenAI agents for accurate response generation
- Implementation of retrieval-augmented generation to ground responses in source content
- System will be designed to properly cite source passages
- Content chunking strategy (512-1024 tokens) will help maintain context accuracy

### II. Responsiveness
- FastAPI framework chosen for high-performance API development
- Target response time of <2s per query will be monitored in implementation
- Asynchronous processing for content scraping to improve user experience
- Vector search with Qdrant Cloud for efficient similarity matching

### III. Simplicity
- Lightweight architecture with minimal complexity
- SQLite for content storage to keep deployment simple
- Clear separation of concerns in system components
- Single-page chatbot UI to minimize complexity

### IV. Privacy
- Plan ensures user data is stored locally in browser
- No server-side user tracking or authentication required in design
- Implementation will respect privacy requirements from constitution
- No user data transmitted to external services beyond API calls for processing

### V. Reliability
- Error handling and system health monitoring included in component design
- If Qdrant limits are hit, ingestion is disabled until cleanup
- Oldest vectors removed when storage limits are reached
- Proper fallback mechanisms for out-of-context queries
- Content persistence in SQLite for availability during service disruptions
- Static content approach ensures consistent availability after initial setup

## Gates

### Feasibility Gate
- [X] Technology stack is proven and appropriate for requirements - FastAPI, OpenAI, Qdrant, and SQLite are established technologies with strong community support
- [X] Qdrant Cloud Free Tier limitations can be respected (storage, query limits) - The system can be designed with caching and efficient querying to work within these constraints
- [X] Architecture supports required concurrency (up to 10 concurrent users) - FastAPI with async processing can handle this load in testing environment
- [X] Response time targets can be achieved with proposed approach - Vector similarity search with Qdrant and optimized API calls should meet response time requirements

### Risk Assessment Gate
- [X] External dependencies (OpenAI API, Qdrant Cloud) have appropriate fallback/backup plans - Implement timeout handling and error responses when external services are unavailable
- [X] Content scraping approach complies with website terms and legal requirements - Will implement respectful scraping with appropriate delays and adherence to robots.txt
- [X] System design addresses potential rate limiting from external APIs - Will implement rate limiting and retry logic with exponential backoff
- [X] Privacy requirements can be fully implemented as specified - Architecture is designed to store user data only in browser storage

### Resource Gate
- [X] Available resources (time, budget, personnel) are sufficient for implementation - The MVP can be built with the specified technology stack within reasonable timeframes
- [X] OpenAI and Qdrant API costs align with project budget for free tier - Designed to work within free tier limitations
- [X] Development environment setup is feasible within project constraints - All required technologies can be installed in standard development environments

## Phase 0: Research & Analysis

### 0.1 URL Management Research
**Decision**: Use environment variables for managing the pre-stored URL
**Rationale**: Environment variables provide a simple, secure way to configure the URL at deployment time without requiring code changes
**Alternatives considered**: Database storage, configuration file, hardcoding (rejected)

### 0.2 Content Static Assessment
**Decision**: Content from the pre-stored URL will be scraped once and remain static
**Rationale**: Since there's a single pre-stored URL, static content approach simplifies architecture and reduces external dependencies after initial setup
**Alternatives considered**: Dynamic content (refreshed periodically), real-time scraping, static (selected)

### 0.3 Security Research
**Decision**: Use environment variables for managing API keys and credentials
**Rationale**: Security is critical when using external APIs with billing implications
**Alternatives considered**: Environment variables (selected), secure key vaults, encrypted storage

### 0.4 Docusaurus Integration Research
**Decision**: Integrate the chatbot UI as a React component within Docusaurus pages
**Rationale**: Docusaurus natively supports React components, making this the simplest integration approach
**Alternatives considered**: Standalone React app, Docusaurus plugin, iframe integration

## Phase 1: Design & Architecture

### 1.1 Data Model Design

#### ContentEntity
- id: UUID
- url: String (URL of the source)
- title: String (title of the content)
- content: Text (full scraped content)
- created_at: DateTime
- updated_at: DateTime
- status: String (processing, completed, failed)

#### ContentChunk
- id: UUID
- content_id: UUID (foreign key to ContentEntity)
- chunk_text: Text
- chunk_order: Integer
- embedding: Vector (OpenAI embedding)
- created_at: DateTime

#### ChatSession
- id: UUID
- url_reference: String (reference to processed URL)
- created_at: DateTime
- updated_at: DateTime

#### ChatMessage
- id: UUID
- session_id: UUID (foreign key to ChatSession)
- role: String (user, assistant)
- content: Text
- sources: JSON (references to content chunks)
- created_at: DateTime

### 1.2 API Contracts

#### `/api/initialize`
- `POST /api/initialize` - Initialize the content from the pre-stored URL in environment variable
  - Request: `{ }`
  - Response: `{ "status": "initializing", "job_id": "string" }`

- `GET /api/initialize/{job_id}` - Check initialization job status
  - Response: `{ "status": "processing|completed|failed", "progress": "number" }`

#### `/api/query`
- `POST /api/query` - Submit user query and get response
  - Request: `{ "query": "string" }`
  - Response: `{ "response": "string", "sources": ["string"] }`

#### `/api/status`
- `GET /api/status` - Get system status and initialization information
  - Response: `{ "initialized": true|false, "content_source": "URL from env var", "last_updated": "timestamp" }`

### 1.3 Implementation Approach

#### Phase 1A: Core Processing Pipeline
1. Develop content scraper module for the pre-stored URL from environment variable
2. Implement content chunker with 512-1024 token strategy
3. Create embedding generator using OpenAI API
4. Implement vector storage with Qdrant integration
5. Build initialization API endpoints for one-time setup
6. Add content persistence for static content (not re-scraped)

#### Phase 1B: Query Processing
1. Create similarity search functionality
2. Implement OpenAI agent integration with system instructions
3. Build query processing endpoint
4. Add source citation functionality

#### Phase 1C: Integration and UI
1. Integrate with existing Docusaurus website as React component
2. Implement chatbot UI component
3. Add browser storage for chat history
4. Implement session management

### 1.4 Frontend UI/UX Rework
- **Decision**: Redesign chatbot UI from a standalone page to a floating, accessible component on documentation pages.
  - **Rationale**: Improves user experience by making the chatbot readily available across the site without navigating away from documentation. Addresses user feedback regarding current UI presentation.
  - **Approach**: Implement a floating chat bubble that, when clicked, opens a dedicated chat window/modal.
  - **Alternatives Considered**:
    - Embedding chat directly into the sidebar (rejected: can be intrusive, reduces content area).
    - Dedicated full-page chat (rejected: current design, user found "pathetic").

#### 1.4.1 Floating Chat Component
- **Component**: `FloatingChatButton.js` (new) - Displays a chat icon, opens/closes chat window.
- **Placement**: Integrated into Docusaurus root layout via swizzling to ensure presence on all pages.

#### 1.4.2 Chat Window/Modal
- **Component**: `ChatWindow.js` (new) - Contains the main `ChatComponent.js` logic.
- **Functionality**: Toggles visibility, handles open/close state, displays `ChatComponent`.

#### 1.4.3 Chatbot UI Styling
- **Goal**: Improve visual appeal and responsiveness.
- **Approach**: Leverage existing `ChatComponent.css` and introduce new styles as needed for `FloatingChatButton` and `ChatWindow`. Adhere to Docusaurus theme for consistency.

#### 1.4.4 API Interaction
- **Component**: Reuse `ApiClient.js` for backend communication.

## Phase 2: Implementation Plan

### 2.1 Development Environment Setup
- Set up Python virtual environment
- Install required dependencies (FastAPI, OpenAI, Qdrant client, etc.)
- Configure API keys and URL environment variables

### 2.2 Content Processing Module
- Implement web scraper using appropriate libraries for pre-stored URL
- Create content cleaning and preprocessing functions
- Build chunking algorithm with semantic awareness
- Develop embedding generation functionality
- Add functionality to scrape content once and store statically

### 2.3 API Development
- Create FastAPI application structure
- Implement initialization endpoints with job status tracking for setting up content
- Build query processing endpoints
- Add proper error handling and validation
- Add system status endpoint

### 2.4 Database Integration
- Set up SQLite database with appropriate models
- Create data access layer for content management
- Implement vector storage with Qdrant
- Ensure content persistence for static data

### 2.5 Frontend Integration
- **Rework**: Implement new UI as per "1.4 Frontend UI/UX Rework" plan.
- Create `FloatingChatButton.js` component for persistent access.
- Create `ChatWindow.js` component to house `ChatComponent.js`.
- Integrate `FloatingChatButton` into Docusaurus root layout (via swizzling).
- Remove `website/src/pages/chat.js` and update `docusaurus.config.js` to remove the dedicated chatbot page link.
- Update `ChatComponent.css` and create new CSS for `FloatingChatButton` and `ChatWindow` for improved styling and responsiveness.
- Implement browser storage for chat history (as previously planned).
- Add responsive design elements (as previously planned).

### 2.6 Testing
- Unit tests for core processing functions
- Integration tests for API endpoints
- Performance testing to ensure response time targets
- End-to-end tests for complete workflow

### 2.7 Security and Privacy Verification
- Verify no server-side user data storage
- Confirm privacy compliance
- Test secure API key and URL environment variable handling
- Validate that the pre-stored URL is properly loaded from environment variables