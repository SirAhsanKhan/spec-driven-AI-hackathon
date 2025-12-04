# Feature Specification: RAG Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "implement a Retrieval-Augmented Generation (RAG) chatbot within the published book, enabling users to ask questions and receive accurate answers based on the book’s content. The chatbot leverages OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud to provide contextual responses, including the ability to answer queries based on text specifically selected by the user."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask General Questions (Priority: P1)

As a user reading the published book, I want to ask general questions about the book's content and receive accurate, concise answers from the chatbot.

**Why this priority**: This is the core functionality of a RAG chatbot for a book, enabling basic knowledge retrieval.

**Independent Test**: User asks a question about a core concept from the book (e.g., "What is Physical AI?") and receives a correct answer derived from the book's content.

**Acceptance Scenarios**:

1. **Given** the chatbot is active, **When** the user asks "What is Physical AI?", **Then** the chatbot provides a definition of Physical AI based on the book's introduction.
2. **Given** the chatbot is active, **When** the user asks "List the key characteristics of Physical AI Systems.", **Then** the chatbot returns the list of characteristics as described in the book.

---

### User Story 2 - Query Selected Text (Priority: P1)

As a user, I want to select a specific passage of text from the book and ask the chatbot questions *related only to that selected passage* to get more focused and contextual answers.

**Why this priority**: This addresses a key and unique requirement of the user, enabling highly contextual querying.

**Independent Test**: User selects a paragraph and asks a question relevant only to that paragraph, receiving an answer strictly from the selected text, even if the general book content might offer a broader answer.

**Acceptance Scenarios**:

1. **Given** the user selects a paragraph discussing "Embodied Cognition", **When** the user asks "What does Brooks mean by 'The world is its own best model'?", **Then** the chatbot provides an answer based *only* on the selected text.
2. **Given** the user selects a section about "Actuation Technologies", **When** the user asks "What are the typical specs for Electric Actuators?", **Then** the chatbot responds with the torque density and efficiency mentioned within the selected section.

---

### User Story 3 - Understand Answer Context (Priority: P2)

As a user, I want the chatbot to indicate the source(s) (e.g., chapter/section) from the book that were used to generate its answer, so I can verify the information or explore further.

**Why this priority**: Enhances trust and utility, allowing users to delve deeper into the content.

**Independent Test**: User asks a question and the chatbot provides an answer along with a clear reference to the relevant chapter or section in the book.

**Acceptance Scenarios**:

1. **Given** the chatbot provides an answer to a question, **When** the answer is displayed, **Then** the chatbot also shows the chapter and section titles from which the information was retrieved.

---

### Edge Cases

- What happens when a question is unanswerable based on the book's content? (Chatbot should state it cannot find information in the book).
- How does the system handle very long user-selected text? (Should have a reasonable limit or provide a summary).
- What happens if the underlying LLM or vector database APIs are unavailable? (Graceful degradation, error message to user).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST ingest Markdown content from the published book (Docusaurus site) and convert it into a searchable format.
- **FR-002**: The system MUST chunk the book's content into semantically meaningful units suitable for embedding.
- **FR-003**: The system MUST generate vector embeddings for each content chunk using OpenAI's embedding models.
- **FR-004**: The system MUST store content chunks and their vector embeddings in Qdrant Cloud.
- **FR-005**: The system MUST store metadata (e.g., file path, chapter, section, original text, vector ID) for each content chunk in Neon Serverless Postgres.
- **FR-006**: The system MUST provide an API endpoint (`/chat`) to receive user text queries.
- **FR-007**: The system MUST, for a given user query, retrieve relevant content chunks from Qdrant Cloud based on semantic similarity.
- **FR-008**: The system MUST augment the user query with retrieved content chunks (and metadata from Postgres) to form a prompt for the LLM.
- **FR-009**: The system MUST leverage OpenAI Agents/ChatKit SDKs to interact with an LLM for generating responses.
- **FR-010**: The system MUST provide an API endpoint (e.g., `/query_selected`) to receive user queries paired with user-selected text, prioritizing the selected text as primary context.
- **FR-011**: The system MUST include source information (chapter, section) from the book along with the generated answer.
- **FR-012**: The system MUST handle authentication and authorization for API access (at least for internal components, if not external users initially).

### Key Entities

- **DocumentChunk**: Represents a segment of the book's content.
    - `id`: Unique identifier (e.g., UUID or sequential ID).
    - `text_content`: The actual text of the chunk.
    - `embedding`: Vector representation of the text.
    - `metadata`: Associated information (file_path, chapter, section, page_number).
- **UserQuery**: The question or selected text provided by the user.
- **ChatResponse**: The answer generated by the chatbot.
    - `answer`: The LLM's generated response.
    - `sources`: List of document metadata indicating where the answer came from.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chatbot accurately answers 90% of general questions based on book content.
- **SC-002**: Chatbot accurately answers 95% of questions specific to user-selected text, deriving the answer solely from the selected context.
- **SC-003**: For 90% of answers, the chatbot correctly identifies and presents the chapter and section from which the information was sourced.
- **SC-004**: Average response time for a chatbot query is under 3 seconds.
- **SC-005**: The ingestion pipeline successfully processes all book content (Markdown files) without errors.

## Assumptions

- The published book content (Markdown files) will be stable and accessible for the ingestion pipeline.
- OpenAI API keys and Qdrant/Neon service credentials will be securely provided via environment variables.
- The LLM will primarily be used for response generation and not for complex conversational state management, which will be handled by the backend application.