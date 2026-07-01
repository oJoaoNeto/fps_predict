import { useState, useEffect } from 'react';
import { Crosshair, AlertCircle, Sparkles } from 'lucide-react';
import { getComponents, predictFps } from '../services/api';
import type {
  HardwareComponent,
  PredictFpsResponse,
  Resolution,
  QualityPreset,
} from '../types/api';
import FpsCounter from '../components/FpsCounter';
import ComponentCard from '../components/ComponentCard';
import LoadingSpinner from '../components/LoadingSpinner';

const RESOLUTIONS: Resolution[] = ['1080p', '1440p', '4K'];
const QUALITIES: QualityPreset[] = ['Low', 'Medium', 'High', 'Ultra'];
const RAM_OPTIONS = [4, 8, 16, 32, 64];

export default function PredictView() {
  // Data
  const [cpus, setCpus] = useState<HardwareComponent[]>([]);
  const [gpus, setGpus] = useState<HardwareComponent[]>([]);

  // Form
  const [cpuId, setCpuId] = useState<number>(0);
  const [gpuId, setGpuId] = useState<number>(0);
  const [ramGb, setRamGb] = useState<number>(16);
  const [resolution, setResolution] = useState<Resolution>('1080p');
  const [qualityPreset, setQualityPreset] = useState<QualityPreset>('Low');

  // State
  const [loading, setLoading] = useState(false);
  const [loadingComponents, setLoadingComponents] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictFpsResponse | null>(null);

  useEffect(() => {
    async function fetchComponents() {
      try {
        const [cpuList, gpuList] = await Promise.all([
          getComponents('CPU'),
          getComponents('GPU'),
        ]);
        setCpus(cpuList);
        setGpus(gpuList);
        if (cpuList.length > 0) setCpuId(cpuList[0].id);
        if (gpuList.length > 0) setGpuId(gpuList[0].id);
      } catch {
        setError('Não foi possível carregar os componentes. Verifique se o backend está rodando.');
      } finally {
        setLoadingComponents(false);
      }
    }
    fetchComponents();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cpuId || !gpuId) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictFps({
        game_id: 1,
        cpu_id: cpuId,
        gpu_id: gpuId,
        ram_gb: ramGb,
        resolution,
        quality_preset: qualityPreset,
      });
      setResult(data);
    } catch (err: unknown) {
      const msg =
        err && typeof err === 'object' && 'response' in err
          ? (err as { response: { data: { error?: string } } }).response?.data?.error
          : undefined;
      setError(msg || 'Erro ao realizar a predição. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  if (loadingComponents) {
    return <LoadingSpinner text="Carregando componentes do backend..." />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero */}
      <div className="text-center mb-10 animate-slide-up">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-semibold mb-4">
          <Sparkles className="w-3 h-3" />
          Powered by Gradient Boosting
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
          Simule a <span className="gradient-text">Performance</span>
        </h2>
        <p className="text-text-secondary mt-2 max-w-lg mx-auto text-sm">
          Selecione o hardware desejado e descubra quantos FPS você terá no CS:GO / CS2 utilizando nosso modelo de Machine Learning.
        </p>
      </div>

      <div className="grid lg:grid-cols-5 gap-8">
        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-2 card-glass p-6 space-y-5 h-fit"
        >
          <h3 className="text-sm font-bold uppercase tracking-widest text-text-muted flex items-center gap-2">
            <Crosshair className="w-4 h-4 text-accent" />
            Configuração
          </h3>

          {/* CPU */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Processador (CPU)
            </label>
            <select
              value={cpuId}
              onChange={(e) => setCpuId(Number(e.target.value))}
              className="w-full px-3 py-2.5 rounded-xl bg-bg-input border border-border-default text-text-primary text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-all appearance-none cursor-pointer"
            >
              {cpus.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} — R$ {parseFloat(c.price).toLocaleString('pt-BR')}
                </option>
              ))}
            </select>
          </div>

          {/* GPU */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Placa de Vídeo (GPU)
            </label>
            <select
              value={gpuId}
              onChange={(e) => setGpuId(Number(e.target.value))}
              className="w-full px-3 py-2.5 rounded-xl bg-bg-input border border-border-default text-text-primary text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-all appearance-none cursor-pointer"
            >
              {gpus.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.name} — R$ {parseFloat(g.price).toLocaleString('pt-BR')}
                </option>
              ))}
            </select>
          </div>

          {/* RAM */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Memória RAM
            </label>
            <div className="flex gap-2">
              {RAM_OPTIONS.map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRamGb(r)}
                  className={`flex-1 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    ramGb === r
                      ? 'bg-accent text-white shadow-md shadow-accent-glow'
                      : 'bg-bg-input border border-border-default text-text-secondary hover:border-accent/40'
                  }`}
                >
                  {r}GB
                </button>
              ))}
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
                      ? 'bg-accent text-white shadow-md shadow-accent-glow'
                      : 'bg-bg-input border border-border-default text-text-secondary hover:border-accent/40'
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
                      ? 'bg-accent text-white shadow-md shadow-accent-glow'
                      : 'bg-bg-input border border-border-default text-text-secondary hover:border-accent/40'
                  }`}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading || !cpuId || !gpuId}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-accent to-neon-purple text-white font-bold text-sm uppercase tracking-wider transition-all hover:shadow-lg hover:shadow-accent-glow disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? 'Calculando...' : 'Prever FPS'}
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

          {loading && <LoadingSpinner text="Calculando FPS via modelo de IA..." />}

          {result && !loading && (
            <div className="space-y-6 animate-slide-up">
              {/* FPS Display */}
              <div className="card-glass p-8 flex flex-col items-center animate-pulse-glow">
                <FpsCounter value={result.predicted_fps} />
                <div className="mt-4 flex items-center gap-3 text-xs text-text-muted">
                  <span className="px-2 py-0.5 rounded bg-bg-primary border border-border-default">
                    {result.resolution}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-bg-primary border border-border-default">
                    {result.quality_preset}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-bg-primary border border-border-default">
                    {result.ram_gb}GB RAM
                  </span>
                </div>
              </div>

              {/* Components used */}
              <div className="grid sm:grid-cols-2 gap-4">
                {result.cpu_details && (
                  <ComponentCard component={result.cpu_details} highlight />
                )}
                {result.gpu_details && (
                  <ComponentCard component={result.gpu_details} highlight />
                )}
              </div>

              {/* Game info */}
              {result.game_details && (
                <div className="card-glass p-4 flex items-center gap-4">
                  {result.game_details.cover_image_url && (
                    <img
                      src={result.game_details.cover_image_url}
                      alt={result.game_details.name}
                      className="w-28 h-14 rounded-lg object-cover border border-border-default"
                    />
                  )}
                  <div>
                    <h4 className="text-sm font-bold text-text-primary">
                      {result.game_details.name}
                    </h4>
                    <p className="text-xs text-text-muted">{result.game_details.genre}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Empty state */}
          {!result && !loading && !error && (
            <div className="card-glass p-12 flex flex-col items-center gap-4 text-center">
              <div className="w-16 h-16 rounded-2xl bg-accent/10 flex items-center justify-center animate-float">
                <Crosshair className="w-8 h-8 text-accent" />
              </div>
              <h3 className="text-lg font-bold text-text-primary">
                Pronto para simular
              </h3>
              <p className="text-sm text-text-secondary max-w-sm">
                Configure o hardware desejado no painel ao lado e clique em{' '}
                <strong className="text-accent">Prever FPS</strong> para obter a
                estimativa de performance via Machine Learning.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
