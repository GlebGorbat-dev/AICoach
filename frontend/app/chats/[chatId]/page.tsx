'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { agentAPI, chatAPI, Message, Chat } from '@/lib/api';
import { Message as MessageComponent } from '@/components/Message';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { formatDate } from '@/lib/dateUtils';

export default function ChatPage() {
  const router = useRouter();
  const params = useParams();
  const chatId = params.chatId as string;
  const { isAuthenticated, logout } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [chat, setChat] = useState<Chat | null>(null);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [documentsCount, setDocumentsCount] = useState<number | null>(null);
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [titleInput, setTitleInput] = useState('');
  const [isUpdatingTitle, setIsUpdatingTitle] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    loadChat();
    loadMessages();
    loadDocumentsCount();
  }, [chatId, isAuthenticated, router]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChat = async () => {
    try {
      const chatData = await chatAPI.get(chatId);
      setChat(chatData);
      setTitleInput(chatData.title);
    } catch (error) {
      console.error('Failed to load chat:', error);
    }
  };

  const handleStartEditTitle = () => {
    if (chat) {
      setTitleInput(chat.title);
      setIsEditingTitle(true);
    }
  };

  const handleCancelEditTitle = () => {
    if (chat) {
      setTitleInput(chat.title);
    }
    setIsEditingTitle(false);
  };

  const handleSaveTitle = async () => {
    if (!chat || !titleInput.trim() || isUpdatingTitle) return;

    setIsUpdatingTitle(true);
    try {
      const updatedChat = await chatAPI.updateTitle(chatId, titleInput.trim());
      setChat(updatedChat);
      setIsEditingTitle(false);
    } catch (error) {
      console.error('Failed to update title:', error);
      if (chat) {
        setTitleInput(chat.title);
      }
    } finally {
      setIsUpdatingTitle(false);
    }
  };

  const loadMessages = async () => {
    setIsLoading(true);
    try {
      const response = await agentAPI.getMessages(chatId, 100, 0);
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadDocumentsCount = async () => {
    try {
      const response = await agentAPI.getDocumentsCount();
      setDocumentsCount(response.amountOfDocuments);
    } catch (error) {
      console.error('Failed to load documents count:', error);
    }
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const userInput = input;
    const userMessage: Message = {
      id: Date.now().toString(),
      content: userInput,
      author: 'user',
      datetimeCreated: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsSending(true);

    try {
      const response = await agentAPI.sendMessage(chatId, {
        text: userInput,
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.text || 'No response',
        author: 'ai',
        datetimeCreated: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, aiMessage]);
      await loadChat(); // Refresh chat info
      await loadMessages(); // Reload messages for sync
    } catch (error: any) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Error: ${error.response?.data?.detail || 'Failed to send message'}`,
        author: 'ai',
        datetimeCreated: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex flex-col h-screen bg-dark-bg overflow-hidden">
      {/* Mobile header: Back + title (only on small screens) */}
      <div className="flex md:hidden flex-shrink-0 items-center gap-3 p-3 border-b border-dark-border bg-dark-surface min-h-[52px]">
        <Link
          href="/chats"
          className="text-gray-400 hover:text-neon-red transition-colors py-2 pr-2 -ml-1 min-h-[44px] min-w-[44px] flex items-center touch-manipulation"
          aria-label="Back to chats"
        >
          ← Back
        </Link>
        <h1 className="text-white font-medium truncate flex-1 min-w-0">
          {chat?.title ?? 'Chat'}
        </h1>
      </div>

      <div className="flex flex-1 min-h-0">
        {/* Sidebar: hidden on mobile, visible on desktop */}
        <div className="hidden md:flex md:w-80 flex-shrink-0 bg-dark-surface border-r border-dark-border flex-col overflow-y-auto">
          <div className="p-4 border-b border-dark-border">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-bold text-neon-red animate-neon">AI Coach</h1>
              <Link
                href="/chats"
                className="text-gray-400 hover:text-neon-red transition-colors cursor-pointer"
              >
                ← Back
              </Link>
            </div>
            {chat && (
              <div className="mb-4">
                {isEditingTitle ? (
                  <div className="space-y-2">
                    <Input
                      value={titleInput}
                      onChange={(e) => setTitleInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          handleSaveTitle();
                        } else if (e.key === 'Escape') {
                          handleCancelEditTitle();
                        }
                      }}
                      disabled={isUpdatingTitle}
                      className="mb-2"
                      autoFocus
                    />
                    <div className="flex gap-2">
                      <Button
                        onClick={handleSaveTitle}
                        isLoading={isUpdatingTitle}
                        variant="primary"
                        className="flex-1 text-sm py-2"
                      >
                        Save
                      </Button>
                      <Button
                        onClick={handleCancelEditTitle}
                        variant="secondary"
                        disabled={isUpdatingTitle}
                        className="flex-1 text-sm py-2"
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <h2 className="text-white font-medium flex-1">{chat.title}</h2>
                      <button
                        onClick={handleStartEditTitle}
                        className="text-gray-400 hover:text-neon-red transition-colors text-sm"
                        title="Edit title"
                      >
                        ✏️
                      </button>
                    </div>
                    <p className="text-xs text-gray-400">
                      Created: {formatDate(chat.datetimeCreated || chat.datetimeInserted)}
                    </p>
                  </div>
                )}
              </div>
            )}
            {documentsCount !== null && (
              <div className="text-sm text-gray-400">
                Documents in database: <span className="text-neon-red">{documentsCount}</span>
              </div>
            )}
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6 overscroll-contain">
            {isLoading ? (
              <div className="flex items-center justify-center h-full">
                <div className="animate-pulse text-neon-red">Loading messages...</div>
              </div>
            ) : messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-gray-400">
                <div className="text-center px-4">
                  <p className="text-xl mb-2">Start the conversation</p>
                  <p className="text-sm">Ask a question to the AI assistant</p>
                </div>
              </div>
            ) : (
              <div>
                {messages.map((message) => (
                  <MessageComponent key={message.id} message={message} />
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input: stack on very small screens */}
          <div className="border-t border-dark-border p-3 md:p-4 bg-dark-surface flex-shrink-0">
            <form onSubmit={handleSend} className="flex gap-2 md:gap-4">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Enter your question..."
                disabled={isSending}
                className="flex-1 min-w-0 min-h-[44px]"
              />
              <Button type="submit" isLoading={isSending} disabled={!input.trim()} className="min-h-[44px] px-4 touch-manipulation">
                Send
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

