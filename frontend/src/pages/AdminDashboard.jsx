import React, { useEffect, useState } from 'react'
import { Layout } from '../components/Layout'
import axios from 'axios'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const COLORS = ['#006770', '#9a442d', '#ba1a1a']

export function AdminDashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    axios.get('http://localhost:8000/api/admin/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error("Could not load stats", err))
  }, [])

  if (!stats) return <Layout><div className="text-center p-20">Loading Dashboard...</div></Layout>

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-8">
        <div>
          <h1 className="text-4xl font-headline font-bold text-primary mb-2">Admin Dashboard</h1>
          <p className="text-on-surface-variant">Real-time assessment analytics and logs.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-surface-container p-8 rounded-3xl text-center">
            <h3 className="text-xl font-bold mb-2">Total Assessments</h3>
            <p className="text-6xl font-headline font-extrabold text-primary">{stats.total_assessments}</p>
          </div>
          <div className="bg-surface-container p-8 rounded-3xl text-center">
            <h3 className="text-xl font-bold mb-2">Assessments by Risk</h3>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={stats.risk_distribution} cx="50%" cy="50%" innerRadius={40} outerRadius={70} paddingAngle={5} dataKey="value">
                    {stats.risk_distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="bg-surface-container-lowest p-8 rounded-3xl shadow-sm">
          <h3 className="text-xl font-bold mb-6">Recent Assessment Logs</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase text-sm tracking-wider">
                  <th className="pb-4">Condition</th>
                  <th className="pb-4">Risk Level</th>
                  <th className="pb-4">Probability</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_logs.map((log, i) => (
                  <tr key={i} className="border-b border-outline-variant/10">
                    <td className="py-4 capitalize">{log.condition_type}</td>
                    <td className="py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold 
                        ${log.risk_level === 'Elevated' ? 'bg-error-container text-on-error-container' : 'bg-tertiary-container text-on-tertiary-container'}`}>
                        {log.risk_level}
                      </span>
                    </td>
                    <td className="py-4">{(log.risk_probability * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  )
}
