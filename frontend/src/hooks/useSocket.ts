import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { Message } from '../types/message';

const SOCKET_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useSocket = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const newSocket = io(SOCKET_URL, {
      namespace: '/ws'
    });

    newSocket.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server');
      setIsConnected(false);
    });

    newSocket.on('message', (message: Message) => {
      setMessages(prev => [...prev, message]);
    });

    newSocket.on('error', (error: any) => {
      console.error('Socket error:', error);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const sendMessage = (message: Omit<Message, 'ts'>) => {
    if (socket && isConnected) {
      const messageWithTimestamp = {
        ...message,
        ts: new Date().toISOString()
      };
      socket.emit('message', messageWithTimestamp);
    }
  };

  return {
    socket,
    messages,
    isConnected,
    sendMessage
  };
}; 