import React, { useState, useEffect } from 'react';
import { TrendingUp, Calendar, RefreshCw, Activity } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function HealthTimelineScreen() {
  const [timelineData, setTimelineData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedDisease, setSelectedDisease] = useState('diabetes');

  useEffect(() => {
    fetchTimeline();
  }, []);

  const fetchTimeline = async () => {
    setLoading(true);
    try {
      const resp = await fetch('http://localhost:8000/health-profile/demo_patient_01');
      const data = await resp.json();
      setTimelineData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const diseaseRecords = timelineData?.disease_timelines?.[selectedDisease] || [];
  const chartData = diseaseRecords.map((r, i) => ({
    date: r.date,
    risk_percentage: Number((r.predicted_risk * 100).toFixed(1)),
    bmi: r.inputs?.bmi || 27.5,
    glucose: r.inputs?.glucose || 120
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-widest mb-1">
            <TrendingUp className="w-4 h-4" /> Novel Feature #5: Health Timeline
          </div>
          <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">
            Personal Model-Estimate Health Trends
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Tracks historical model-estimate variations across patient-entered measurement sessions over time.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <select
            value={selectedDisease}
            onChange={(e) => setSelectedDisease(e.target.value)}
            className="bg-slate-900 text-xs text-slate-200 font-semibold rounded-xl px-3 py-2 border border-slate-800"
          >
            <option value="diabetes">Diabetes Trend</option>
            <option value="heart_disease">Heart Disease Trend</option>
            <option value="breast_cancer">Breast Cancer Trend</option>
            <option value="lung_cancer">Lung Cancer Trend</option>
            <option value="stroke">Stroke Trend</option>
          </select>

          <button
            onClick={fetchTimeline}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {chartData.length > 0 ? (
        <div className="space-y-6">
          
          {/* Line Chart Card */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h4 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
              Model-Estimated Risk Trend (% Probability over Time)
            </h4>

            <div className="h-80 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="date" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#94a3b8" domain={[0, 100]} unit="%" />
                  <Tooltip
                    content={({ payload }) => {
                      if (!payload || !payload.length) return null;
                      const d = payload[0].payload;
                      return (
                        <div className="p-3 bg-slate-900 border border-slate-700 rounded-xl text-xs space-y-1 shadow-2xl">
                          <div className="font-bold text-slate-200">{d.date}</div>
                          <div>Model Risk Estimate: <strong className="text-cyan-400">{d.risk_percentage}%</strong></div>
                          <div>Glucose: <strong className="text-slate-300">{d.glucose} mg/dL</strong></div>
                          <div>BMI: <strong className="text-slate-300">{d.bmi}</strong></div>
                        </div>
                      );
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="risk_percentage"
                    stroke="#38bdf8"
                    strokeWidth={3}
                    dot={{ fill: '#38bdf8', r: 5 }}
                    activeDot={{ r: 8 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Table */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h4 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Measurement History Records</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="pb-3 font-semibold">Measurement Date</th>
                    <th className="pb-3 font-semibold">Model Estimated Risk</th>
                    <th className="pb-3 font-semibold">Category</th>
                    <th className="pb-3 font-semibold">Input Values</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {diseaseRecords.map((r) => (
                    <tr key={r.id} className="hover:bg-slate-800/40">
                      <td className="py-3.5 text-slate-300 font-mono">{r.date}</td>
                      <td className="py-3.5 font-bold text-cyan-400 font-mono text-sm">{r.percentage}</td>
                      <td className="py-3.5">
                        <span className="px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 text-xs font-semibold">
                          {r.risk_tier}
                        </span>
                      </td>
                      <td className="py-3.5 text-slate-400 max-w-xs truncate font-mono">
                        {JSON.stringify(r.inputs)}
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
            <Calendar className="w-7 h-7" />
          </div>
          <h3 className="text-base font-bold text-slate-200">No Assessment History Recorded</h3>
          <p className="text-xs max-w-md mx-auto text-slate-400 leading-relaxed">
            Perform an analysis in the Chatbot or Risk Profile screen to begin recording model-estimate health trends.
          </p>
        </div>
      )}
    </div>
  );
}
