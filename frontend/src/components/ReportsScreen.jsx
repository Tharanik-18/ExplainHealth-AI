import React, { useState } from 'react';
import { FileText, Download, Printer, RefreshCw } from 'lucide-react';

export default function ReportsScreen() {
  const [loading, setLoading] = useState(false);
  const [reportHtml, setReportHtml] = useState(null);

  const handleGenerateReport = async () => {
    setLoading(true);
    try {
      const resp = await fetch('http://localhost:8000/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ anonymized_id: 'demo_patient_01' })
      });
      const html = await resp.text();
      setReportHtml(html);
    } catch (err) {
      alert('Error generating clinical report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">Clinical Assessment Report Generator</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Generates downloadable, print-ready multi-disease clinical decision support reports.
        </p>
      </div>

      <div className="glass-card p-6 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-4 border border-slate-800">
        <div className="flex items-center gap-3">
          <FileText className="w-6 h-6 text-cyan-400" />
          <div>
            <h3 className="text-base font-semibold text-slate-200">Generate Patient Report</h3>
            <p className="text-xs text-slate-400">Anonymized Patient ID: demo_patient_01</p>
          </div>
        </div>

        <button
          onClick={handleGenerateReport}
          disabled={loading}
          className="px-6 py-3 rounded-2xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 font-bold text-slate-950 text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition-all shrink-0"
        >
          {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <FileText className="w-4 h-4" />}
          Generate Complete HTML/PDF Report
        </button>
      </div>

      {reportHtml ? (
        <div className="space-y-4">
          <div className="flex justify-end gap-2">
            <button
              onClick={() => {
                const win = window.open('', '_blank');
                win.document.write(reportHtml);
                win.document.close();
                win.print();
              }}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 border border-slate-700"
            >
              <Printer className="w-4 h-4" /> Print / Save PDF
            </button>
          </div>

          <div className="glass-card p-4 rounded-3xl border border-slate-800 overflow-hidden">
            <iframe
              srcDoc={reportHtml}
              title="Clinical Assessment Report"
              className="w-full h-[700px] border-0 rounded-2xl bg-white"
            />
          </div>
        </div>
      ) : (
        <div className="glass-card p-12 rounded-3xl border border-slate-800 text-center text-slate-400 space-y-3">
          <FileText className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-base font-semibold text-slate-300">Report Generator Ready</h3>
          <p className="text-xs max-w-md mx-auto">
            Click "Generate Complete HTML/PDF Report" to compile all multi-disease assessments, SHAP explanations, and model cards into a printable document.
          </p>
        </div>
      )}
    </div>
  );
}
