import React, { useState, useEffect } from 'react';
import { Cpu, Sparkles, AlertCircle, Info, TrendingUp } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';

export default function ExplainabilityScreen({ activeAssessment }) {
  const [selectedDisease, setSelectedDisease] = useState(activeAssessment?.disease || 'diabetes');
  const [assessment, setAssessment] = useState(activeAssessment || null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!assessment || assessment.disease !== selectedDisease) {
      fetchSHAPAnalysis(selectedDisease);
    }
  }, [selectedDisease]);

  const fetchSHAPAnalysis = async (disease) => {
    setLoading(true);
    try {
      const resp = await fetch(`http://localhost:8000/predict/${disease}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_data: {}, anonymized_id: 'demo_patient_01' })
      });
      const data = await resp.json();
      setAssessment(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const chartData = assessment?.shap_explanation?.all_contributions
    ? assessment.shap_explanation.all_contributions.map((c) => ({
        name: c.label,
        shap_value: c.shap_value,
        original_value: c.original_value
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-widest mb-1">
            <Cpu className="w-4 h-4" /> Explainable AI Layer (XAI)
          </div>
          <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">
            SHAP Local Feature Attribution Engine
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Calculates exact mathematical Shapley values describing how each feature pushes the model output away from the background baseline.
          </p>
        </div>

        {/* Disease Module Switcher */}
        <div className="flex items-center gap-1.5 bg-slate-900/90 p-2 rounded-2xl border border-slate-800 shrink-0">
          {['diabetes', 'heart_disease', 'breast_cancer', 'lung_cancer', 'stroke'].map((d) => (
            <button
              key={d}
              onClick={() => setSelectedDisease(d)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold capitalize transition-all duration-200 ${
                selectedDisease === d
                  ? 'bg-gradient-to-r from-cyan-500 to-indigo-600 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {d.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center text-cyan-400 font-medium flex items-center justify-center gap-3 glass-card rounded-3xl">
          <div className="w-5 h-5 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
          Computing exact Shapley values...
        </div>
      ) : (
        assessment && (
          <div className="space-y-6">
            
            {/* KPI Risk Summary Banner */}
            <div className="glass-card p-6 rounded-3xl border border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  {assessment.display_name}
                </span>
                <div className="text-3xl font-black text-white mt-1">
                  Model Estimated Risk: <span className={
                    assessment.severity === 'elevated' ? 'text-red-400' :
                    assessment.severity === 'moderate' ? 'text-amber-400' : 'text-emerald-400'
                  }>{assessment.percentage}</span>
                </div>
                <div className="text-xs text-slate-400 mt-1">
                  Confidence Tier: <strong className="text-cyan-400">{assessment.uncertainty?.confidence_level}</strong>
                </div>
              </div>

              <div className="md:col-span-2 p-4 rounded-2xl bg-slate-950/80 border border-slate-800 text-xs text-slate-300 leading-relaxed space-y-1.5">
                <strong className="text-cyan-400 flex items-center gap-1.5">
                  <Info className="w-4 h-4" /> Plain-Language Non-Causal Explanation:
                </strong>
                <p>{assessment.shap_explanation?.summary_explanation}</p>
              </div>
            </div>

            {/* SHAP Recharts Horizontal Waterfall Bar Chart */}
            <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
                  SHAP Contribution Waterfall Chart
                </h3>
                <span className="text-xs text-slate-400">
                  Amber (+ Risk Increasing) vs Sky Blue (- Protective)
                </span>
              </div>

              <div className="h-96 w-full pt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 140, bottom: 5 }}>
                    <XAxis type="number" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                    <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fontSize: 11 }} width={130} />
                    <Tooltip
                      content={({ payload }) => {
                        if (!payload || !payload.length) return null;
                        const data = payload[0].payload;
                        return (
                          <div className="p-3 bg-slate-900 border border-slate-700 rounded-xl text-xs space-y-1 shadow-2xl">
                            <div className="font-bold text-slate-100">{data.name}</div>
                            <div>Patient Input Value: <strong className="text-cyan-400">{data.original_value}</strong></div>
                            <div>SHAP Value: <strong className={data.shap_value > 0 ? "text-amber-400" : "text-sky-400"}>{data.shap_value > 0 ? `+${data.shap_value.toFixed(4)}` : data.shap_value.toFixed(4)}</strong></div>
                          </div>
                        );
                      }}
                    />
                    <ReferenceLine x={0} stroke="#475569" strokeDasharray="3 3" />
                    <Bar dataKey="shap_value" radius={[0, 4, 4, 0]}>
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.shap_value >= 0 ? '#f59e0b' : '#38bdf8'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Why & Why Not Detailed Visual Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Factors Increasing Risk */}
              <div className="glass-card p-6 rounded-3xl border-l-4 border-l-amber-500 space-y-4">
                <h4 className="text-xs font-extrabold text-amber-400 uppercase tracking-widest flex items-center justify-between">
                  <span>Why? (Factors Elevating Model Output)</span>
                  <span className="text-[10px] text-slate-500 font-normal">SHAP Contribution</span>
                </h4>

                <div className="space-y-3">
                  {assessment.shap_explanation?.why_factors_increasing_risk?.map((f, i) => (
                    <div key={i} className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-slate-200">{f.label}</span>
                        <span className="text-amber-400 font-mono font-bold">+{f.shap_value.toFixed(4)}</span>
                      </div>
                      <div className="flex justify-between items-center text-[11px] text-slate-400">
                        <span>Patient Value: <strong className="text-slate-200">{f.original_value}</strong></span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Factors Decreasing Risk */}
              <div className="glass-card p-6 rounded-3xl border-l-4 border-l-sky-500 space-y-4">
                <h4 className="text-xs font-extrabold text-sky-400 uppercase tracking-widest flex items-center justify-between">
                  <span>Why Not? (Factors Lowering Model Output)</span>
                  <span className="text-[10px] text-slate-500 font-normal">SHAP Contribution</span>
                </h4>

                <div className="space-y-3">
                  {assessment.shap_explanation?.why_not_factors_decreasing_risk?.map((f, i) => (
                    <div key={i} className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-slate-200">{f.label}</span>
                        <span className="text-sky-400 font-mono font-bold">{f.shap_value.toFixed(4)}</span>
                      </div>
                      <div className="flex justify-between items-center text-[11px] text-slate-400">
                        <span>Patient Value: <strong className="text-slate-200">{f.original_value}</strong></span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </div>
        )
      )}
    </div>
  );
}
