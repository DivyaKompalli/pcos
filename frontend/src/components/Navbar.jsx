import React from 'react'
import { Link } from 'react-router-dom'

export function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 bg-[#fdfae7]/95 backdrop-blur-xl shadow-sm border-b border-surface-variant/30">
      <div className="flex justify-between items-center px-8 py-4 max-w-7xl mx-auto">
        <Link to="/" className="text-2xl font-bold text-[#006770] font-headline tracking-tight">
          Serene Sanctuary
        </Link>
        <div className="hidden md:flex gap-6 items-center flex-wrap">
          <Link to="/pcos-assessment" className="text-[#3e494a] font-headline tracking-tight hover:text-[#006770] transition-colors whitespace-nowrap">PCOS</Link>
          <Link to="/anemia-assessment" className="text-[#3e494a] font-headline tracking-tight hover:text-[#006770] transition-colors whitespace-nowrap">Anemia</Link>
          <Link to="/comprehensive" className="text-[#3e494a] font-headline font-bold text-[#12828c] tracking-tight hover:text-[#006770] transition-colors whitespace-nowrap">Comprehensive</Link>
          <Link to="/admin" className="text-[#3e494a] font-headline tracking-tight hover:text-[#006770] transition-colors whitespace-nowrap">Dashboard</Link>
        </div>
      </div>
    </nav>
  )
}
