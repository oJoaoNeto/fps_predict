import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import warnings
warnings.filterwarnings('ignore')

print("Iniciando treinamento do modelo...")

# 1. Carregamento dos Dados
CSV_PATH = "csv_result-fps-in-video-games.csv"
df_raw = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Dataset completo carregado: {df_raw.shape[0]:,} linhas.")

# 2. Filtragem para CS:GO 1080p Low
csgo = df_raw[
    (df_raw["GameName"]       == "counterStrikeGlobalOffensive") &
    (df_raw["GameResolution"] == 1080) &
    (df_raw["GameSetting"]    == "low")
].copy()

csgo = csgo.replace("?", np.nan)
csgo["FPS"] = pd.to_numeric(csgo["FPS"], errors="coerce")
csgo = csgo[(csgo["FPS"] >= 5) & (csgo["FPS"] <= 900)].copy()
print(f"CS:GO 1080p Low: {len(csgo):,} amostras de FPS filtradas.")

csgo["hw_combo"] = csgo["CpuName"] + "_" + csgo["GpuName"]

# 3. Agregação por Combo
NUMERIC_FEATS = [
    "CpuFrequency", "CpuNumberOfCores", "CpuNumberOfThreads",
    "CpuBaseClock", "CpuTurboClock", "CpuTDP", "CpuCacheL2", "CpuCacheL3",
    "CpuProcessSize", "CpuNumberOfTransistors",
    "GpuBoostClock", "GpuBaseClock", "GpuMemoryBus",
    "GpuMemorySize", "GpuBandwidth", "GpuNumberOfShadingUnits",
    "GpuNumberOfROPs", "GpuNumberOfTMUs", "GpuFP32Performance",
    "GpuNumberOfTransistors", "GpuPixelRate", "GpuTextureRate",
    "GpuDieSize", "GpuProcessSize",
]

for col in NUMERIC_FEATS:
    csgo[col] = pd.to_numeric(csgo[col], errors="coerce")

# Agregar: cada linha = uma combinação CPU+GPU única
agg = csgo.groupby("hw_combo").agg(
    FPS_mean   = ("FPS",              "mean"),
    FPS_count  = ("FPS",              "count"),
    GpuArch    = ("GpuArchitecture",  "first"),
    GpuMemType = ("GpuMemoryType",    "first"),
    **{c: (c, "first") for c in NUMERIC_FEATS}
).reset_index()

# Manter apenas combos com >= 5 medições (mais robustos)
agg = agg[agg["FPS_count"] >= 5].copy()

# Preencher NaN com mediana da coluna
for col in NUMERIC_FEATS:
    agg[col] = agg[col].fillna(agg[col].median())

print(f"Combos de hardware agregados (amostras >= 5): {len(agg)}")

# 4. Engenharia de Features
# CPU
agg["CpuTotalPower"]   = agg["CpuTurboClock"] * agg["CpuNumberOfCores"]
agg["CpuTurboRatio"]   = agg["CpuTurboClock"] / (agg["CpuFrequency"] + 1)
agg["ThreadsPerCore"]  = agg["CpuNumberOfThreads"] / (agg["CpuNumberOfCores"] + 1)
agg["CpuCache_Total"]  = agg["CpuCacheL2"] + agg["CpuCacheL3"].fillna(0)
agg["sqrt_CpuTurbo"]   = np.sqrt(agg["CpuTurboClock"])

# GPU
agg["GpuBoostRatio"]      = agg["GpuBoostClock"] / (agg["GpuBaseClock"] + 1)
agg["GpuClockDiff"]       = agg["GpuBoostClock"] - agg["GpuBaseClock"]
agg["GpuMemoryPower"]     = agg["GpuMemorySize"] * agg["GpuMemoryBus"]
agg["GpuShadingPerROP"]   = agg["GpuNumberOfShadingUnits"] / (agg["GpuNumberOfROPs"] + 1)
agg["BandwidthPerShader"] = agg["GpuBandwidth"] / (agg["GpuNumberOfShadingUnits"] + 1)
agg["GpuROPs_Bandwidth"]  = agg["GpuNumberOfROPs"] * agg["GpuBandwidth"]
agg["log_GpuFP32"]        = np.log1p(agg["GpuFP32Performance"])
agg["log_GpuBandwidth"]   = np.log1p(agg["GpuBandwidth"])

# CPU x GPU
agg["CpuGpuRatio"] = agg["CpuTurboClock"] / (agg["GpuFP32Performance"] + 1)

# Encoding de arquiteturas
ARCH_ORDER = {
    "Tesla": 1, "Tesla 2.0": 2,
    "Fermi": 3, "Fermi 2.0": 4,
    "TeraScale": 3, "TeraScale 2": 4, "TeraScale 3": 5,
    "GCN 1.0": 5, "GCN 2.0": 6, "GCN 3.0": 7, "GCN 4.0": 8,
    "Kepler": 6, "Kepler 2.0": 7, "Maxwell": 8, "Maxwell 2.0": 9,
    "GCN 5.0": 10, "GCN 5.1": 11, "Generation 7.0": 9,
    "Pascal": 11, "Turing": 12, "Volta": 12,
    "RDNA": 12, "RDNA 2": 13, "Ampere": 14,
}
MEM_ORDER = {"GDDR3": 1, "GDDR5": 2, "GDDR5X": 3,
             "HBM": 3, "HBM2": 4, "GDDR6": 4, "GDDR6X": 5}

agg["GpuArchScore"]       = agg["GpuArch"].map(ARCH_ORDER).fillna(7)
agg["GpuMemTypeScore"]    = agg["GpuMemType"].map(MEM_ORDER).fillna(2)
agg["GpuArch_x_Turbo"]    = agg["GpuArchScore"] * agg["CpuTurboClock"]

DERIVED_FEATS = [
    "CpuTotalPower", "CpuTurboRatio", "ThreadsPerCore", "CpuCache_Total", "sqrt_CpuTurbo",
    "GpuBoostRatio", "GpuClockDiff", "GpuMemoryPower", "GpuShadingPerROP",
    "BandwidthPerShader", "GpuROPs_Bandwidth", "log_GpuFP32", "log_GpuBandwidth",
    "CpuGpuRatio", "GpuArchScore", "GpuMemTypeScore", "GpuArch_x_Turbo",
]

ALL_FEATS = NUMERIC_FEATS + DERIVED_FEATS
X = agg[ALL_FEATS].fillna(0).copy()
y = agg["FPS_mean"]
y_log = np.log(y)

# 5. Treinamento Final do Modelo
final_model = GradientBoostingRegressor(
    n_estimators=400, learning_rate=0.03, max_depth=4,
    min_samples_leaf=2, subsample=0.8, random_state=42
)
final_model.fit(X, y_log)

# 6. Salvar Modelos e Metadados
joblib.dump(final_model, "fps_model_csgo_1080p_low.pkl")
joblib.dump(ALL_FEATS,   "fps_features_csgo_1080p_low.pkl")

# Salvar medianas para imputation de NaN
medians = {c: agg[c].median() for c in NUMERIC_FEATS}
joblib.dump(medians, "fps_medians_csgo_1080p_low.pkl")

print("Modelo final treinado e salvo com sucesso!")
print("   - fps_model_csgo_1080p_low.pkl")
print("   - fps_features_csgo_1080p_low.pkl")
print("   - fps_medians_csgo_1080p_low.pkl")
