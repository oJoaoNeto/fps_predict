import { Cpu, Crosshair } from 'lucide-react';

interface HeaderProps {
  activeTab: 'predict' | 'optimize';
  onTabChange: (tab: 'predict' | 'optimize') => void;
}

export default function Header({ activeTab, onTabChange }: HeaderProps) {
  return (
    <header className="relative border-b border-border-default bg-bg-secondary/80 backdrop-blur-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-neon-purple flex items-center justify-center shadow-lg shadow-accent-glow">
                <Crosshair className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -inset-1 rounded-xl bg-gradient-to-br from-accent to-neon-purple opacity-30 blur-md -z-10" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-text-primary">
                FPS <span className="gradient-text">Predict</span>
              </h1>
              <p className="text-[10px] text-text-muted uppercase tracking-widest">
                Machine Learning
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 bg-bg-primary/50 rounded-xl p-1 border border-border-default">
            <button
              onClick={() => onTabChange('predict')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 cursor-pointer ${
                activeTab === 'predict'
                  ? 'bg-accent text-white shadow-lg shadow-accent-glow'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-card'
              }`}
            >
              <Crosshair className="w-4 h-4" />
              <span className="hidden sm:inline">Preditor de FPS</span>
              <span className="sm:hidden">FPS</span>
            </button>
            <button
              onClick={() => onTabChange('optimize')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 cursor-pointer ${
                activeTab === 'optimize'
                  ? 'bg-accent text-white shadow-lg shadow-accent-glow'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-card'
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span className="hidden sm:inline">Montar PC</span>
              <span className="sm:hidden">PC</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}
