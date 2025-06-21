import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Circle } from 'lucide-react';
import { useSocket } from '../hooks/useSocket';
import { Message } from '../types/message';
import MessageItem from './MessageItem';
import './ChatPage.css';

const ChatPage: React.FC = () => {
  const { messages, isConnected, sendMessage } = useSocket();
  const [inputText, setInputText] = useState('');
  const [currentUser] = useState({
    id: `user_${Math.random().toString(36).substr(2, 9)}`,
    name: 'Developer',
    role: 'developer'
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim() && isConnected) {
      const message: Omit<Message, 'ts'> = {
        userId: currentUser.id,
        role: currentUser.role,
        text: inputText.trim()
      };
      sendMessage(message);
      setInputText('');
    }
  };

  return (
    <div className="chat-page">
      <header className="chat-header">
        <div className="chat-title">
          <User size={24} />
          <h1>AI Dev Platform</h1>
        </div>
        <div className="connection-status">
          <Circle 
            size={12} 
            fill={isConnected ? '#22c55e' : '#ef4444'} 
            color={isConnected ? '#22c55e' : '#ef4444'} 
          />
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </header>

      <div className="messages-container">
        <div className="messages-list">
          {messages.length === 0 ? (
            <div className="no-messages">
              <p>No messages yet. Start the conversation!</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <MessageItem 
                key={`${message.userId}-${message.ts}-${index}`} 
                message={message} 
              />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <form className="message-input-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your message..."
            className="message-input"
            disabled={!isConnected}
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={!inputText.trim() || !isConnected}
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatPage; 