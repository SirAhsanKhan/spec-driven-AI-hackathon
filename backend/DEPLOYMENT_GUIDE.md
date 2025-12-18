# Deployment Guide for Vercel with Neon Database

## Overview

This guide explains how to deploy the RAG Chatbot Backend to Vercel using Neon as the serverless PostgreSQL database.

## Prerequisites

1. A Neon account and database
2. Vercel account for deployment
3. OpenAI API key

## Step-by-Step Deployment Process

### 1. Set up Neon Database

1. Sign up at [Neon](https://neon.tech/)
2. Create a new project
3. Note down the connection string (DATABASE_URL) from the Neon dashboard

### 2. Configure Environment Variables

Add these environment variables in your Vercel project settings:

```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_neon_database_connection_string
QDRANT_HOST=your_qdrant_host_if_not_using_local
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_PORT=6333
CONTENT_URL=your_default_content_url
CONTENT_URL_DOC1=optional_additional_url
CONTENT_URL_DOC2=optional_additional_url
```

### 3. Database Migration for Vercel

For serverless environments like Vercel, database schema migration needs to happen before the application starts serving requests. 

The current implementation skips table creation at runtime (in `init_db()` function) when running in Vercel. To properly set up your tables:

#### Option A: Using Vercel's Build Hooks
Add a build script to your `vercel.json` to run migrations:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "functions": {
    "api/migrate.py": {
      "runtime": "python3.11"
    }
  }
}
```

#### Option B: Manual Table Creation (Quick Start)
Execute the following SQL statements in your Neon SQL editor:

```sql
CREATE TABLE content_entities (
    id VARCHAR PRIMARY KEY,
    url VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR DEFAULT 'processing'
);

CREATE TABLE content_chunks (
    id VARCHAR PRIMARY KEY,
    content_id VARCHAR NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Deploy to Vercel

You can deploy in two ways:

#### Via Vercel CLI:
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your backend directory
3. Follow the prompts to link your project

#### Via Git Integration:
1. Push your code to a GitHub/GitLab/Bitbucket repository
2. Connect the repository to your Vercel dashboard
3. Deploy automatically on pushes to main branch

## Important Notes

- The application is configured to skip table creation at runtime in Vercel environments to avoid timeout issues
- SSL is enforced for database connections to Neon
- Connection pooling is optimized for serverless environments
- For production use, consider adding a proper migration system using Alembic

## Troubleshooting

### Common Issues:

1. **Connection Timeout Errors**: Verify your Neon database connection string and SSL settings
2. **Table Doesn't Exist Errors**: Ensure you've run the database migration/schema creation
3. **Environment Variables Not Found**: Double-check that all required environment variables are set in your Vercel project settings
4. **Initialization Taking Too Long**: The initialization process is intensive and may take time; ensure your content URLs are accessible

### Testing the Deployment:

Once deployed, you can test your API using:
- Health check: `GET /health/ready` and `GET /health/live`
- Documentation: `GET /docs` (Swagger UI) or `GET /redoc` (Redoc UI)
- Initialize content: `POST /api/initialize` with JSON body `{"url": "your-content-url"}`
- Query content: `POST /api/query` with JSON body `{"query": "your-question"}`