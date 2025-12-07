import React, { useState } from 'react';
import ChatWindow from './ChatWindow';
import './FloatingChatButton.css';

const FloatingChatButton = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <>
      <button className="floating-chat-button" onClick={toggleChat}>
        Chat
      </button>
      {isChatOpen && <ChatWindow closeChat={toggleChat} />}
    </>
  );
};

export default FloatingChatButton;
