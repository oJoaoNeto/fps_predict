import { useState } from 'react';
import Header from './components/Header';
import PredictView from './views/PredictView';
import OptimizeView from './views/OptimizeView';

function App() {
  const [activeTab, setActiveTab] = useState<'predict' | 'optimize'>('predict');

  return (
    <div className="min-h-screen bg-bg-primary bg-grid">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="relative">
        {activeTab === 'predict' ? <PredictView /> : <OptimizeView />}
      </main>

      {/* Footer */}
      <footer className="border-t border-border-default py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p className="text-xs text-text-muted">
            FPS Predict — Projeto de Aprendizado de Máquina
          </p>
          <p className="text-xs text-text-muted">
            Modelo: Gradient Boosting Regressor · Scikit-Learn
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
