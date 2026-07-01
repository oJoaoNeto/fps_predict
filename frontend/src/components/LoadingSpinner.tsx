import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ text = 'Processando...' }: { text?: string }) {
  return (
    <div className="flex flex-col items-center gap-4 py-12 animate-fade-in" style={{ animation: 'fade-in 0.3s ease-out' }}>
      <div className="relative">
        <Loader2 className="w-10 h-10 text-accent animate-spin" />
        <div className="absolute inset-0 w-10 h-10 rounded-full bg-accent/20 blur-xl" />
      </div>
      <p className="text-sm text-text-secondary">{text}</p>
    </div>
  );
}
