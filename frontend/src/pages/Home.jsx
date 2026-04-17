import React from 'react'
import { Link } from 'react-router-dom'
import { Layout } from '../components/Layout'

export function Home() {
  return (
    <Layout>
      <section className="relative py-20 px-4 md:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="z-10">
            <span className="inline-block px-4 py-1.5 mb-6 bg-secondary-fixed text-on-secondary-fixed rounded-full text-xs font-bold tracking-widest uppercase">
              AI-Powered Screening
            </span>
            <h1 className="text-5xl md:text-7xl font-headline font-extrabold text-primary leading-tight mb-6">
              Empowering Your Health Journey
            </h1>
            <p className="text-lg md:text-xl text-on-surface-variant mb-10 max-w-lg">
              Clinical-grade AI designed specifically for women. Discover personalized insights for PCOS and Anemia with ease, privacy, and precision.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link to="/pcos-assessment" className="px-8 py-4 bg-gradient-to-r from-primary to-primary-container text-on-primary rounded-xl font-bold text-center text-lg shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform">
                PCOS Assessment
              </Link>
              <Link to="/anemia-assessment" className="px-8 py-4 bg-surface-container-lowest text-primary rounded-xl font-bold text-lg text-center hover:bg-surface-container-high transition-colors">
                Anemia Assessment
              </Link>
            </div>
          </div>
          <div className="relative hidden md:block">
            <div className="absolute -top-20 -right-20 w-96 h-96 bg-primary-fixed/30 rounded-full blur-[100px]"></div>
            <div className="absolute -bottom-20 -left-10 w-72 h-72 bg-secondary-fixed/20 rounded-full blur-[80px]"></div>
            <div className="relative glass-card p-4 rounded-[2rem] shadow-2xl h-[400px] flex items-center justify-center">
              <span className="text-primary font-bold text-xl">The Serene Sanctuary</span>
            </div>
          </div>
        </div>
      </section>
      
      <section className="bg-surface-container-low py-12 rounded-[2rem] mt-12">
        <p className="text-center text-sm font-semibold text-on-surface-variant/60 uppercase tracking-[0.2em] mb-8">Trusted by researchers</p>
        <div className="flex flex-wrap justify-center gap-12 font-headline font-bold text-lg text-primary/80">
          <div>HIPAA Compliant Structure</div>
          <div>Evidence Based AI</div>
          <div>Inclusive Models</div>
        </div>
      </section>
    </Layout>
  )
}
