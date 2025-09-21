'use client'

import { useState, useCallback } from 'react'

export interface Message {
  id: string
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

const mockResponses = [
  "I'd be happy to help you explore career opportunities! What specific area interests you most?",
  "Based on your profile, I see great potential in tech roles. Would you like to discuss specific career paths?",
  "That's an excellent question! Let me analyze your skills and suggest some personalized recommendations.",
  "I can help you create a learning plan tailored to your goals. What timeline are you working with?",
  "Great choice! This skill is in high demand. I can show you the best resources to get started.",
  "Let's dive deeper into that. What specific challenges are you facing in this area?",
  "I understand your concern. Many professionals face similar challenges. Here's what I recommend...",
  "That's a smart approach! Have you considered these complementary skills that could boost your career?",
]

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hi! I'm your AI Career Advisor. I can help you with career planning, skill development, and job market insights. What would you like to explore today?",
      sender: 'ai',
      timestamp: new Date(),
    }
  ])
  const [isTyping, setIsTyping] = useState(false)

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsTyping(true)

    // Simulate AI response delay
    const delay = 1000 + Math.random() * 1500
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: mockResponses[Math.floor(Math.random() * mockResponses.length)],
        sender: 'ai',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, aiResponse])
      setIsTyping(false)
    }, delay)
  }, [])

  const clearMessages = useCallback(() => {
    setMessages([
      {
        id: '1',
        text: "Hi! I'm your AI Career Advisor. I can help you with career planning, skill development, and job market insights. What would you like to explore today?",
        sender: 'ai',
        timestamp: new Date(),
      }
    ])
  }, [])

  return {
    messages,
    isTyping,
    sendMessage,
    clearMessages,
  }
}