// API client for RAG Chatbot Backend

// Default API base URL for the RAG chatbot backend
// This can be overridden by defining window.RAG_CHATBOT_CONFIG.apiBaseUrl in the HTML
const DEFAULT_API_BASE_URL = 'http://localhost:8000/api';

// Get the API base URL from a global config, or use the default
const getApiBaseUrl = () => {
  if (typeof window !== 'undefined' && window.RAG_CHATBOT_CONFIG && window.RAG_CHATBOT_CONFIG.apiBaseUrl) {
    return window.RAG_CHATBOT_CONFIG.apiBaseUrl;
  }
  return DEFAULT_API_BASE_URL;
};

class ApiClient {
  static async query(text) {
    const API_BASE_URL = getApiBaseUrl();
    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: text }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Query API error:', error);
      throw error;
    }
  }

  static async initializeContent() {
    const API_BASE_URL = getApiBaseUrl();
    try {
      const response = await fetch(`${API_BASE_URL}/initialize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Initialize API error:', error);
      throw error;
    }
  }

  static async getInitializationStatus(jobId) {
    const API_BASE_URL = getApiBaseUrl();
    try {
      const response = await fetch(`${API_BASE_URL}/initialize/${jobId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Initialization status API error:', error);
      throw error;
    }
  }

  static async getStatus() {
    const API_BASE_URL = getApiBaseUrl();
    try {
      const response = await fetch(`${API_BASE_URL}/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Status API error:', error);
      throw error;
    }
  }
}

export default ApiClient;