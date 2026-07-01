// ─── Hardware Component ───────────────────────────────────────────────
export interface HardwareComponent {
  id: number;
  name: string;
  category: 'CPU' | 'GPU' | 'RAM' | 'MOBO' | 'PSU' | 'STORAGE';
  price: string;
  shop_link: string | null;
  specs: Record<string, number | string>;
  is_active: boolean;
}

// ─── Game ─────────────────────────────────────────────────────────────
export interface Game {
  id: number;
  name: string;
  steam_id: string | null;
  cover_image_url: string | null;
  genre: string | null;
  min_requirements: Record<string, string>;
  rec_requirements: Record<string, string>;
}

// ─── Predict FPS ──────────────────────────────────────────────────────
export type Resolution = '1080p' | '1440p' | '4K';
export type QualityPreset = 'Low' | 'Medium' | 'High' | 'Ultra';
export type Priority = 'cost-benefit' | 'performance' | 'balance';

export interface PredictFpsRequest {
  game_id: number;
  cpu_id: number;
  gpu_id: number;
  ram_gb: number;
  resolution: Resolution;
  quality_preset: QualityPreset;
}

export interface PredictFpsResponse {
  id: number;
  game: number;
  cpu: number;
  gpu: number;
  ram_gb: number;
  resolution: string;
  quality_preset: string;
  predicted_fps: number;
  created_at: string;
  game_details: Game;
  cpu_details: HardwareComponent;
  gpu_details: HardwareComponent;
}

// ─── Optimize Build ───────────────────────────────────────────────────
export interface OptimizeBuildRequest {
  budget: number;
  resolution: Resolution;
  quality_preset: QualityPreset;
  priority: Priority;
}

export interface OptimizeBuildResponse {
  cpu: HardwareComponent;
  gpu: HardwareComponent;
  motherboard: HardwareComponent;
  ram: HardwareComponent;
  psu: HardwareComponent;
  storage: HardwareComponent;
  total_cost: string;
  fps_predicted: number;
  budget_utilization_percent: number;
  priority_applied: string;
  settings: {
    resolution: string;
    quality_preset: string;
  };
}
