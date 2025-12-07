import React from 'react';
import ChatComponent from './ChatComponent';
import './ChatWindow.css';

const ChatWindow = ({ closeChat }) => {
  return (
    <div className="chat-window">
      <div className="chat-window-header">
        <h2>Chatbot</h2>
        <button onClick={closeChat} className="chat-window-close-button">
          &times;
        </button>
      </div>
      <div className="chat-window-body">
        <ChatComponent />
      </div>
    </div>
  );
};

export default ChatWindow;
