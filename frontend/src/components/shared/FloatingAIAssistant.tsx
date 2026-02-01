/**
 * Floating AI Assistant Component
 * Bottom-right floating chat interface
 */

import React, { useState } from 'react';

interface FloatingAIAssistantProps {
  userRole?: string;
}

const FloatingAIAssistant: React.FC<FloatingAIAssistantProps> = ({ userRole = 'OPERATOR' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; text: string }>>([]);
  const [input, setInput] = useState('');

  const quickQuestions = [
    'What is running now?',
    'Which orders are delayed?',
    "Show today's OEE",
  ];

  const handleQuickQuestion = (question: string) => {
    handleSend(question);
  };

  const handleSend = async (text: string = input) => {
    if (!text.trim()) return;

    const userMessage = { role: 'user' as const, text };
    setMessages([...messages, userMessage]);
    setInput('');

    // Simulated AI response (in real implementation, call the AI API)
    setTimeout(() => {
      const response = {
        role: 'assistant' as const,
        text: `I understand you're asking about: "${text}". This is a simulated response. In production, this would connect to the AI assistant API.`,
      };
      setMessages((prev) => [...prev, response]);
    }, 500);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {isOpen ? (
        <div className="bg-white rounded-lg shadow-2xl w-96 h-[500px] flex flex-col border border-gray-200">
          {/* Header */}
          <div className="bg-blue-600 text-white px-4 py-3 rounded-t-lg flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-2xl">✨</span>
              <h3 className="font-semibold">AI Assistant</h3>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 text-xl"
            >
              ×
            </button>
          </div>

          {/* Quick Questions */}
          {messages.length === 0 && (
            <div className="p-4 border-b">
              <p className="text-sm text-gray-600 mb-2">Quick questions:</p>
              <div className="flex flex-col gap-2">
                {quickQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleQuickQuestion(q)}
                    className="text-left px-3 py-2 bg-blue-50 hover:bg-blue-100 rounded text-sm border border-blue-200"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] px-4 py-2 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask a question..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={() => handleSend()}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg hover:bg-blue-700 transition-all hover:scale-110"
          aria-label="Open AI Assistant"
        >
          <span className="text-3xl">✨</span>
        </button>
      )}
    </div>
  );
};

export default FloatingAIAssistant;
