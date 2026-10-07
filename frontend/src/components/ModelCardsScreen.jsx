import React, { useState, useEffect } from 'react';
import { BookOpen, ShieldCheck, Database, Award, AlertCircle } from 'lucide-react';

export default function ModelCardsScreen() {
  const [selectedDisease, setSelectedDisease] = useState('diabetes');
  const [cardData, setCardData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchModelCard(selectedDisease);
  }, [selectedDisease]);

  const fetchModelCard = async (disease) => {
    setLoading(true);
    try {
      const resp = await fetch(`http://localhost:8000/models/${disease}/model-card`);
      const data = await resp.json();
      setCardData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h2 className="text-2xl font-extrabold gradient-text-cyan tracking-tight">Novel Feature #7: Mitchell et al. Model Cards</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Transparent model cards documenting dataset provenance, features, evaluation metrics, intended use, and limitations.
        </p>
      </div>

      <div className="glass-card p-6 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-4 border border-slate-800">
        <div className="flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-cyan-400" />
          <div>
            <h3 className="text-base font-semibold text-slate-200">Select Production Model Card</h3>
            <p className="text-xs text-slate-400">Endpoint: GET /models/{"{disease}"}/model-card</p>
          </div>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto">
          {['diabetes', 'heart_disease', 'breast_cancer', 'lung_cancer', 'stroke'].map((d) => (
            <button
              key={d}
              onClick={() => setSelectedDisease(d)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold capitalize transition-all ${
                selectedDisease === d ? 'bg-gradient-to-r from-cyan-500 to-indigo-600 text-slate-950 font-bold shadow-md shadow-cyan-500/20' : 'bg-slate-900 text-slate-400 hover:text-slate-200'
              }`}
            >
              {d.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="py-12 text-center text-cyan-400 font-medium flex items-center justify-center gap-3 glass-card rounded-3xl">
          <div className="w-5 h-5 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
          Loading model card...
        </div>
      ) : (
        cardData && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column: Details & Use */}
            <div className="space-y-6">
              <div className="glass-card p-6 rounded-3xl space-y-4 border border-slate-800">
                <div className="flex items-center gap-2 text-cyan-400">
                  <Award className="w-5 h-5" />
                  <h4 className="font-bold text-slate-200 text-sm">Model Overview</h4>
                </div>

                <div className="space-y-2 text-xs text-slate-300">
                  <div>Model Name: <strong className="text-cyan-400">{cardData.model_details.model_name}</strong></div>
                  <div>Architecture: <strong className="text-slate-100">{cardData.model_details.architecture}</strong></div>
                  <div>Version: <span className="text-slate-400">{cardData.model_details.version}</span></div>
                  <div>Release Date: <span className="text-slate-400">{cardData.model_details.release_date}</span></div>
                  <div>License: <span className="text-slate-400">{cardData.model_details.license}</span></div>
                </div>
              </div>

              <div className="glass-card p-6 rounded-3xl space-y-4 border border-slate-800">
                <div className="flex items-center gap-2 text-emerald-400">
                  <ShieldCheck className="w-5 h-5" />
                  <h4 className="font-bold text-slate-200 text-sm">Intended Use & Scope</h4>
                </div>

                <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
                  <div>
                    <strong className="text-emerald-400">Primary Intended Use:</strong>
                    <p className="text-slate-400 mt-0.5">{cardData.intended_use.primary_intended_use}</p>
                  </div>

                  <div>
                    <strong className="text-red-400">Out of Scope Use:</strong>
                    <p className="text-slate-400 mt-0.5">{cardData.intended_use.out_of_scope_use}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Middle & Right Column: Data & Metrics */}
            <div className="lg:col-span-2 space-y-6">
              <div className="glass-card p-6 rounded-3xl space-y-4 border border-slate-800">
                <div className="flex items-center gap-2 text-indigo-400">
                  <Database className="w-5 h-5" />
                  <h4 className="font-bold text-slate-200 text-sm">Dataset Provenance & Metrics</h4>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-2xl bg-slate-950/80 text-center border border-slate-800/80">
                  <div>
                    <div className="text-xs text-slate-400">ROC-AUC</div>
                    <div className="text-xl font-extrabold text-cyan-400 mt-1">{cardData.evaluation_results.roc_auc}</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400">Recall / Sensitivity</div>
                    <div className="text-xl font-extrabold text-emerald-400 mt-1">{cardData.evaluation_results.recall_sensitivity}</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400">F1 Score</div>
                    <div className="text-xl font-extrabold text-indigo-400 mt-1">{cardData.evaluation_results.f1_score}</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400">Brier Score</div>
                    <div className="text-xl font-extrabold text-amber-400 mt-1">{cardData.evaluation_results.calibrated_brier_score}</div>
                  </div>
                </div>

                <div className="space-y-2 text-xs text-slate-300 pt-2">
                  <div>Dataset Name: <strong>{cardData.data.dataset_name}</strong></div>
                  <div>Source: <span className="text-slate-400">{cardData.data.source}</span></div>
                  <div>Sample Count: <span>{cardData.data.total_records} (Train: {cardData.data.training_samples}, Test: {cardData.data.test_samples})</span></div>
                </div>
              </div>

              {/* Known Limitations */}
              <div className="glass-card p-6 rounded-3xl space-y-3 border-l-4 border-l-amber-500 border-slate-800">
                <div className="flex items-center gap-2 text-amber-400">
                  <AlertCircle className="w-5 h-5" />
                  <h4 className="font-bold text-slate-200 text-sm">Known Limitations & Bias Notes</h4>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {cardData.data.known_limitations}
                </p>
              </div>
            </div>
          </div>
        )
      )}
    </div>
  );
}
