import { useState } from 'react';
import {
  Cpu,
  AlertCircle,
  Sparkles,
  DollarSign,
  TrendingUp,
  PieChart,
} from 'lucide-react';
import { optimizeBuild } from '../services/api';
import type {
  OptimizeBuildResponse,
  Resolution,
  QualityPreset,
  Priority,
} from '../types/api';
import FpsCounter from '../components/FpsCounter';
import ComponentCard from '../components/ComponentCard';
import LoadingSpinner from '../components/LoadingSpinner';

const RESOLUTIONS: Resolution[] = ['1080p', '1440p', '4K'];
const QUALITIES: QualityPreset[] = ['Low', 'Medium', 'High', 'Ultra'];
const PRIORITIES: { value: Priority; label: string; desc: string }[] = [
  { value: 'cost-benefit', label: 'Custo-Benefício', desc: 'Melhor valor pelo dinheiro' },
  { value: 'balance', label: 'Equilibrado', desc: 'Balanceado entre custo e desempenho' },
  { value: 'performance', label: 'Performance', desc: 'Máximo desempenho possível' },
];

export default function OptimizeView() {
  // Form
  const [budget, setBudget] = useState<number>(5000);
  const [resolution, setResolution] = useState<Resolution>('1080p');
  const [qualityPreset, setQualityPreset] = useState<QualityPreset>('Medium');
  const [priority, setPriority] = useState<Priority>('balance');

  // State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<OptimizeBuildResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await optimizeBuild({
        budget,
        resolution,
        quality_preset: qualityPreset,
        priority,
      });
      setResult(data);
    } catch (err: unknown) {
      const msg =
        err && typeof err === 'object' && 'response' in err
          ? (err as { response: { data: { error?: string } } }).response?.data?.error
          : undefined;
      setError(msg || 'Erro ao otimizar a build. Verifique se o backend está rodando.');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (val: string | number) =>
    parseFloat(String(val)).toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero */}
      <div className="text-center mb-10 animate-slide-up">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-neon-cyan/10 border border-neon-cyan/20 text-neon-cyan text-xs font-semibold mb-4">
          <Sparkles className="w-3 h-3" />
          Otimizador Inteligente
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
          Monte o <span className="gradient-text">PC Ideal</span>
        </h2>
        <p className="text-text-secondary mt-2 max-w-lg mx-auto text-sm">
          Informe seu orçamento e preferências. Nossa IA encontrará a melhor combinação de peças compatíveis, maximizando o FPS dentro do seu limite.
        </p>
      </div>

      <div className="grid lg:grid-cols-5 gap-8">
        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-2 card-glass p-6 space-y-5 h-fit"
        >
          <h3 className="text-sm font-bold uppercase tracking-widest text-text-muted flex items-center gap-2">
            <Cpu className="w-4 h-4 text-neon-cyan" />
            Parâmetros
          </h3>

          {/* Budget */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Orçamento Máximo
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted text-sm">
                R$
              </span>
              <input
                type="number"
                min={1000}
                step={100}
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full pl-10 pr-3 py-2.5 rounded-xl bg-bg-input border border-border-default text-text-primary text-sm focus:outline-none focus:border-neon-cyan focus:ring-1 focus:ring-neon-cyan/30 transition-all"
              />
            </div>
            <input
              type="range"
              min={1000}
              max={20000}
              step={500}
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full accent-neon-cyan cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-text-muted">
              <span>R$ 1.000</span>
              <span>R$ 20.000</span>
            </div>
          </div>

          {/* Resolution */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Resolução
            </label>
            <div className="flex gap-2">
              {RESOLUTIONS.map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setResolution(r)}
                  className={`flex-1 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    resolution === r
                      ? 'bg-neon-cyan text-bg-primary shadow-md shadow-neon-cyan/30'
                      : 'bg-bg-input border border-border-default text-text-secondary hover:border-neon-cyan/40'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {/* Quality */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Qualidade Gráfica
            </label>
            <div className="grid grid-cols-4 gap-2">
              {QUALITIES.map((q) => (
                <button
                  key={q}
                  type="button"
                  onClick={() => setQualityPreset(q)}
                  className={`py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    qualityPreset === q
                      ? 'bg-neon-cyan text-bg-primary shadow-md shadow-neon-cyan/30'
                      : 'bg-bg-input border border-border-default text-text-secondary hover:border-neon-cyan/40'
                  }`}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Priority */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Prioridade
            </label>
            <div className="space-y-2">
              {PRIORITIES.map((p) => (
                <button
                  key={p.value}
                  type="button"
                  onClick={() => setPriority(p.value)}
                  className={`w-full text-left px-4 py-3 rounded-xl transition-all cursor-pointer ${
                    priority === p.value
                      ? 'bg-neon-cyan/10 border border-neon-cyan/40 text-neon-cyan'
                      : 'bg-bg-input border border-border-default text-text-secondary hover:border-neon-cyan/20'
                  }`}
                >
                  <span className="text-xs font-bold">{p.label}</span>
                  <p className="text-[10px] mt-0.5 opacity-70">{p.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-neon-cyan to-accent text-white font-bold text-sm uppercase tracking-wider transition-all hover:shadow-lg hover:shadow-neon-cyan/30 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? 'Otimizando...' : 'Montar PC Ideal'}
          </button>
        </form>

        {/* Results */}
        <div className="lg:col-span-3 space-y-6">
          {error && (
            <div className="card-glass p-4 border-danger/30 flex items-center gap-3 animate-slide-up">
              <AlertCircle className="w-5 h-5 text-danger flex-shrink-0" />
              <p className="text-sm text-danger">{error}</p>
            </div>
          )}

          {loading && <LoadingSpinner text="Otimizando a melhor build com IA..." />}

          {result && !loading && (
            <div className="space-y-6 animate-slide-up">
              {/* Stats row */}
              <div className="grid grid-cols-3 gap-4">
                <div className="card-glass p-4 flex flex-col items-center text-center">
                  <DollarSign className="w-5 h-5 text-success mb-1" />
                  <span className="text-xs text-text-muted uppercase tracking-wider">
                    Custo Total
                  </span>
                  <span className="text-lg font-bold text-success mt-1">
                    {formatCurrency(result.total_cost)}
                  </span>
                </div>
                <div className="card-glass p-4 flex flex-col items-center text-center">
                  <PieChart className="w-5 h-5 text-info mb-1" />
                  <span className="text-xs text-text-muted uppercase tracking-wider">
                    Orçamento Usado
                  </span>
                  <span className="text-lg font-bold text-info mt-1">
                    {result.budget_utilization_percent.toFixed(1)}%
                  </span>
                </div>
                <div className="card-glass p-4 flex flex-col items-center text-center">
                  <TrendingUp className="w-5 h-5 text-accent mb-1" />
                  <span className="text-xs text-text-muted uppercase tracking-wider">
                    Prioridade
                  </span>
                  <span className="text-lg font-bold text-accent mt-1 capitalize">
                    {PRIORITIES.find((p) => p.value === result.priority_applied)?.label ||
                      result.priority_applied}
                  </span>
                </div>
              </div>

              {/* FPS Display */}
              <div className="card-glass p-8 flex flex-col items-center animate-pulse-glow">
                <FpsCounter value={result.fps_predicted} label="FPS Estimado da Build" />
                <div className="mt-4 flex items-center gap-3 text-xs text-text-muted">
                  <span className="px-2 py-0.5 rounded bg-bg-primary border border-border-default">
                    {result.settings.resolution}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-bg-primary border border-border-default">
                    {result.settings.quality_preset}
                  </span>
                </div>
              </div>

              {/* Components Grid */}
              <div>
                <h3 className="text-sm font-bold uppercase tracking-widest text-text-muted mb-4">
                  Peças Recomendadas
                </h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  <ComponentCard component={result.cpu} highlight />
                  <ComponentCard component={result.gpu} highlight />
                  <ComponentCard component={result.motherboard} />
                  <ComponentCard component={result.ram} />
                  <ComponentCard component={result.psu} />
                  <ComponentCard component={result.storage} />
                </div>
              </div>

              {/* Budget bar */}
              <div className="card-glass p-4">
                <div className="flex items-center justify-between text-xs text-text-secondary mb-2">
                  <span>Utilização do Orçamento</span>
                  <span>
                    {formatCurrency(result.total_cost)} / {formatCurrency(budget)}
                  </span>
                </div>
                <div className="h-3 rounded-full bg-bg-primary overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-neon-cyan to-accent transition-all duration-1000"
                    style={{ width: `${Math.min(result.budget_utilization_percent, 100)}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Empty state */}
          {!result && !loading && !error && (
            <div className="card-glass p-12 flex flex-col items-center gap-4 text-center">
              <div className="w-16 h-16 rounded-2xl bg-neon-cyan/10 flex items-center justify-center animate-float">
                <Cpu className="w-8 h-8 text-neon-cyan" />
              </div>
              <h3 className="text-lg font-bold text-text-primary">
                Monte seu setup ideal
              </h3>
              <p className="text-sm text-text-secondary max-w-sm">
                Defina seu orçamento e preferências no painel ao lado. A IA
                encontrará a configuração com o melhor custo-benefício, garantindo
                compatibilidade entre todas as peças.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
