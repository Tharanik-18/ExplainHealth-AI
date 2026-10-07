import React, { useState } from 'react';
import Navbar from './components/Navbar';
import ChatScreen from './components/ChatScreen';
import RiskProfileScreen from './components/RiskProfileScreen';
import ExplainabilityScreen from './components/ExplainabilityScreen';
import WhatIfScreen from './components/WhatIfScreen';
import ModelComparisonScreen from './components/ModelComparisonScreen';
import HealthTimelineScreen from './components/HealthTimelineScreen';
import ModelCardsScreen from './components/ModelCardsScreen';
import ReportsScreen from './components/ReportsScreen';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [activeAssessment, setActiveAssessment] = useState(null);

  const handleNavigateToExplainability = (assessment) => {
    setActiveAssessment(assessment);
    setActiveTab('explainability');
  };

  const handleNavigateToWhatIf = (assessment) => {
    setActiveAssessment(assessment);
    setActiveTab('whatif');
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main 
        style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '2rem',
          minHeight: 'calc(100vh - 180px)',
          width: '100%',
          flex: 1
        }}
      >
        {activeTab === 'chat' && (
          <ChatScreen
            onNavigateToExplainability={handleNavigateToExplainability}
            onNavigateToWhatIf={handleNavigateToWhatIf}
          />
        )}
        {activeTab === 'profile' && <RiskProfileScreen />}
        {activeTab === 'explainability' && (
          <ExplainabilityScreen activeAssessment={activeAssessment} />
        )}
        {activeTab === 'whatif' && (
          <WhatIfScreen activeAssessment={activeAssessment} />
        )}
        {activeTab === 'disagreement' && <ModelComparisonScreen />}
        {activeTab === 'timeline' && <HealthTimelineScreen />}
        {activeTab === 'modelcards' && <ModelCardsScreen />}
        {activeTab === 'reports' && <ReportsScreen />}
      </main>

      <footer className="bg-[#131c2e] border-t border-[#1e293b] py-6 px-4 text-center text-xs text-slate-400">
        ExplainHealth AI © 2026 — Educational & Research Decision Support Prototype. Not for Direct Medical Diagnosis.
      </footer>
    </div>
  );
}
