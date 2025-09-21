'use client'

import { useState, useEffect } from 'react'

export function ChatDrawer() {
  const [isOpen, setIsOpen] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const [messages, setMessages] = useState([
    {
      id: '1',
      text: "Hi! I'm your AI Career Advisor. How can I help you today?",
      sender: 'ai',
      timestamp: new Date(),
    }
  ])

  const suggestedQuestions = [
    "What career path should I choose?",
    "How can I improve my skills?",
    "What's trending in tech jobs?",
    "Help me prepare for interviews",
  ]

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return

    const userMessage = {
      id: Date.now().toString(),
      text: text.trim(),
      sender: 'user' as const,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "That's a great question! Let me help you with that.",
        "I'd be happy to provide some guidance on this topic.",
        "Based on current market trends, here's what I recommend...",
        "Great choice! This is definitely worth exploring further.",
      ]
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        text: responses[Math.floor(Math.random() * responses.length)],
        sender: 'ai' as const,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, aiResponse])
    }, 1000)
  }

  // Handle Ctrl+K to open chat
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        setIsOpen(true)
      }
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false)
      }
    }
    
    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', handleKeyDown)
      return () => window.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen])

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-2xl border-2 border-white/20 hover:shadow-cyan-500/30 hover:scale-110 transition-all duration-300"
      >
        <div className="relative">
          <div className="absolute inset-0 rounded-full bg-cyan-400 opacity-30 animate-ping"></div>
          <div className="relative z-10 flex items-center justify-center h-full">
            {isOpen ? (
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            )}
          </div>
        </div>
      </button>

      {/* Keyboard shortcut hint */}
      {!isOpen && (
        <div className="fixed bottom-24 right-6 z-40 bg-slate-900/80 backdrop-blur-md rounded-lg px-3 py-2 text-sm text-gray-300 border border-white/20">
          Press <kbd className="px-2 py-1 bg-white/10 rounded text-xs">Ctrl+K</kbd> to chat
        </div>
      )}

      {/* Chat Drawer */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            onClick={() => setIsOpen(false)}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          />

          {/* Drawer */}
          <div className="fixed right-0 top-0 h-full w-full max-w-md bg-slate-900/95 backdrop-blur-xl border-l border-white/20 shadow-2xl z-50 flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-white/20">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">AI</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Career Advisor</h3>
                  <p className="text-sm text-gray-400">Always here to help</p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
                      message.sender === 'user'
                        ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white'
                        : 'bg-white/10 border border-white/20 text-gray-200'
                    }`}
                  >
                    <p className="mb-1">{message.text}</p>
                    <p className={`text-xs opacity-70 ${
                      message.sender === 'user' ? 'text-white/70' : 'text-gray-400'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}

              {/* Suggested questions - only show if no user messages yet */}
              {messages.length === 1 && (
                <div className="space-y-2">
                  <p className="text-sm text-gray-400 mb-3">Quick questions to get started:</p>
                  {suggestedQuestions.map((question) => (
                    <button
                      key={question}
                      onClick={() => handleSendMessage(question)}
                      className="block w-full text-left p-3 bg-white/5 border border-white/20 rounded-lg hover:border-white/30 hover:bg-white/10 transition-all duration-200 text-sm text-gray-300"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Input */}
            <div className="border-t border-white/20 p-6">
              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value)}
                  onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => {
                    if (e.key === 'Enter') {
                      e.preventDefault()
                      handleSendMessage(inputValue)
                    }
                  }}
                  placeholder="Ask me anything about your career..."
                  className="flex-1 bg-white/5 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-white/30 transition-all duration-200"
                />
                <button
                  onClick={() => handleSendMessage(inputValue)}
                  disabled={!inputValue.trim()}
                  className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-3 rounded-xl shadow-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-cyan-500/30 transition-all duration-200"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2 text-center">
                Press Enter to send • Esc to close
              </p>
            </div>
          </div>
        </>
      )}
    </>
  )
}