import React from 'react';
import { MessageSquare, Activity, Cpu, Sliders, ShieldAlert, TrendingUp, BookOpen, FileText, HeartPulse } from 'lucide-react';

const NAV_ITEMS = [
  { id: 'chat', label: 'Chatbot AI', icon: MessageSquare, badge: 'NLP' },
  { id: 'profile', label: 'Risk Profile', icon: Activity, badge: '5 Diseases' },
  { id: 'explainability', label: 'Explainability', icon: Cpu, badge: 'SHAP' },
  { id: 'whatif', label: 'What-If Engine', icon: Sliders, badge: 'Sim' },
  { id: 'disagreement', label: 'Model Comparison', icon: ShieldAlert, badge: 'Ensemble' },
  { id: 'timeline', label: 'Health Trends', icon: TrendingUp, badge: 'Timeline' },
  { id: 'modelcards', label: 'Model Cards', icon: BookOpen, badge: 'Mitchell' },
  { id: 'reports', label: 'Reports', icon: FileText, badge: 'PDF' }
];

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <div className="w-full font-sans">
      {/* Step 2.1: Brand & Top Header Bar */}
      <header 
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          background: '#0f172a',
          borderBottom: '1px solid #1e293b',
          padding: '1rem 2.5rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        {/* Left Side: Brand Logo, Title & Subtitle */}
        <div className="flex flex-col">
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => setActiveTab('chat')}
            style={{ display: 'flex', alignItems: 'center', gap: '12px' }}
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-sky-500 to-indigo-600 flex items-center justify-center shadow-md shadow-cyan-500/20 group-hover:scale-105 transition-transform">
              <HeartPulse className="w-5 h-5 text-slate-950 font-bold" />
            </div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-extrabold tracking-tight text-white group-hover:text-cyan-400 transition-colors">
                ExplainHealth <span className="gradient-text-cyan">AI</span>
              </h1>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">
                v1.0 XAI
              </span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 font-medium mt-0.5">
            Conversational Multi-Disease Interpretable ML
          </p>
        </div>

        {/* Right Side: API Status Connected Badge with Glowing Dot */}
        <div 
          style={{
            background: 'rgba(16, 185, 129, 0.1)',
            color: '#10b981',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            padding: '6px 14px',
            borderRadius: '20px',
            fontSize: '0.85rem',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#10b981', boxShadow: '0 0 8px #10b981' }}></span>
          <span>API Status: Connected</span>
        </div>
      </header>

      {/* Step 2.2: Main Navigation Ribbon */}
      <nav 
        style={{
          display: 'flex',
          gap: '8px',
          background: '#131c2e',
          borderBottom: '1px solid #1e293b',
          padding: '0.75rem 2.5rem',
          overflowX: 'auto'
        }}
      >
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                backgroundColor: isActive ? '#2563eb' : 'transparent',
                color: isActive ? '#ffffff' : '#94a3b8',
                fontWeight: isActive ? 600 : 500,
                borderRadius: '8px',
                padding: '8px 16px',
                fontSize: '0.85rem',
                border: 'none',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                whiteSpace: 'nowrap',
                transition: 'all 0.15s ease-in-out'
              }}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
