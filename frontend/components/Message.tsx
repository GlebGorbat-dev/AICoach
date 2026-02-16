import React from 'react';
import { Message as MessageType } from '@/lib/api';
import { formatTime } from '@/lib/dateUtils';

interface MessageProps {
  message: MessageType;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.author === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`
          max-w-[80%] rounded-lg px-4 py-3
          ${isUser 
            ? 'bg-neon-red text-white shadow-neon-red-sm' 
            : 'bg-dark-surface text-gray-200 border border-dark-border'
          }
        `}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        <p className={`text-xs mt-2 ${isUser ? 'text-red-200' : 'text-gray-400'}`}>
          {formatTime(message.datetimeCreated)}
        </p>
      </div>
    </div>
  );
};

