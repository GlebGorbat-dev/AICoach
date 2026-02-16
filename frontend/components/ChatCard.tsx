import React from 'react';
import { Chat } from '@/lib/api';
import { formatDate } from '@/lib/dateUtils';

interface ChatCardProps {
  chat: Chat;
  onSelect: (chatId: string) => void;
  onDelete: (chatId: string) => void;
  isSelected?: boolean;
}

export const ChatCard: React.FC<ChatCardProps> = ({
  chat,
  onSelect,
  onDelete,
  isSelected = false,
}) => {
  return (
    <div
      className={`
        p-4 rounded-lg cursor-pointer transition-all duration-300
        ${isSelected 
          ? 'bg-dark-surface-light border-2 border-neon-red shadow-neon-red-sm' 
          : 'bg-dark-surface border border-dark-border hover:border-neon-red hover:shadow-neon-red-sm'
        }
      `}
      onClick={() => onSelect(chat.id)}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <h3 className="text-white font-medium truncate mb-1">{chat.title}</h3>
          <p className="text-xs text-gray-400">
            {formatDate(chat.datetimeUpdated)}
          </p>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(chat.id);
          }}
          className="ml-2 text-red-500 hover:text-neon-red transition-colors"
        >
          🗑️
        </button>
      </div>
    </div>
  );
};

