// Global configuration for the RAG Chatbot
// This will be available in the browser as window.RAG_CHATBOT_CONFIG

// In a real deployment, you might want to load this from an environment variable or external config
if (typeof window !== 'undefined') {
  window.RAG_CHATBOT_CONFIG = {
    apiBaseUrl: 'http://localhost:8000/api', // Default for development
    // This can be changed in deployment to point to your production backend
  };
}