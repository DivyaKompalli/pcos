import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export function ComprehensiveAssessment() {
  const [formData, setFormData] = useState({
    age: 26, bmi: 23.0, menstrual_regularity: 0, cycle_length_days: 28,
    irregular_periods: 0, hirsutism: 0, acne: 0, hair_loss: 0, weight_gain: 0,
    hemoglobin: 12.0, fatigue_level: 1, vegetarian_diet: 0, iron_rich_food: 2,
    menstrual_blood_loss: 1, pregnancy_count: 0,
    stress_level: 1, exercise_frequency: 2, fast_food_frequency: 1, diet_quality: 2, sleep_hours: 6.5
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
      const pcosData = { ...formData }
      const anemiaData = { ...formData }
      
      const [resPcos, resAnemia] = await Promise.all([
        axios.post('http://localhost:8000/api/predict/pcos', pcosData),
        axios.post('http://localhost:8000/api/predict/anemia', anemiaData)
      ])
      
      setResult({ pcos: resPcos.data, anemia: resAnemia.data })
    } catch (error) {
      alert("Error: " + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const renderResultBox = (title, data) => (
    <div className={`p-8 rounded-[2rem] border-l-8 flex-1 ${data.level === 'Elevated' ? 'border-error bg-error-container' : data.level === 'Moderate' ? 'border-secondary bg-secondary-container' : 'border-tertiary bg-tertiary-container'}`}>
      <h2 className="text-2xl font-headline font-bold mb-2">{title} Risk: {data.level}</h2>
      <p className="text-lg">Probability: {(data.probability * 100).toFixed(1)}%</p>
    </div>
  )

  return (
    <Layout>
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-headline font-bold text-primary mb-2">Comprehensive Assessment</h1>
        <p className="text-on-surface-variant mb-8 text-lg">Evaluate your risk for both PCOS and Anemia with a single, holistic health profile.</p>
        
        {!result ? (
          <form className="bg-surface-container-lowest p-8 rounded-[2rem] shadow-sm space-y-8" onSubmit={handleSubmit}>
            
            <div className="space-y-6">
              <h3 className="text-2xl font-headline font-bold text-primary border-b border-surface-variant pb-2">General Physical & Vitals</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div><label className="block text-sm font-semibold mb-2">Age</label><input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg flex-1 outline-none focus:ring-2 focus:ring-surface-tint" /></div>
                <div><label className="block text-sm font-semibold mb-2">BMI</label><input type="number" step="0.1" name="bmi" value={formData.bmi} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" /></div>
                <div><label className="block text-sm font-semibold mb-2">Hemoglobin (g/dL)</label><input type="number" step="0.5" name="hemoglobin" value={formData.hemoglobin} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" /></div>
              </div>
            </div>

            <div className="space-y-6">
              <h3 className="text-2xl font-headline font-bold text-primary border-b border-surface-variant pb-2">Reproductive Health</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">Menstrual Regularity</label>
                  <select name="menstrual_regularity" value={formData.menstrual_regularity} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint">
                    <option value={0}>Regular</option>
                    <option value={1}>Irregular</option>
                  </select>
                </div>
                <div><label className="block text-sm font-semibold mb-2">Cycle Length (Days)</label><input type="number" name="cycle_length_days" value={formData.cycle_length_days} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" /></div>
                <div><label className="block text-sm font-semibold mb-2">Pregnancy Count</label><input type="number" name="pregnancy_count" value={formData.pregnancy_count} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" /></div>
              </div>
            </div>

            <div className="space-y-6">
              <h3 className="text-2xl font-headline font-bold text-primary border-b border-surface-variant pb-2">Symptoms (Scale 0-4)</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {['irregular_periods', 'hirsutism', 'acne', 'hair_loss', 'weight_gain', 'fatigue_level', 'menstrual_blood_loss', 'stress_level'].map((field) => (
                  <div key={field}>
                    <label className="block text-sm font-semibold mb-2 capitalize">{field.replace(/_/g, ' ')}</label>
                    <input type="range" min="0" max="4" name={field} value={formData[field]} onChange={handleChange} className="w-full accent-primary" />
                    <div className="text-right text-xs text-on-surface-variant">{formData[field]}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-6">
              <h3 className="text-2xl font-headline font-bold text-primary border-b border-surface-variant pb-2">Lifestyle & Diet</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">Vegetarian Diet?</label>
                  <select name="vegetarian_diet" value={formData.vegetarian_diet} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint">
                    <option value={0}>No</option>
                    <option value={1}>Yes</option>
                  </select>
                </div>
                <div><label className="block text-sm font-semibold mb-2">Sleep Hours</label><input type="number" step="0.5" name="sleep_hours" value={formData.sleep_hours} onChange={handleChange} className="w-full bg-surface-container p-3 rounded-lg outline-none focus:ring-2 focus:ring-surface-tint" /></div>
                {['iron_rich_food', 'exercise_frequency', 'fast_food_frequency', 'diet_quality'].map((field) => (
                  <div key={field}>
                    <label className="block text-sm font-semibold mb-2 capitalize">{field.replace(/_/g, ' ')} (0-4)</label>
                    <input type="range" min="0" max="4" name={field} value={formData[field]} onChange={handleChange} className="w-full accent-primary" />
                    <div className="text-right text-xs text-on-surface-variant">{formData[field]}</div>
                  </div>
                ))}
              </div>
            </div>

            <button type="submit" disabled={loading} className="w-full py-4 bg-gradient-to-r from-primary to-primary-container text-white font-bold rounded-xl mt-6">
              {loading ? "Analyzing Both Conditions..." : "Assess Comprehensive Risk"}
            </button>
          </form>
        ) : (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row gap-6">
              {renderResultBox("PCOS", result.pcos)}
              {renderResultBox("Anemia", result.anemia)}
            </div>
            
            <div className="bg-surface-container-lowest p-8 rounded-[2rem] shadow-sm flex flex-col md:flex-row gap-8">
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-4 text-primary">PCOS AI Reasoning (SHAP)</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={result.pcos.shap_data?.features?.slice(0,5)} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                      <XAxis type="number" />
                      <YAxis dataKey="name" type="category" width={100} tick={{fontSize: 12}} />
                      <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} />
                      <Bar dataKey="value" fill="#006770" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-4 text-primary">Anemia AI Reasoning (SHAP)</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={result.anemia.shap_data?.features?.slice(0,5)} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                      <XAxis type="number" />
                      <YAxis dataKey="name" type="category" width={100} tick={{fontSize: 12}} />
                      <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} />
                      <Bar dataKey="value" fill="#9a442d" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
            
            <button onClick={() => setResult(null)} className="px-6 py-3 bg-surface-container text-primary font-bold rounded-lg border border-outline-variant">Back to Assessment</button>
          </div>
        )}
      </div>
    </Layout>
  )
}
