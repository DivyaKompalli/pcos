import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { MessageCircle, X } from 'lucide-react'

export function Chatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'model', content: "Hello! I'm the Serene Sanctuary health educator AI. Ask me about PCOS, Anemia, diet, or lifestyle. Please note, I cannot provide clinical diagnoses." }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  
  const bottomRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Send the current history excluding the immediate new message
      const history = messages.slice(1).map(m => ({ role: m.role, content: m.content }))
      
      const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      const res = await axios.post(`${apiUrl}/api/chat`, {
        message: userMessage.content,
        history: history
      })
      
      setMessages(prev => [...prev, { role: 'model', content: res.data.reply }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'model', content: "Sorry, I encountered an error. Please verify the Gemini API key." }])
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="fixed bottom-8 right-8 p-4 bg-primary text-white rounded-full shadow-2xl hover:scale-105 transition-transform z-50 flex items-center justify-center">
        <MessageCircle size={28} />
      </button>
    )
  }

  return (
    <div className="fixed bottom-8 right-8 w-96 max-w-[90vw] h-[500px] bg-white rounded-3xl shadow-2xl flex flex-col z-50 border border-surface-variant/30 overflow-hidden">
      <div className="bg-primary text-white p-4 flex justify-between items-center">
        <div className="font-bold">Health Educator AI</div>
        <button onClick={() => setIsOpen(false)} className="hover:text-white/70">
          <X size={24} />
        </button>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-surface-container-low">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-3 text-sm ${
              msg.role === 'user' 
                ? 'bg-primary text-white rounded-br-none' 
                : 'bg-white text-on-surface border border-surface-variant/30 rounded-bl-none shadow-sm'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white text-on-surface border border-surface-variant/30 rounded-2xl rounded-bl-none p-3 text-sm shadow-sm opacity-60">
              Thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      
      <form onSubmit={handleSend} className="p-3 bg-white border-t border-surface-variant/30 flex gap-2">
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 bg-surface-container outline-none px-4 py-2 rounded-xl text-sm"
          disabled={loading}
        />
        <button 
          type="submit" 
          disabled={loading || !input.trim()}
          className="bg-primary text-white px-4 py-2 rounded-xl text-sm font-bold disabled:opacity-50">
          Send
        </button>
      </form>
    </div>
  )
}
