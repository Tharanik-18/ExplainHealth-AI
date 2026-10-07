import React, { useState } from 'react';
import { ShieldAlert, RefreshCw, AlertTriangle, CheckCircle2, Cpu } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function ModelComparisonScreen() {
  const [disease, setDisease] = useState('diabetes');
  const [loading, setLoading] = useState(false);
  const [comparisonResult, setComparisonResult] = useState(null);

  const handleRunComparison = async () => {
    setLoading(true);
    try {
      const resp = await fetch(`http://localhost:8000/compare-models/${disease}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_data: {} })
      });
      const data = await resp.json();
      setComparisonResult(data);
    } catch (err) {
      alert('Error running model comparison engine');
    } finally {
      setLoading(false);
    }
  };

  const chartData = comparisonResult?.models_comparison
    ? comparisonResult.models_comparison.map((m) => ({
        name: m.model_name,
        probability: Number((m.probability * 100).toFixed(1)),
        verdict: m.risk_verdict
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-widest mb-1">
            <ShieldAlert className="w-4 h-4" /> Novel Feature #2: Model Disagreement Engine
          </div>
          <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">
            Multi-Architecture Model Comparison
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Executes multiple candidate classifier families (Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM) on identical parameters to prevent false certainty.
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto shrink-0">
          <select
            value={disease}
            onChange={(e) => setDisease(e.target.value)}
            className="bg-slate-900 text-xs text-slate-200 font-semibold rounded-xl px-3 py-2.5 border border-slate-800"
          >
            <option value="diabetes">Diabetes Suite</option>
            <option value="heart_disease">Heart Disease Suite</option>
            <option value="breast_cancer">Breast Cancer Suite</option>
            <option value="lung_cancer">Lung Cancer Suite</option>
            <option value="stroke">Stroke Suite</option>
          </select>

          <button
            onClick={handleRunComparison}
            disabled={loading}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 font-bold text-slate-950 text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition-all"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Cpu className="w-4 h-4" />}
            Run Multi-Model Comparison
          </button>
        </div>
      </div>

      {comparisonResult ? (
        <div className="space-y-6">
          
          {/* Disagreement / Consensus Banner */}
          <div
            className={`p-5 rounded-3xl border flex items-start gap-4 ${
              comparisonResult.disagreement_detected
                ? 'bg-red-500/10 border-red-500/30 text-red-300'
                : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
            }`}
          >
            {comparisonResult.disagreement_detected ? (
              <AlertTriangle className="w-6 h-6 text-red-400 shrink-0 mt-0.5" />
            ) : (
              <CheckCircle2 className="w-6 h-6 text-emerald-400 shrink-0 mt-0.5" />
            )}

            <div>
              <div className="font-extrabold text-sm uppercase tracking-wider">
                {comparisonResult.disagreement_detected ? 'Model Disagreement Detected' : 'High Model Consensus'}
              </div>
              <p className="text-xs mt-1 leading-relaxed">{comparisonResult.interpretation}</p>
            </div>
          </div>

          {/* Bar Chart Comparison */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h4 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
              Side-by-Side Model Probabilities (% Estimated Risk)
            </h4>

            <div className="h-80 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#94a3b8" domain={[0, 100]} unit="%" />
                  <Tooltip
                    content={({ payload }) => {
                      if (!payload || !payload.length) return null;
                      const data = payload[0].payload;
                      return (
                        <div className="p-3 bg-slate-900 border border-slate-700 rounded-xl text-xs space-y-1 shadow-2xl">
                          <div className="font-bold text-slate-100">{data.name}</div>
                          <div>Estimated Risk: <strong className="text-cyan-400">{data.probability}%</strong></div>
                          <div>Category: <strong className="text-slate-300">{data.verdict}</strong></div>
                        </div>
                      );
                    }}
                  />
                  <Bar dataKey="probability" radius={[6, 6, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.probability >= 50 ? '#f43f5e' : '#10b981'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Table Details */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h4 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Architecture Details</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="pb-3 font-semibold">Candidate Architecture</th>
                    <th className="pb-3 font-semibold">Probability Estimate</th>
                    <th className="pb-3 font-semibold">Category</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {comparisonResult.models_comparison.map((m, i) => (
                    <tr key={i} className="hover:bg-slate-800/40">
                      <td className="py-3.5 font-bold text-slate-200">{m.model_name}</td>
                      <td className="py-3.5 font-bold text-cyan-400 font-mono text-sm">{m.percentage}</td>
                      <td className="py-3.5">
                        <span
                          className={`px-2.5 py-1 rounded-full text-[11px] font-bold ${
                            m.probability >= 0.50
                              ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                              : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                          }`}
                        >
                          {m.risk_verdict}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="glass-card p-12 rounded-3xl text-center text-slate-400 space-y-4 border border-slate-800">
          <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mx-auto">
            <ShieldAlert className="w-7 h-7" />
          </div>
          <h3 className="text-base font-bold text-slate-200">Model Disagreement Suite Ready</h3>
          <p className="text-xs max-w-md mx-auto text-slate-400 leading-relaxed">
            Click "Run Multi-Model Comparison" to execute Logistic Regression, Decision Tree, Random Forest, XGBoost, and LightGBM in parallel.
          </p>
        </div>
      )}
    </div>
  );
}
