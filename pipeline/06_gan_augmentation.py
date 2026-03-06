"""
=============================================================
ÉTAPE B — GAN AUGMENTATION (sur données corrigées)
=============================================================
Source  : outputs/final/train_final.csv
Signal  : value_norm_clipped (±3σ, sans runs courts)

Corrections vs version précédente :
  - Signal : value_norm_clipped au lieu de value_norm
  - Runs courts exclus → toutes les fenêtres complètes
  - Weighted sampling par run_id dans le DataLoader
  - WINDOW_SIZE=256 aligné avec SimCLR
  - Validation statistique plus stricte

Corrections de bugs (v2 → v3) :
  - BUG 1 (crash) : np.random.choice avec replace=False et
    N_SYNTHETIC > len(X) → ValueError. Corrigé : replace=True.
  - BUG 2 (effondrement GAN) : le Discriminateur domine dès
    l'époque 1 (Loss_D→0, Loss_G→10). Corrections :
      a) Label smoothing unilatéral (réel=0.9 au lieu de 1.0)
      b) Dropout(0.3) dans le Discriminateur
      c) Entraînement conditionnel du Discriminateur : D n'est
         mis à jour que si sa perte est > D_LOSS_THRESHOLD,
         ce qui laisse le temps au Générateur de rattraper.
  - BUG 3 (early stopping) : arrêt basé sur G_loss seul
    (toujours minimal à l'époque 1 → arrêt à l'époque 51).
    Corrigé : arrêt basé sur dist_to_nash = |G-0.693|+|D-0.693|.
=============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json, time, os
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

OUTPUT_DIR = Path("outputs/augmentation_v2")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device : {DEVICE}")
print("=" * 60)
print("  GAN AUGMENTATION v2 — Données corrigées")
print("=" * 60)

# ─────────────────────────────────────────────
# PARAMÈTRES
# ─────────────────────────────────────────────
WINDOW_SIZE        = 256
STRIDE             = 64        # pas glissant train
LATENT_DIM         = 64
BATCH_SIZE         = 128
EPOCHS             = 500
LR                 = 0.0002
BETA1              = 0.5
N_SYNTHETIC        = 5000
PATIENCE           = 50        # early stopping GAN
SEED               = 42

# CORRECTION BUG 2c — seuil pour l'entraînement conditionnel du Discriminateur.
# D n'est mis à jour que quand sa perte dépasse ce seuil ; cela évite que D
# écrase G dès les premières époques (Loss_D→0, gradient G nul).
D_LOSS_THRESHOLD   = 0.4

torch.manual_seed(SEED)
np.random.seed(SEED)

INPUT_DIR  = Path("outputs/final")

print(f"\n  WINDOW_SIZE={WINDOW_SIZE}  STRIDE={STRIDE}  "
      f"LATENT={LATENT_DIM}  EPOCHS={EPOCHS}")

# ─────────────────────────────────────────────
# ÉTAPE 1 — CHARGEMENT
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 1 — Chargement")
print("=" * 60)

df_train = pd.read_csv(INPUT_DIR / "train_final.csv")
with open(INPUT_DIR / "norm_final.json") as f:
    norm = json.load(f)

# Utiliser value_norm_clipped
sig = df_train["value_norm_clipped"].values.astype(np.float32)
run_ids = df_train["run_id"].values
weights_pts = df_train["weight"].values.astype(np.float32)

print(f"  Signal chargé   : {len(sig):,} pts (value_norm_clipped)")
print(f"  Min / Max       : {sig.min():.3f} / {sig.max():.3f}")
print(f"  Mean / Std      : {sig.mean():.3f} / {sig.std():.3f}")
print(f"  Runs uniques    : {len(np.unique(run_ids))}")

# ─────────────────────────────────────────────
# ÉTAPE 2 — FENÊTRES GLISSANTES AVEC POIDS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 2 — Fenêtres glissantes + weighted sampling")
print("=" * 60)

windows = []
window_weights = []
window_run_ids = []

for start in range(0, len(sig) - WINDOW_SIZE + 1, STRIDE):
    end = start + WINDOW_SIZE
    # Vérifier que la fenêtre est dans un seul run (pas de couture)
    runs_in_window = np.unique(run_ids[start:end])
    if len(runs_in_window) > 1:
        continue   # skip les fenêtres qui chevauchent deux runs

    # Vérifier is_boundary si la colonne existe
    if "is_boundary" in df_train.columns:
        if df_train["is_boundary"].values[start:end].any():
            continue   # skip les fenêtres aux coutures

    windows.append(sig[start:end])
    # Poids de la fenêtre = poids moyen des points (tous identiques dans un run)
    window_weights.append(float(weights_pts[start]))
    window_run_ids.append(int(run_ids[start]))

X = np.stack(windows).astype(np.float32)   # (N, WINDOW_SIZE)
W = np.array(window_weights, dtype=np.float32)
W = W / W.sum()   # normaliser

print(f"  Fenêtres extraites     : {len(X):,}")
print(f"  Fenêtres skippées      : coutures/multi-runs")
print(f"  Distribution par run   :")
run_win_counts = pd.Series(window_run_ids).value_counts().sort_index()
for rid, cnt in run_win_counts.nlargest(5).items():
    w = W[np.array(window_run_ids) == rid].sum()
    print(f"    run {rid:3d} : {cnt:5d} fenêtres → poids total={w:.4f}")

# ─────────────────────────────────────────────
# DATASET AVEC WEIGHTED SAMPLER
# ─────────────────────────────────────────────
class WindowDataset(Dataset):
    def __init__(self, X):
        self.X = torch.tensor(X).unsqueeze(1)   # (N, 1, W)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx]

dataset = WindowDataset(X)

# WeightedRandomSampler : chaque tirage est pondéré par le poids du run
# → les petits runs sont tirés aussi souvent que les grands
sampler = WeightedRandomSampler(
    weights     = torch.tensor(W),
    num_samples = len(W),
    replacement = True
)

loader = DataLoader(dataset, batch_size=BATCH_SIZE,
                    sampler=sampler, drop_last=True, num_workers=0)

print(f"\n  WeightedRandomSampler actif")
print(f"  Batches par époque : {len(loader)}")

# ─────────────────────────────────────────────
# ÉTAPE 3 — ARCHITECTURE DCGAN 1D
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 3 — Architecture DCGAN 1D")
print("=" * 60)

class Generator(nn.Module):
    """z[LATENT_DIM] → fenêtre [1, WINDOW_SIZE]"""
    def __init__(self, latent_dim, window_size):
        super().__init__()
        # Calculer la taille initiale pour arriver à window_size après 4 upsampling ×2
        init_len = window_size // 16   # 256//16 = 16
        self.init_len = init_len
        self.fc = nn.Linear(latent_dim, 256 * init_len)
        self.conv = nn.Sequential(
            # (256, 16) → (128, 32)
            nn.ConvTranspose1d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm1d(128), nn.ReLU(),
            # (128, 32) → (64, 64)
            nn.ConvTranspose1d(128, 64,  4, stride=2, padding=1),
            nn.BatchNorm1d(64),  nn.ReLU(),
            # (64, 64) → (32, 128)
            nn.ConvTranspose1d(64,  32,  4, stride=2, padding=1),
            nn.BatchNorm1d(32),  nn.ReLU(),
            # (32, 128) → (1, 256)
            nn.ConvTranspose1d(32,  1,   4, stride=2, padding=1),
            nn.Tanh()
        )
    def forward(self, z):
        x = self.fc(z).view(z.size(0), 256, self.init_len)
        return self.conv(x)

class Discriminator(nn.Module):
    """fenêtre [1, WINDOW_SIZE] → score [0,1]"""
    def __init__(self, window_size):
        super().__init__()
        self.conv = nn.Sequential(
            # (1, 256) → (32, 128)
            nn.Conv1d(1,   32,  4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            # CORRECTION BUG 2b — Dropout régularise D et ralentit son apprentissage,
            # évitant qu'il atteigne Loss_D=0 dès les premières époques.
            nn.Dropout(0.3),
            # (32, 128) → (64, 64)
            nn.Conv1d(32,  64,  4, stride=2, padding=1),
            nn.BatchNorm1d(64),  nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            # (64, 64) → (128, 32)
            nn.Conv1d(64,  128, 4, stride=2, padding=1),
            nn.BatchNorm1d(128), nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            # (128, 32) → (256, 16)
            nn.Conv1d(128, 256, 4, stride=2, padding=1),
            nn.BatchNorm1d(256), nn.LeakyReLU(0.2),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * (window_size // 16), 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.fc(self.conv(x))

G = Generator(LATENT_DIM, WINDOW_SIZE).to(DEVICE)
D = Discriminator(WINDOW_SIZE).to(DEVICE)

n_G = sum(p.numel() for p in G.parameters())
n_D = sum(p.numel() for p in D.parameters())
print(f"  Générateur     : {n_G:,} params")
print(f"  Discriminateur : {n_D:,} params")

opt_G   = torch.optim.Adam(G.parameters(), lr=LR, betas=(BETA1, 0.999))
opt_D   = torch.optim.Adam(D.parameters(), lr=LR, betas=(BETA1, 0.999))
loss_fn = nn.BCELoss()

# ─────────────────────────────────────────────
# ÉTAPE 4 — ENTRAÎNEMENT
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 4 — Entraînement DCGAN")
print("=" * 60)

hist_G, hist_D = [], []
# CORRECTION BUG 3 — utiliser dist_to_nash pour l'early stopping plutôt que
# la seule G_loss. G_loss est minimale à l'époque 1 (avant tout apprentissage
# utile), donc l'ancien critère déclenchait l'arrêt après seulement 51 époques.
# dist_to_nash mesure la distance à l'équilibre de Nash (0.693, 0.693),
# ce qui reflète réellement la convergence du GAN.
best_dist_nash = float("inf")
pat_cnt        = 0
t0             = time.time()

for epoch in range(1, EPOCHS + 1):
    ep_G = ep_D = 0.0
    n_batches = 0

    for real_batch in loader:
        real = real_batch.to(DEVICE)
        B    = real.size(0)

        # CORRECTION BUG 2a — Label smoothing unilatéral.
        # Utiliser 0.9 au lieu de 1.0 pour les vrais exemples empêche D de
        # devenir trop confiant trop rapidement (Loss_D → 0 dès l'époque 1).
        # Le label des faux reste 0.0 (pas de smoothing bilatéral).
        real_lbl = torch.full((B, 1), 0.9).to(DEVICE)
        fake_lbl = torch.zeros(B, 1).to(DEVICE)

        z    = torch.randn(B, LATENT_DIM).to(DEVICE)
        fake = G(z).detach()

        loss_D_real = loss_fn(D(real), real_lbl)
        loss_D_fake = loss_fn(D(fake), fake_lbl)
        loss_D      = (loss_D_real + loss_D_fake) / 2
        loss_D_val  = loss_D.item()   # sauvegardé avant backward() éventuel

        # CORRECTION BUG 2c — Entraînement conditionnel de D.
        # D n'est mis à jour que si sa perte actuelle est supérieure au seuil
        # D_LOSS_THRESHOLD. Si D est déjà trop bon (perte < seuil), on le
        # saute pour laisser G progresser avant le prochain affrontement.
        # loss_D_val est déjà calculé, aucun recalcul supplémentaire nécessaire.
        if loss_D_val > D_LOSS_THRESHOLD:
            opt_D.zero_grad()
            loss_D.backward()
            opt_D.step()

        # ── Entraîner Générateur ──────────────────
        z      = torch.randn(B, LATENT_DIM).to(DEVICE)
        fake   = G(z)
        # G essaie de tromper D : on veut que D(fake) ≈ 1.0
        loss_G = loss_fn(D(fake), torch.ones(B, 1).to(DEVICE))

        opt_G.zero_grad(); loss_G.backward(); opt_G.step()

        ep_G += loss_G.item(); ep_D += loss_D_val; n_batches += 1

    ep_G /= n_batches; ep_D /= n_batches
    hist_G.append(ep_G); hist_D.append(ep_D)

    # CORRECTION BUG 3 — early stopping sur dist_to_nash
    dist_to_nash = abs(ep_G - 0.693) + abs(ep_D - 0.693)
    if dist_to_nash < best_dist_nash:
        best_dist_nash = dist_to_nash
        pat_cnt        = 0
        torch.save(G.state_dict(), OUTPUT_DIR / "generator_best.pth")
        torch.save(D.state_dict(), OUTPUT_DIR / "discriminator_best.pth")
    else:
        pat_cnt += 1
        if pat_cnt >= PATIENCE:
            print(f"  Early stopping à l'époque {epoch}")
            break

    if epoch % 50 == 0 or epoch == 1:
        print(f"  Epoch [{epoch:>4}/{EPOCHS}]  "
              f"Loss_G={ep_G:.4f}  Loss_D={ep_D:.4f}  "
              f"|dist_Nash|={dist_to_nash:.4f}")

fit_time = time.time() - t0
print(f"\n  ✓ Entraînement terminé en {fit_time:.1f}s")
print(f"    Best dist_Nash : {best_dist_nash:.4f}  "
      f"(Nash equilibrium = 0.693 pour chacun)")

# Recharger meilleurs poids
G.load_state_dict(torch.load(OUTPUT_DIR / "generator_best.pth",
                              map_location=DEVICE))
G.eval()

# ─────────────────────────────────────────────
# ÉTAPE 5 — GÉNÉRATION SYNTHÉTIQUE
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 5 — Génération données synthétiques")
print("=" * 60)

with torch.no_grad():
    z_syn     = torch.randn(N_SYNTHETIC, LATENT_DIM).to(DEVICE)
    synthetic = G(z_syn).squeeze(1).cpu().numpy()   # (N_SYNTHETIC, WINDOW_SIZE)

# Dénormaliser pour comparaison statistique
mu_orig    = norm["mean"]
sigma_orig = norm["std"]
# En espace clipped[-3,3] → dénorm
syn_denorm  = np.clip(synthetic, -3, 3) * sigma_orig + mu_orig

# CORRECTION BUG 1 — replace=True au lieu de replace=False.
# N_SYNTHETIC=5000 > len(X)=4 506 : np.random.choice avec replace=False
# lève ValueError car on ne peut pas tirer 5 000 éléments distincts dans
# un pool de 4 506. replace=True autorise les répétitions, ce qui est
# acceptable pour une comparaison statistique.
real_sample = X[np.random.choice(len(X), N_SYNTHETIC, replace=True)]
real_denorm = real_sample * sigma_orig + mu_orig

print(f"  Fenêtres synthétiques : {N_SYNTHETIC:,}  shape={synthetic.shape}")
print(f"  Synthétique clipped   : [{synthetic.min():.3f}, {synthetic.max():.3f}]")

# ─────────────────────────────────────────────
# ÉTAPE 6 — VALIDATION STATISTIQUE STRICTE
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 6 — Validation statistique")
print("=" * 60)

stats_real = {
    "mean": real_denorm.mean(), "std":  real_denorm.std(),
    "p5":   np.percentile(real_denorm, 5),
    "p25":  np.percentile(real_denorm, 25),
    "p50":  np.percentile(real_denorm, 50),
    "p75":  np.percentile(real_denorm, 75),
    "p95":  np.percentile(real_denorm, 95),
}
stats_syn = {
    "mean": syn_denorm.mean(), "std":  syn_denorm.std(),
    "p5":   np.percentile(syn_denorm, 5),
    "p25":  np.percentile(syn_denorm, 25),
    "p50":  np.percentile(syn_denorm, 50),
    "p75":  np.percentile(syn_denorm, 75),
    "p95":  np.percentile(syn_denorm, 95),
}

print(f"  {'Stat':<8} {'Réel':>10} {'Synthétique':>12} {'Écart %':>10} Status")
print(f"  {'─'*50}")
all_ok = True
for key in stats_real:
    r, s  = stats_real[key], stats_syn[key]
    ecart = abs(r - s) / (abs(r) + 1e-8) * 100
    ok    = "OK" if ecart < 15 else "WARN"
    if ok == "WARN": all_ok = False
    print(f"  {key:<8} {r:>10.4f} {s:>12.4f} {ecart:>9.1f}%  {ok}")

# % de synthétique dans les bornes du réel
in_range = ((syn_denorm >= real_denorm.min()) &
            (syn_denorm <= real_denorm.max())).mean() * 100
print(f"\n  % synthétique dans bornes réel : {in_range:.1f}%  "
      f"({'OK' if in_range > 85 else 'WARN'})")

if all_ok and in_range > 85:
    print("  ✓ Distribution synthétique cohérente")
else:
    print("  ⚠ Distribution à vérifier — relancer avec plus d'epochs")

# ─────────────────────────────────────────────
# ÉTAPE 7 — CONSTRUCTION DATASET AUGMENTÉ
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ÉTAPE 7 — Dataset augmenté")
print("=" * 60)

# Signal réel (points individuels)
df_real_out = df_train[["index", "value", "run_id",
                         "value_norm_clipped", "weight"]].copy()
df_real_out["source"] = "real"
df_real_out.rename(columns={"value_norm_clipped": "value_norm"}, inplace=True)

# Signal synthétique (aplatir les fenêtres en points)
# On prend la valeur centrale de chaque fenêtre pour éviter les doublons
syn_flat   = synthetic[:, WINDOW_SIZE // 2]   # valeur centrale
syn_denorm_flat = syn_flat * sigma_orig + mu_orig

df_syn = pd.DataFrame({
    "index":      range(df_real_out["index"].max() + 1,
                        df_real_out["index"].max() + 1 + N_SYNTHETIC),
    "value":      syn_denorm_flat,
    "run_id":     -1,            # -1 = synthétique
    "value_norm": syn_flat,
    "weight":     1.0 / N_SYNTHETIC,
    "source":     "synthetic",
})

df_augmented = pd.concat([df_real_out, df_syn], ignore_index=True)
df_augmented = df_augmented.sample(frac=1, random_state=SEED).reset_index(drop=True)

df_augmented.to_csv(OUTPUT_DIR / "train_augmented_v2.csv", index=False)
df_syn.to_csv(OUTPUT_DIR / "synthetic_only_v2.csv", index=False)

print(f"  Signal réel        : {len(df_real_out):,} pts")
print(f"  Signal synthétique : {N_SYNTHETIC:,} pts ({100*N_SYNTHETIC/len(df_real_out):.1f}%)")
print(f"  Dataset augmenté   : {len(df_augmented):,} pts (mélangé)")
print(f"  ✓ train_augmented_v2.csv → outputs/augmentation_v2/")

# ─────────────────────────────────────────────
# VISUALISATION
# ─────────────────────────────────────────────
print("\n  Génération des visualisations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("GAN Augmentation v2 — Données corrigées\n"
             "value_norm_clipped | Runs courts exclus | "
             "Weighted sampling",
             fontsize=12, fontweight="bold")

# Plot 1 : courbes de loss
ax = axes[0, 0]
ax.plot(hist_G, color="#E74C3C", lw=1.5, label="Loss_G (Générateur)")
ax.plot(hist_D, color="#2196F3", lw=1.5, label="Loss_D (Discriminateur)")
ax.axhline(0.693, color="green", lw=1.5, ls="--",
           label="Nash equilibrium (0.693)")
ax.set_title("Courbes de loss GAN", fontsize=10, fontweight="bold")
ax.set_xlabel("Époque"); ax.set_ylabel("BCE Loss")
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
ax.set_facecolor("#f8f9fa")

# Plot 2 : fenêtres réelles vs synthétiques
ax = axes[0, 1]
n_show = 8
idx_r  = np.random.choice(len(X), n_show, replace=False)
for i, ir in enumerate(idx_r):
    alpha = 0.6 if i == 0 else 0.25
    lbl   = "Réel" if i == 0 else None
    ax.plot(X[ir], color="#2196F3", alpha=alpha, lw=1.2, label=lbl)
idx_s = np.random.choice(N_SYNTHETIC, n_show, replace=False)
for i, is_ in enumerate(idx_s):
    alpha = 0.6 if i == 0 else 0.25
    lbl   = "Synthétique" if i == 0 else None
    ax.plot(synthetic[is_], color="#E74C3C", alpha=alpha, lw=1.2,
            linestyle="--", label=lbl)
ax.set_title(f"Fenêtres réelles vs synthétiques ({n_show} chacune)",
             fontsize=10, fontweight="bold")
ax.set_xlabel("Position dans la fenêtre (pts)")
ax.set_ylabel("value_norm_clipped")
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
ax.set_facecolor("#f8f9fa")

# Plot 3 : distribution réel vs synthétique
ax = axes[1, 0]
ax.hist(real_denorm.flatten(), bins=80, alpha=0.6, density=True,
        color="#2196F3", label=f"Réel (n={len(real_denorm):,})")
ax.hist(syn_denorm.flatten(),  bins=80, alpha=0.6, density=True,
        color="#E74C3C", label=f"Synthétique (n={N_SYNTHETIC:,})")
ax.set_title("Distribution réel vs synthétique (Ampères)",
             fontsize=10, fontweight="bold")
ax.set_xlabel("Courant (A)"); ax.set_ylabel("Densité")
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
ax.set_facecolor("#f8f9fa")

# Plot 4 : apercu dataset augmenté
ax = axes[1, 1]
step = max(1, len(df_augmented) // 20_000)
df_p = df_augmented.iloc[::step]
real_mask = df_p["source"] == "real"
syn_mask  = df_p["source"] == "synthetic"
ax.scatter(df_p[real_mask].index, df_p[real_mask]["value"],
           s=0.3, alpha=0.4, color="#2196F3", label="Réel")
ax.scatter(df_p[syn_mask].index,  df_p[syn_mask]["value"],
           s=1.5, alpha=0.8, color="#E74C3C", label="Synthétique")
ax.set_title("Dataset augmenté (mélangé)\n"
             f"Réel={len(df_real_out):,} + Synthétique={N_SYNTHETIC:,}",
             fontsize=10, fontweight="bold")
ax.set_xlabel("Index mélangé"); ax.set_ylabel("Courant (A)")
ax.legend(fontsize=8, markerscale=5); ax.grid(True, alpha=0.3)
ax.set_facecolor("#f8f9fa")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "gan_augmentation_v2.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"  ✓ Figure : outputs/augmentation_v2/gan_augmentation_v2.png")

# ─────────────────────────────────────────────
# BILAN
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  BILAN GAN AUGMENTATION v2")
print("=" * 60)
print(f"""
  Corrections vs v1 :
    Signal         : value_norm_clipped (au lieu de value_norm)
    Runs courts    : exclus → {len(X):,} fenêtres (toutes completes)
    Weighted sampl.: actif → run 122 pondéré comme les petits runs
    WINDOW_SIZE    : 256 (aligné SimCLR)

  Corrections de bugs (crash + effondrement GAN) :
    BUG 1 (crash)  : replace=True dans np.random.choice (N_SYNTHETIC > len(X))
    BUG 2a (GAN)   : label smoothing réel=0.9 (évite Loss_D→0)
    BUG 2b (GAN)   : Dropout(0.3) dans Discriminateur (régularisation)
    BUG 2c (GAN)   : D entraîné seulement si loss_D > {D_LOSS_THRESHOLD}
    BUG 3 (stop)   : early stopping sur dist_to_nash (non sur G_loss seul)

  Résultats :
    Fenêtres réelles    : {len(X):,}
    Best dist_Nash      : {best_dist_nash:.4f}
    Nash equilibrium    : 0.693
    % in range          : {in_range:.1f}%
    Dataset augmenté    : {len(df_augmented):,} pts

  Fichiers :
    outputs/augmentation_v2/train_augmented_v2.csv
    outputs/augmentation_v2/synthetic_only_v2.csv
    outputs/augmentation_v2/generator_best.pth
    outputs/augmentation_v2/discriminator_best.pth

  Prochaine étape : python 06_Injection_Anomalies.py
""")
print("=" * 60)
