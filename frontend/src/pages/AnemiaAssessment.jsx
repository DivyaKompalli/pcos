import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export function AnemiaAssessment() {
  const [formData, setFormData] = useState({
    age: 28, hemoglobin: 12.0, vegetarian_diet: 0, fatigue_level: 1,
    iron_rich_food: 2, menstrual_blood_loss: 1, pregnancy_count: 0,
    diet_quality: 2, sleep_hours: 6.5, stress_level: 1
  })
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: Number(value) }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await axios.post('http://localhost:8000/api/predict/anemia', formData)
      setResult(res.data)
    } catch (error) {
      alert("Error: " + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-headline font-bold text-primary mb-2">Anemia Assessment</h1>
        <p className="text-on-surface-variant mb-8 text-lg">Provide your details to receive an AI-powered risk assessment.</p>
        
        {!result ? (
          <form className="bg-surface-container-lowest p-8 rounded-[2rem] shadow-sm space-y-6" onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold mb-2">Age</label>
                <input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-2">Hemoglobin level (g/dL) - Leave 12.0 if unknown</label>
                <input type="number" step="0.5" name="hemoglobin" value={formData.hemoglobin} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-2">Vegetarian Diet? (0=No, 1=Yes)</label>
                <select name="vegetarian_diet" value={formData.vegetarian_diet} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint">
                  <option value={0}>No</option>
                  <option value={1}>Yes</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-2">Pregnancy Count</label>
                <input type="number" name="pregnancy_count" value={formData.pregnancy_count} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" />
              </div>
              {['fatigue_level', 'iron_rich_food', 'menstrual_blood_loss', 'stress_level', 'diet_quality'].map((field) => (
                <div key={field}>
                  <label className="block text-sm font-semibold mb-2 capitalize">{field.replace(/_/g, ' ')} (0-4)</label>
                  <input type="range" min="0" max="4" name={field} value={formData[field]} onChange={handleChange} className="w-full accent-primary" />
                  <div className="text-right text-xs text-on-surface-variant">{formData[field]}</div>
                </div>
              ))}
              <div>
                <label className="block text-sm font-semibold mb-2">Sleep Hours</label>
                <input type="number" step="0.5" name="sleep_hours" value={formData.sleep_hours} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" />
              </div>
            </div>
            <button type="submit" disabled={loading} className="w-full py-4 bg-gradient-to-r from-primary to-primary-container text-white font-bold rounded-xl mt-6">
              {loading ? "Analyzing..." : "Assess Risk"}
            </button>
          </form>
        ) : (
          <div className="space-y-6">
            <div className={`p-8 rounded-[2rem] border-l-8 ${result.level === 'Elevated' ? 'border-error bg-error-container' : result.level === 'Moderate' ? 'border-secondary bg-secondary-container' : 'border-tertiary bg-tertiary-container'}`}>
              <h2 className="text-3xl font-headline font-bold mb-2">Risk Level: {result.level}</h2>
              <p className="text-xl">Probability: {(result.probability * 100).toFixed(1)}%</p>
              <p className="mt-4 text-sm opacity-80"> Disclaimer: This is a non-diagnostic risk assessment. Consult a doctor for medical advice.</p>
            </div>
            
            <div className="bg-surface-container-lowest p-8 rounded-[2rem] shadow-sm">
              <h3 className="text-xl font-bold mb-4 text-primary">AI Decision Reasoning (SHAP)</h3>
              <p className="text-sm mb-6 text-on-surface-variant">Top factors influencing this prediction:</p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={result.shap_data?.features?.slice(0,5)} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                    <XAxis type="number" />
                    <YAxis dataKey="name" type="category" width={100} tick={{fontSize: 12}} />
                    <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} />
                    <Bar dataKey="value" fill="#006770" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            <button onClick={() => setResult(null)} className="px-6 py-3 bg-surface-container text-primary font-bold rounded-lg border border-outline-variant">Back to Assessment</button>
          </div>
        )}
      </div>
    </Layout>
  )
}
