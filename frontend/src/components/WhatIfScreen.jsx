import React, { useState } from 'react';
import { Sliders, RefreshCw, AlertTriangle, ArrowRight, CheckCircle2, Sparkles } from 'lucide-react';

export default function WhatIfScreen({ activeAssessment }) {
  const [disease, setDisease] = useState(activeAssessment?.disease || 'diabetes');
  const [params, setParams] = useState({
    glucose: 165,
    bmi: 31.0,
    blood_pressure: 85,
    age: 45,
    chol: 240,
    thalach: 150,
    smoking: 2
  });

  const [loading, setLoading] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const resp = await fetch(`http://localhost:8000/counterfactual/${disease}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_data: params })
      });
      const data = await resp.json();
      setSimulationResult(data);
    } catch (err) {
      alert('Error contacting counterfactual engine');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-widest mb-1">
            <Sliders className="w-4 h-4" /> Novel Feature #1: Counterfactual Engine
          </div>
          <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">
            "What Would Change the Prediction?"
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Mathematically searches for minimal input adjustments in actionable features (BMI, Glucose, BP) while holding non-actionable features (Age, Sex) constant.
          </p>
        </div>

        <button
          onClick={handleSimulate}
          disabled={loading}
          className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-500 via-sky-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 font-bold text-slate-950 text-xs sm:text-sm flex items-center justify-center gap-2 shadow-xl shadow-cyan-500/20 transition-all shrink-0"
        >
          {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sliders className="w-4 h-4" />}
          Simulate Mathematical Counterfactual
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Sliders Control Panel */}
        <div className="glass-card p-6 rounded-3xl space-y-6 border border-slate-800">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Actionable Sliders</h3>
            <select
              value={disease}
              onChange={(e) => setDisease(e.target.value)}
              className="bg-slate-900 text-xs text-slate-200 rounded-xl px-2.5 py-1.5 border border-slate-800"
            >
              <option value="diabetes">Diabetes</option>
              <option value="heart_disease">Heart Disease</option>
              <option value="breast_cancer">Breast Cancer</option>
              <option value="lung_cancer">Lung Cancer</option>
              <option value="stroke">Stroke</option>
            </select>
          </div>

          <div className="space-y-5">
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1.5">
                <span className="text-slate-400">Fasting Glucose:</span>
                <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
                  {params.glucose} mg/dL
                </span>
              </div>
              <input
                type="range"
                min="70"
                max="250"
                value={params.glucose}
                onChange={(e) => setParams({ ...params, glucose: Number(e.target.value) })}
                className="w-full accent-cyan-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>70 mg/dL (Normal)</span>
                <span>250 mg/dL (High)</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold mb-1.5">
                <span className="text-slate-400">Body Mass Index (BMI):</span>
                <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
                  {params.bmi} kg/m²
                </span>
              </div>
              <input
                type="range"
                min="18"
                max="45"
                step="0.5"
                value={params.bmi}
                onChange={(e) => setParams({ ...params, bmi: Number(e.target.value) })}
                className="w-full accent-cyan-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>18.5 (Normal)</span>
                <span>45.0 (Obese)</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold mb-1.5">
                <span className="text-slate-400">Diastolic Blood Pressure:</span>
                <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
                  {params.blood_pressure} mm Hg
                </span>
              </div>
              <input
                type="range"
                min="60"
                max="140"
                value={params.blood_pressure}
                onChange={(e) => setParams({ ...params, blood_pressure: Number(e.target.value) })}
                className="w-full accent-cyan-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>60 mm Hg</span>
                <span>140 mm Hg</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold mb-1.5">
                <span className="text-slate-400">Serum Cholesterol:</span>
                <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
                  {params.chol} mg/dL
                </span>
              </div>
              <input
                type="range"
                min="120"
                max="400"
                value={params.chol}
                onChange={(e) => setParams({ ...params, chol: Number(e.target.value) })}
                className="w-full accent-cyan-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>120 mg/dL</span>
                <span>400 mg/dL</span>
              </div>
            </div>
          </div>
        </div>

        {/* Counterfactual Scenarios Display */}
        <div className="lg:col-span-2 space-y-6">
          {simulationResult ? (
            <div className="space-y-6">
              
              {/* Top Risk Comparison KPI Banner */}
              <div className="glass-card p-6 rounded-3xl border border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-6 items-center">
                <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30">
                  <span className="text-[10px] text-amber-400 font-bold uppercase tracking-wider">Current Input Model Estimate</span>
                  <div className="text-3xl font-black text-amber-400 mt-1">
                    {(simulationResult.current_probability * 100).toFixed(1)}% Risk
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30">
                  <span className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider">Simulated Target Threshold</span>
                  <div className="text-3xl font-black text-emerald-400 mt-1">
                    &lt; {(simulationResult.target_threshold * 100).toFixed(1)}% Risk
                  </div>
                </div>
              </div>

              {/* Scenarios Cards */}
              {simulationResult.scenarios?.map((scen, idx) => (
                <div key={idx} className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <h4 className="font-bold text-slate-100 text-sm">{scen.scenario_name}</h4>
                    <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
                      Simulated Risk: {(scen.estimated_probability * 100).toFixed(1)}% (-{(scen.absolute_risk_reduction * 100).toFixed(1)}%)
                    </span>
                  </div>

                  <div className="space-y-3">
                    {scen.modified_features?.map((f, i) => (
                      <div key={i} className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-800 flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-200">{f.label}</span>
                        <div className="flex items-center gap-3 text-xs">
                          <span className="text-slate-400 line-through">{f.current_value} {f.unit}</span>
                          <ArrowRight className="w-4 h-4 text-cyan-400" />
                          <span className="text-emerald-400 font-bold bg-emerald-500/10 px-2.5 py-0.5 rounded-lg border border-emerald-500/30">
                            {f.scenario_value} {f.unit}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}

              <div className="p-4 rounded-2xl bg-slate-950/90 border border-cyan-500/30 text-xs text-slate-400 leading-relaxed flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
                <div>{simulationResult.disclaimer}</div>
              </div>
            </div>
          ) : (
            <div className="glass-card p-12 rounded-3xl text-center text-slate-400 space-y-4 border border-slate-800">
              <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mx-auto">
                <Sliders className="w-7 h-7" />
              </div>
              <h3 className="text-base font-bold text-slate-200">Counterfactual Simulation Ready</h3>
              <p className="text-xs max-w-md mx-auto text-slate-400 leading-relaxed">
                Adjust any actionable slider on the left panel and click "Simulate Mathematical Counterfactual" to calculate how feature perturbations alter the model risk estimate.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
