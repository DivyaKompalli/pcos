import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { PCOSAssessment } from './pages/PCOSAssessment'
import { AnemiaAssessment } from './pages/AnemiaAssessment'
import { AdminDashboard } from './pages/AdminDashboard'
import { ComprehensiveAssessment } from './pages/ComprehensiveAssessment'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pcos-assessment" element={<PCOSAssessment />} />
        <Route path="/anemia-assessment" element={<AnemiaAssessment />} />
        <Route path="/comprehensive" element={<ComprehensiveAssessment />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
