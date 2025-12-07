import React from 'react';
import ChatComponent from '../components/ChatComponent';

const ChatPage = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>RAG Chatbot Interface</h1>
      <p>Ask questions about the content from the pre-stored URL:</p>
      <ChatComponent />
    </div>
  );
};

export default ChatPage;