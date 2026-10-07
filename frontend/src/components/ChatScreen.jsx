import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, ArrowRight, ShieldAlert, CheckCircle, Activity, HelpCircle, AlertTriangle } from 'lucide-react';

const SUGGESTED_PROMPTS = [
  { label: 'Diabetes Risk', query: 'Check my diabetes risk (glucose: 165, BMI: 31, age: 45, BP: 85)', tag: 'En' },
  { label: 'Tanglish Check', query: 'enakku diabetes risk check pannanum', tag: 'Tanglish' },
  { label: 'Heart Disease', query: 'Check heart risk (age: 55, BP: 140, cholesterol: 240, max heart rate: 150)', tag: 'En' },
  { label: 'Stroke Risk', query: 'Check stroke risk (age: 65, hypertension: yes, avg glucose: 150, BMI: 30.5)', tag: 'En' }
];

export default function ChatScreen({ onNavigateToExplainability, onNavigateToWhatIf }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: "👋 Welcome to **ExplainHealth AI**!\n\nI am your conversational healthcare risk assistant. I handle natural-language interactions in English, Tamil, and Tanglish while delegating all disease risk predictions to 5 specialized, calibrated machine-learning models.\n\nSelect an active disease module above or type your clinical measurements below to begin!"
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedDisease, setSelectedDisease] = useState('diabetes');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async (textToSend) => {
    const query = textToSend || inputText;
    if (!query.trim() || loading) return;

    const userMsg = { id: Date.now(), role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputText('');
    setLoading(true);

    try {
      const resp = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: query,
          session_id: sessionId,
          disease_override: selectedDisease,
          anonymized_id: 'demo_patient_01'
        })
      });

      const data = await resp.json();
      if (data.session_id) setSessionId(data.session_id);

      const botMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.message,
        assessment: data.assessment_result,
        missing_fields: data.missing_fields,
        is_complete: data.is_complete
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: '❌ **Backend Error**: Could not connect to ExplainHealth API server (http://localhost:8000). Please ensure the FastAPI backend is running.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 flex flex-col h-[calc(100vh-5rem)]">
      
      {/* Top Disease Module Header */}
      <div className="glass-card p-3.5 mb-4 rounded-2xl flex flex-wrap items-center justify-between gap-3 border border-slate-800">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-cyan-400" />
          </div>
          <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">Active Disease Model:</span>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto py-1">
          {[
            { id: 'diabetes', label: 'Diabetes' },
            { id: 'heart_disease', label: 'Heart Disease' },
            { id: 'breast_cancer', label: 'Breast Cancer' },
            { id: 'lung_cancer', label: 'Lung Cancer' },
            { id: 'stroke', label: 'Stroke' }
          ].map((d) => (
            <button
              key={d.id}
              onClick={() => setSelectedDisease(d.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
                selectedDisease === d.id
                  ? 'bg-gradient-to-r from-cyan-500 to-indigo-600 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                  : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Stream */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-xl bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center shrink-0 mt-1">
                <Bot className="w-4 h-4 text-cyan-400" />
              </div>
            )}

            <div
              className={`max-w-2xl rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white rounded-tr-none shadow-lg shadow-cyan-500/10'
                  : 'glass-card text-slate-200 rounded-tl-none border border-slate-800/80'
              }`}
            >
              <div className="whitespace-pre-wrap font-sans">{msg.content}</div>

              {/* KPI Risk Summary Overlay Card */}
              {msg.assessment && msg.assessment.success && (
                <div className="mt-4 p-5 rounded-2xl bg-slate-950/90 border border-slate-800/90 space-y-4 shadow-xl">
                  
                  {/* KPI Header */}
                  <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                    <div>
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                        {msg.assessment.display_name}
                      </span>
                      <div className="text-2xl font-black tracking-tight text-white mt-0.5">
                        Model Risk: <span className={
                          msg.assessment.severity === 'elevated' ? 'text-red-400' :
                          msg.assessment.severity === 'moderate' ? 'text-amber-400' : 'text-emerald-400'
                        }>{msg.assessment.percentage}</span>
                      </div>
                    </div>

                    <div className="flex flex-col items-end">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                          msg.assessment.severity === 'elevated'
                            ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                            : msg.assessment.severity === 'moderate'
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        }`}
                      >
                        {msg.assessment.risk_tier}
                      </span>
                      <span className="text-[10px] text-cyan-400 mt-1 font-medium">
                        {msg.assessment.uncertainty?.confidence_level}
                      </span>
                    </div>
                  </div>

                  {/* Why Factors Progress Bars */}
                  {msg.assessment.shap_explanation?.why_factors_increasing_risk && (
                    <div className="space-y-2 pt-1">
                      <div className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center justify-between">
                        <span>Why? (Top Risk Factors)</span>
                        <span className="text-[10px] text-slate-500 font-normal">SHAP Impact Score</span>
                      </div>

                      {msg.assessment.shap_explanation.why_factors_increasing_risk.slice(0, 3).map((f, i) => (
                        <div key={i} className="space-y-1">
                          <div className="flex justify-between text-xs text-slate-300">
                            <span className="font-medium">{f.label} ({f.original_value})</span>
                            <span className="text-amber-400 font-mono font-bold">+{f.shap_value.toFixed(2)}</span>
                          </div>
                          <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden border border-slate-800">
                            <div
                              className="bg-gradient-to-r from-amber-500 to-orange-500 h-1.5 rounded-full"
                              style={{ width: `${Math.min(100, Math.max(15, f.shap_value * 120))}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Why Not Factors Progress Bars */}
                  {msg.assessment.shap_explanation?.why_not_factors_decreasing_risk && (
                    <div className="space-y-2 pt-2">
                      <div className="text-xs font-bold text-sky-400 uppercase tracking-wider flex items-center justify-between">
                        <span>Why Not? (Protective Factors)</span>
                      </div>

                      {msg.assessment.shap_explanation.why_not_factors_decreasing_risk.slice(0, 2).map((f, i) => (
                        <div key={i} className="space-y-1">
                          <div className="flex justify-between text-xs text-slate-300">
                            <span className="font-medium">{f.label} ({f.original_value})</span>
                            <span className="text-sky-400 font-mono font-bold">{f.shap_value.toFixed(2)}</span>
                          </div>
                          <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden border border-slate-800">
                            <div
                              className="bg-gradient-to-r from-sky-500 to-indigo-500 h-1.5 rounded-full"
                              style={{ width: `${Math.min(100, Math.max(15, Math.abs(f.shap_value) * 120))}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Quick Action Navigation Buttons */}
                  <div className="flex flex-col sm:flex-row items-center gap-2 pt-3 border-t border-slate-800/80">
                    <button
                      onClick={() => onNavigateToExplainability(msg.assessment)}
                      className="w-full sm:w-1/2 py-2 px-3 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 text-xs font-bold border border-cyan-500/30 flex items-center justify-center gap-1.5 transition-all"
                    >
                      Inspect SHAP Waterfall <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => onNavigateToWhatIf(msg.assessment)}
                      className="w-full sm:w-1/2 py-2 px-3 rounded-xl bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 text-xs font-bold border border-indigo-500/30 flex items-center justify-center gap-1.5 transition-all"
                    >
                      Simulate What-If <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-xl bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4 text-indigo-400" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2.5 text-cyan-400 text-xs font-semibold py-3 px-4 glass-card rounded-2xl w-max">
            <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
            Analyzing parameters with calibrated ML models & SHAP explainer...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Prompt Chips */}
      <div 
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '8px',
          padding: '10px 0',
          alignItems: 'center'
        }}
      >
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0 mr-1">Prompts:</span>
        {SUGGESTED_PROMPTS.map((p, i) => (
          <button
            key={i}
            onClick={() => handleSendMessage(p.query)}
            className="chip-btn"
            style={{
              background: '#1e293b',
              color: '#94a3b8',
              border: '1px solid #334155',
              borderRadius: '20px',
              padding: '6px 14px',
              fontSize: '0.85rem',
              fontWeight: 500,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-slate-900 text-cyan-400 border border-slate-700">{p.tag}</span>
            <span>{p.label}</span>
          </button>
        ))}
      </div>

      {/* Message Input Bar */}
      <div className="pt-2">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          style={{
            display: 'flex',
            gap: '10px',
            background: '#1e293b',
            border: '1px solid #334155',
            borderRadius: '12px',
            padding: '6px 8px 6px 16px',
            alignItems: 'center'
          }}
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your parameters in English, Tamil, or Tanglish (e.g., glucose 165, BMI 31, age 45)..."
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              color: '#f8fafc',
              fontSize: '0.9rem',
              outline: 'none',
              padding: '6px 0'
            }}
          />
          <button
            type="submit"
            disabled={loading || !inputText.trim()}
            style={{
              background: '#2563eb',
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              width: '38px',
              height: '38px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              opacity: (loading || !inputText.trim()) ? 0.5 : 1,
              transition: 'all 0.2s ease',
              flexShrink: 0
            }}
          >
            <Send className="w-4 h-4 text-white" />
          </button>
        </form>
      </div>
    </div>
  );
}
