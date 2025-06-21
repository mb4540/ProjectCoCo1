import React from 'react';
import { Message } from '../types/message';
import './MessageItem.css';

interface MessageItemProps {
  message: Message;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return timestamp;
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role.toLowerCase()) {
      case 'admin':
        return '#ef4444';
      case 'developer':
        return '#3b82f6';
      case 'ai':
        return '#8b5cf6';
      case 'user':
        return '#10b981';
      default:
        return '#6b7280';
    }
  };

  return (
    <div className="message-item">
      <div className="message-header">
        <div className="user-info">
          <span className="user-name">{message.userId}</span>
          <span 
            className="role-badge" 
            style={{ backgroundColor: getRoleBadgeColor(message.role) }}
          >
            {message.role}
          </span>
        </div>
        <span className="timestamp">{formatTimestamp(message.ts)}</span>
      </div>
      <div className="message-content">
        {message.text}
      </div>
    </div>
  );
};

export default MessageItem; 