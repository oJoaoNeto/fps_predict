import os
import logging
import joblib
import numpy as np
import pandas as pd
from django.conf import settings

logger = logging.getLogger(__name__)

def predict_fps(game_name, cpu_specs, gpu_specs, ram_gb, resolution, quality_preset):
    """
    Realiza a predicao de FPS utilizando o modelo treinado de Machine Learning
    (Gradient Boosting Regressor) para CS:GO 1080p Low.
    
    Se o modelo ou os metadados nao estiverem presentes, utiliza uma heuristica
    automatica de fallback para garantir robustez.
    
    Se o usuario requisitar outras resolucoes ou qualidades graficas, o FPS
    de baseline (1080p Low) do modelo de ML e escalado proporcionalmente.
    """
    model_path = os.path.join(settings.BASE_DIR, "fps_model_csgo_1080p_low.pkl")
    features_path = os.path.join(settings.BASE_DIR, "fps_features_csgo_1080p_low.pkl")
    medians_path = os.path.join(settings.BASE_DIR, "fps_medians_csgo_1080p_low.pkl")

    # Verificar se todos os arquivos do modelo ML existem
    if os.path.exists(model_path) and os.path.exists(features_path) and os.path.exists(medians_path):
        try:
            # 1. Carregar modelo e metadados
            model = joblib.load(model_path)
            features = joblib.load(features_path)
            medians = joblib.load(medians_path)

            # 2. Mesclar specs da CPU e GPU
            specs = {}
            specs.update(cpu_specs)
            specs.update(gpu_specs)

            # 3. Mapear e preencher features necessarias (ou usar a mediana)
            s = {k: specs.get(k, medians.get(k, 0)) for k in features}

            # 4. Calcular features derivadas da Engenharia de Features
            turbo = float(s.get("CpuTurboClock", 0))
            freq  = float(s.get("CpuFrequency",  0))
            cores = float(s.get("CpuNumberOfCores", 1))
            threads = float(s.get("CpuNumberOfThreads", 1))
            boost = float(s.get("GpuBoostClock", 0))
            base  = float(s.get("GpuBaseClock",  0))
            mem   = float(s.get("GpuMemorySize", 0))
            bus   = float(s.get("GpuMemoryBus",  0))
            bw    = float(s.get("GpuBandwidth",  0))
            fp32  = float(s.get("GpuFP32Performance", 0))
            rops  = float(s.get("GpuNumberOfROPs", 1))
            shaders = float(s.get("GpuNumberOfShadingUnits", 1))
            l2    = float(s.get("CpuCacheL2", 0))
            l3    = float(s.get("CpuCacheL3", 0))
            arch  = float(s.get("GpuArchScore", 7))
            memt  = float(s.get("GpuMemTypeScore", 2))

            s["CpuTotalPower"]    = turbo * cores
            s["CpuTurboRatio"]    = turbo / (freq + 1)
            s["ThreadsPerCore"]   = threads / (cores + 1)
            s["CpuCache_Total"]   = l2 + l3
            s["sqrt_CpuTurbo"]    = np.sqrt(turbo)
            s["GpuBoostRatio"]    = boost / (base + 1)
            s["GpuClockDiff"]     = boost - base
            s["GpuMemoryPower"]   = mem * bus
            s["GpuShadingPerROP"] = shaders / (rops + 1)
            s["BandwidthPerShader"] = bw / (shaders + 1)
            s["GpuROPs_Bandwidth"]  = rops * bw
            s["log_GpuFP32"]        = np.log1p(fp32)
            s["log_GpuBandwidth"]   = np.log1p(bw)
            s["CpuGpuRatio"]        = turbo / (fp32 + 1)
            s["GpuArchScore"]       = arch
            s["GpuMemTypeScore"]    = memt
            s["GpuArch_x_Turbo"]    = arch * turbo

            # 5. Formatar entrada para predição como um DataFrame (evita warnings de feature names do scikit-learn)
            X_pred = pd.DataFrame([{f: s.get(f, 0) for f in features}])
            
            # 6. Inferência com o modelo (Gradient Boosting)
            # O target y_log foi treinado em log, entao aplicamos exp()
            predicted_log_fps = model.predict(X_pred)[0]
            base_fps = float(np.exp(predicted_log_fps))

            # 7. Aplicar modificadores de RAM adicionais (nao presentes no modelo ML direto)
            if ram_gb >= 16:
                ram_modifier = 1.0
            elif ram_gb >= 8:
                ram_modifier = 0.85
            else:
                ram_modifier = 0.55

            # 8. Modificadores de Resolução (relativos ao baseline de 1080p do modelo)
            res_modifiers = {
                '1080p': 1.0,
                '1440p': 0.72,
                '4K': 0.42
            }
            res_modifier = res_modifiers.get(resolution, 1.0)

            # 9. Modificadores de Preset Grafico (relativos ao baseline Low do modelo)
            # Como o modelo foi treinado em Low, multiplicamos paraPresets maiores:
            # Low = 1.0, Medium = 1/1.35, High = 0.82/1.35, Ultra = 0.64/1.35
            quality_modifiers = {
                'Low': 1.0,
                'Medium': 1.0 / 1.35,
                'High': 0.82 / 1.35,
                'Ultra': 0.64 / 1.35
            }
            quality_modifier = quality_modifiers.get(quality_preset, 1.0)

            # 10. Cálculo do FPS final
            final_fps = base_fps * ram_modifier * res_modifier * quality_modifier
            final_fps = max(1.0, round(final_fps, 1))

            logger.info(
                f"ML Prediction: Game={game_name}, RAM={ram_gb}GB, Res={resolution}, "
                f"Quality={quality_preset} => {final_fps} FPS (Base ML Low={base_fps:.1f} FPS)"
            )
            return final_fps

        except Exception as e:
            logger.error(f"Erro ao inferir FPS com o modelo de Machine Learning: {e}. Usando fallback...")

    # ================= Fallback Heurístico (Se o modelo falhar ou os PKLs não existirem) =================
    try:
        cpu_score = float(cpu_specs.get('score', 10000))
        gpu_score = float(gpu_specs.get('score', 8000))
        
        cpu_contribution = cpu_score / 120.0
        gpu_contribution = gpu_score / 80.0
        base_fps = cpu_contribution + gpu_contribution
        
        if ram_gb >= 16:
            ram_modifier = 1.0
        elif ram_gb >= 8:
            ram_modifier = 0.85
        else:
            ram_modifier = 0.55
            
        res_modifiers = {
            '1080p': 1.0,
            '1440p': 0.72,
            '4K': 0.42
        }
        res_modifier = res_modifiers.get(resolution, 1.0)
        
        quality_modifiers = {
            'Low': 1.35,
            'Medium': 1.0,
            'High': 0.82,
            'Ultra': 0.64
        }
        quality_modifier = quality_modifiers.get(quality_preset, 1.0)
        
        final_fps = base_fps * ram_modifier * res_modifier * quality_modifier
        return max(1.0, round(final_fps, 1))
        
    except Exception as e:
        logger.error(f"Erro no fallback do preditor de FPS: {e}")
        return 60.0
