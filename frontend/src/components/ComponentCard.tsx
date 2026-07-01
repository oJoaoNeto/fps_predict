import type { HardwareComponent } from '../types/api';
import { ExternalLink, Cpu, MonitorSpeaker, CircuitBoard, MemoryStick, Zap, HardDrive } from 'lucide-react';

interface ComponentCardProps {
  component: HardwareComponent;
  highlight?: boolean;
}

const categoryIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  CPU: Cpu,
  GPU: MonitorSpeaker,
  MOBO: CircuitBoard,
  RAM: MemoryStick,
  PSU: Zap,
  STORAGE: HardDrive,
};

const categoryLabels: Record<string, string> = {
  CPU: 'Processador',
  GPU: 'Placa de Vídeo',
  MOBO: 'Placa-Mãe',
  RAM: 'Memória RAM',
  PSU: 'Fonte',
  STORAGE: 'Armazenamento',
};

export default function ComponentCard({ component, highlight }: ComponentCardProps) {
  const Icon = categoryIcons[component.category] || Cpu;

  return (
    <div
      className={`card-glass p-4 ${
        highlight ? 'border-accent/50 shadow-lg shadow-accent-glow' : ''
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 min-w-0">
          <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-accent/10 border border-accent/20 flex items-center justify-center">
            <Icon className="w-5 h-5 text-accent" />
          </div>
          <div className="min-w-0">
            <span className="text-[10px] uppercase tracking-widest text-accent font-semibold">
              {categoryLabels[component.category] || component.category}
            </span>
            <h3 className="text-sm font-semibold text-text-primary truncate mt-0.5">
              {component.name}
            </h3>
          </div>
        </div>
        <div className="flex flex-col items-end flex-shrink-0">
          <span className="text-lg font-bold text-success">
            R$ {parseFloat(component.price).toLocaleString('pt-BR')}
          </span>
          {component.shop_link && (
            <a
              href={component.shop_link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] text-accent hover:text-accent-hover transition-colors mt-1"
            >
              <ExternalLink className="w-3 h-3" />
              Ver lojas
            </a>
          )}
        </div>
      </div>

      {/* Specs preview */}
      {component.specs && Object.keys(component.specs).length > 0 && (
        <div className="mt-3 pt-3 border-t border-border-default">
          <div className="flex flex-wrap gap-1.5">
            {Object.entries(component.specs).slice(0, 4).map(([key, val]) => (
              <span
                key={key}
                className="text-[10px] px-2 py-0.5 rounded-md bg-bg-primary/60 text-text-muted border border-border-default"
              >
                {key.replace(/([A-Z])/g, ' $1').trim()}: {val}
              </span>
            ))}
            {Object.keys(component.specs).length > 4 && (
              <span className="text-[10px] px-2 py-0.5 rounded-md bg-bg-primary/60 text-text-muted border border-border-default">
                +{Object.keys(component.specs).length - 4}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
