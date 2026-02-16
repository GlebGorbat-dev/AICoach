'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { chatAPI, Chat } from '@/lib/api';
import { ChatCard } from '@/components/ChatCard';
import { Button } from '@/components/Button';

export default function ChatsPage() {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, logout } = useAuth();
  const [chats, setChats] = useState<Chat[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  
  // Selected chat from URL
  const selectedChatId = pathname.startsWith('/chats/') && pathname !== '/chats' 
    ? pathname.split('/chats/')[1] 
    : null;

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    loadChats();
  }, [isAuthenticated, router]);

  const loadChats = async () => {
    try {
      const response = await chatAPI.getAll();
      setChats(response.data);
      // User can stay on the list page
    } catch (error) {
      console.error('Failed to load chats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateChat = async () => {
    setIsCreating(true);
    try {
      const newChat = await chatAPI.create();
      setChats([newChat, ...chats]);
      router.push(`/chats/${newChat.id}`);
    } catch (error) {
      console.error('Failed to create chat:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteChat = async (chatId: string) => {
    if (!confirm('Are you sure you want to delete this chat?')) return;

    try {
      await chatAPI.delete(chatId);
      setChats(chats.filter((chat) => chat.id !== chatId));
      // If deleting current chat, go to list
      if (selectedChatId === chatId) {
        router.push('/chats');
      }
    } catch (error) {
      console.error('Failed to delete chat:', error);
    }
  };

  const handleSelectChat = (chatId: string) => {
    router.push(`/chats/${chatId}`);
  };

  if (!isAuthenticated || isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-pulse text-neon-red text-2xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-dark-bg">
      {/* Sidebar */}
      <div className="w-80 bg-dark-surface border-r border-dark-border flex flex-col">
        <div className="p-4 border-b border-dark-border">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-neon-red animate-neon">AI Coach</h1>
            <button
              onClick={logout}
              className="text-gray-400 hover:text-neon-red transition-colors"
            >
              Quit
            </button>
          </div>
          <Button
            onClick={handleCreateChat}
            isLoading={isCreating}
            className="w-full"
          >
            + New chat
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {chats.length === 0 ? (
            <p className="text-gray-400 text-center mt-8">No chats. Create a new one!</p>
          ) : (
            chats.map((chat) => (
              <ChatCard
                key={chat.id}
                chat={chat}
                onSelect={handleSelectChat}
                onDelete={handleDeleteChat}
                isSelected={selectedChatId === chat.id}
              />
            ))
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center text-gray-400">
        <div className="text-center">
          <p className="text-xl mb-4">Welcome!</p>
          <p className="mb-4">Select a chat from the list on the left or create a new one</p>
          {chats.length === 0 && (
            <p className="text-sm">No chats. Create a new one to start chatting with the AI assistant</p>
          )}
        </div>
      </div>
    </div>
  );
}

