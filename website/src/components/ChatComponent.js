import React, { useState, useRef, useEffect } from 'react';
import ApiClient from './ApiClient';
import './ChatComponent.css';

// Keys for local storage
const CHAT_HISTORY_KEY = 'rag_chatbot_history';
const SESSION_ID_KEY = 'rag_chatbot_session_id';

const ChatComponent = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize session on component mount
  useEffect(() => {
    // Generate or retrieve session ID
    let currentSessionId = localStorage.getItem(SESSION_ID_KEY);
    if (!currentSessionId) {
      currentSessionId = 'session_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
      localStorage.setItem(SESSION_ID_KEY, currentSessionId);
    }
    setSessionId(currentSessionId);

    // Load chat history from local storage on component mount
    const savedMessages = localStorage.getItem(CHAT_HISTORY_KEY);
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (e) {
        console.error('Failed to parse saved chat history:', e);
        // Start with empty chat if parsing fails
        setMessages([]);
      }
    }
  }, []);

  // Function to start a new session
  const startNewSession = () => {
    // Generate new session ID
    const newSessionId = 'session_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    localStorage.setItem(SESSION_ID_KEY, newSessionId);
    setSessionId(newSessionId);

    // Clear chat history for the new session
    setMessages([]);
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify([]));
  };

  // Function to scroll to the bottom of the chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Save chat history to local storage whenever messages change
  useEffect(() => {
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API to get the response using the API client
      const data = await ApiClient.query(inputValue);

      // Add assistant message to the chat
      const assistantMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'assistant',
        sources: data.sources
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMessageText = 'Sorry, I encountered an error. Please try again.';

      // More specific error messages based on error type
      if (error.message.includes('400')) {
        errorMessageText = 'Invalid query. Please check your input.';
      } else if (error.message.includes('500')) {
        errorMessageText = 'Server error. Please try again later.';
      } else if (error.message.includes('Network Error') || error.message.includes('Failed to fetch')) {
        errorMessageText = 'Network error. Please check your connection and try again.';
      }

      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'assistant'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h3>RAG Chatbot</h3>
        <button onClick={startNewSession} className="new-session-button">
          New Session
        </button>
      </div>
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-text">{message.text}</div>
            {message.sources && message.sources.length > 0 && (
              <div className="message-sources">
                <strong>Sources:</strong>
                <ul>
                  {message.sources.map((source, index) => (
                    <li key={index}>
                      <a href={source} target="_blank" rel="noopener noreferrer">{source}</a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message assistant-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the content..."
          className="chat-input"
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatComponent;