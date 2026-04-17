import React from 'react'
import { Navbar } from './Navbar'
import { Chatbot } from './Chatbot'

export function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col relative">
      <Navbar />
      <main className="flex-1 pt-24 pb-12 px-8 max-w-7xl mx-auto w-full">
        {children}
      </main>
      <Chatbot />
    </div>
  )
}
