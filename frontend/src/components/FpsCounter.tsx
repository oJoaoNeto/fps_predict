import { useEffect, useRef, useState } from 'react';

interface FpsCounterProps {
  value: number;
  label?: string;
}

export default function FpsCounter({ value, label = 'FPS Previsto' }: FpsCounterProps) {
  const [displayValue, setDisplayValue] = useState(0);
  const animationRef = useRef<number>();

  useEffect(() => {
    const start = 0;
    const end = value;
    const duration = 1200;
    const startTime = performance.now();

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplayValue(Math.round(start + (end - start) * eased));

      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate);
      }
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [value]);

  const getPerformanceColor = () => {
    if (value >= 200) return 'from-neon-green to-neon-cyan';
    if (value >= 120) return 'from-neon-cyan to-accent';
    if (value >= 60) return 'from-warning to-neon-cyan';
    return 'from-danger to-warning';
  };

  const getPerformanceLabel = () => {
    if (value >= 200) return 'Excelente';
    if (value >= 120) return 'Ótimo';
    if (value >= 60) return 'Bom';
    if (value >= 30) return 'Jogável';
    return 'Baixo';
  };

  return (
    <div className="relative flex flex-col items-center animate-slide-up">
      <div className="relative">
        <div className={`text-7xl sm:text-8xl font-black fps-counter bg-gradient-to-r ${getPerformanceColor()} bg-clip-text text-transparent`}>
          {displayValue}
        </div>
        <div className="absolute -inset-4 bg-gradient-to-r from-accent/10 to-neon-cyan/10 blur-3xl rounded-full -z-10" />
      </div>
      <span className="text-lg font-semibold text-text-secondary mt-1">{label}</span>
      <span className={`mt-2 px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-gradient-to-r ${getPerformanceColor()} text-bg-primary`}>
        {getPerformanceLabel()}
      </span>
    </div>
  );
}
