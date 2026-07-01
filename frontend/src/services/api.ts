import axios from 'axios';
import type {
  HardwareComponent,
  Game,
  PredictFpsRequest,
  PredictFpsResponse,
  OptimizeBuildRequest,
  OptimizeBuildResponse,
} from '../types/api';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

// ─── Components ──────────────────────────────────────────────────────
export async function getComponents(category?: string): Promise<HardwareComponent[]> {
  const params = category ? { category } : {};
  const { data } = await api.get('/components/', { params });
  return data;
}

// ─── Games (uses the DRF default router — predictions list includes game info,
//     but there's no standalone /games/ endpoint, so we extract from components
//     or use a small helper) ──────────────────────────────────────────────
// The backend seeds only one game (CS:GO). We'll fetch from predictions or hard-code the ID.
// Since /api/predictions/ exists as a ReadOnlyModelViewSet, let's use that if available.
export async function getGames(): Promise<Game[]> {
  // There is no dedicated games endpoint in the router, but the game data comes
  // embedded in prediction responses. For a cleaner approach we can try a direct
  // request to the browsable API or infer from the first prediction.
  // Fallback: return the known CS:GO game.
  try {
    const { data } = await api.get('/predictions/', { params: { limit: 1 } });
    if (data.length > 0 && data[0].game_details) {
      return [data[0].game_details];
    }
  } catch {
    // ignore
  }
  return [
    {
      id: 1,
      name: 'Counter-Strike: Global Offensive / CS2',
      steam_id: '730',
      cover_image_url: 'https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg',
      genre: 'Action, FPS',
      min_requirements: {},
      rec_requirements: {},
    },
  ];
}

// ─── Predict FPS ─────────────────────────────────────────────────────
export async function predictFps(payload: PredictFpsRequest): Promise<PredictFpsResponse> {
  const { data } = await api.post('/predict-fps/', payload);
  return data;
}

// ─── Optimize Build ──────────────────────────────────────────────────
export async function optimizeBuild(payload: OptimizeBuildRequest): Promise<OptimizeBuildResponse> {
  const { data } = await api.post('/optimize-build/', payload);
  return data;
}
