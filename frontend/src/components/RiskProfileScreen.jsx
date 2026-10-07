import React, { useState } from 'react';
import { Activity, ShieldAlert, Heart, Activity as LungIcon, Brain, CheckCircle, RefreshCw, User, SlidersHorizontal } from 'lucide-react';

export default function RiskProfileScreen() {
  const [formData, setFormData] = useState({
    age: 55,
    glucose: 145,
    bmi: 29.5,
    blood_pressure: 130,
    chol: 230,
    thalach: 145,
    smoking: 2,
    hypertension: 1,
    mean_radius: 14.1,
    mean_texture: 19.3,
    mean_perimeter: 92.0,
    mean_area: 654.0,
    mean_concavity: 0.088
  });

  const [loading, setLoading] = useState(false);
  const [profileResult, setProfileResult] = useState(null);

  const handleRunAllModels = async () => {
    setLoading(true);
    try {
      const resp = await fetch('http://localhost:8000/health-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_data: formData,
          anonymized_id: 'demo_patient_01'
        })
      });
      const data = await resp.json();
      setProfileResult(data);
    } catch (err) {
      alert('Error connecting to ExplainHealth API');
    } finally {
      setLoading(false);
    }
  };

  const diseaseIcons = {
    diabetes: Activity,
    heart_disease: Heart,
    breast_cancer: ShieldAlert,
    lung_cancer: LungIcon,
    stroke: Brain
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-widest mb-1">
            <SlidersHorizontal className="w-4 h-4" /> Multi-Disease Parallel Architecture
          </div>
          <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">
            Comprehensive Patient Health Risk Profile
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Evaluates 5 independent disease models in parallel on a single unified patient parameter form. Probabilities are strictly kept separate and uncombined.
          </p>
        </div>

        <button
          onClick={handleRunAllModels}
          disabled={loading}
          className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-500 via-sky-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 font-bold text-slate-950 text-xs sm:text-sm flex items-center justify-center gap-2 shadow-xl shadow-cyan-500/20 transition-all shrink-0"
        >
          {loading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" /> Evaluating 5 Disease Models...
            </>
          ) : (
            <>
              <CheckCircle className="w-4 h-4" /> Run Independent Multi-Disease Assessment
            </>
          )}
        </button>
      </div>

      {/* Unified Input Controls Grid */}
      <div className="glass-card p-6 rounded-3xl space-y-5 border border-slate-800">
        <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2 border-b border-slate-800 pb-3">
          <User className="w-4 h-4 text-cyan-400" /> Patient Clinical Measurement Inputs
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-400">Age (years)</label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500 font-sans"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Blood Glucose (mg/dL)</label>
            <input
              type="number"
              value={formData.glucose}
              onChange={(e) => setFormData({ ...formData, glucose: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500 font-sans"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Body Mass Index (BMI)</label>
            <input
              type="number"
              step="0.1"
              value={formData.bmi}
              onChange={(e) => setFormData({ ...formData, bmi: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500 font-sans"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Resting BP (mm Hg)</label>
            <input
              type="number"
              value={formData.blood_pressure}
              onChange={(e) => setFormData({ ...formData, blood_pressure: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500 font-sans"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Serum Cholesterol (mg/dL)</label>
            <input
              type="number"
              value={formData.chol}
              onChange={(e) => setFormData({ ...formData, chol: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500 font-sans"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Max Heart Rate (bpm)</label>
            <input
              type="number"
              value={formData.thalach}
              onChange={(e) => setFormData({ ...formData, thalach: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500 font-sans"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Tobacco Smoking Habit</label>
            <select
              value={formData.smoking}
              onChange={(e) => setFormData({ ...formData, smoking: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500"
            >
              <option value={1}>Non-smoker / No</option>
              <option value={2}>Smoker / Yes</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400">Chronic Hypertension</label>
            <select
              value={formData.hypertension}
              onChange={(e) => setFormData({ ...formData, hypertension: Number(e.target.value) })}
              className="w-full mt-1 bg-slate-900 text-slate-100 rounded-xl px-3 py-2.5 text-xs sm:text-sm border border-slate-800 focus:outline-none focus:border-cyan-500"
            >
              <option value={0}>No (Normal BP)</option>
              <option value={1}>Yes (Chronic BP)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Disease Results Grid */}
      {profileResult && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(profileResult.disease_modules).map(([dKey, res]) => {
            const Icon = diseaseIcons[dKey] || Activity;
            if (!res.success) return null;

            return (
              <div
                key={dKey}
                className="glass-card glass-card-hover p-6 rounded-3xl border border-slate-800/80 flex flex-col justify-between space-y-4"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shrink-0">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-100 text-sm">{res.display_name}</h4>
                      <p className="text-[11px] text-slate-500">Machine Learning Estimate</p>
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800/80 flex items-center justify-between">
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-400">Risk Score</div>
                    <div className="text-2xl font-black text-white">{res.percentage}</div>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-bold ${
                      res.severity === 'elevated'
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : res.severity === 'moderate'
                        ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    }`}
                  >
                    {res.risk_tier}
                  </span>
                </div>

                {/* Top Contributor */}
                {res.shap_explanation?.why_factors_increasing_risk?.length > 0 && (
                  <div className="pt-2 text-xs text-slate-300 border-t border-slate-800/80">
                    <span className="text-amber-400 font-semibold">Top Risk Factor: </span>
                    {res.shap_explanation.why_factors_increasing_risk[0].label} (+{res.shap_explanation.why_factors_increasing_risk[0].shap_value.toFixed(2)})
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
