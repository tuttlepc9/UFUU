import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

print("=== UFUU Holographic Fold Predictor v13 (FINAL FIXED): New Superconductors ===")
print("Plasma + radial depth (holographic features) + all engineered features\n")

# Load data
df_unique = pd.read_csv('unique_m.csv')
df_train = pd.read_csv('train.csv').drop(columns=['critical_temp'], errors='ignore')

# Keep original 'material' column
df = df_unique[['material', 'critical_temp']].copy()
df = pd.concat([df.reset_index(drop=True), df_train.reset_index(drop=True)], axis=1)

def get_family(formula):
    f = str(formula).upper()
    if 'CU' in f or 'YBA' in f or 'BI2SR' in f: return 'Cuprate'
    elif 'FE' in f and ('AS' in f or 'SE' in f or 'TE' in f): return 'Iron-based'
    elif 'NB' in f: return 'A15/Niobium'
    elif 'MGB' in f or 'MG B' in f: return 'Diboride'
    elif 'H' in f and len(f) > 3 or (('LA' in f or 'CE' in f) and 'H' in f): return 'Hydride'
    else: return 'Other'

df['family'] = df['material'].apply(get_family)

# Holographic / fold-inspired features
df['plasma'] = df['wtd_entropy_atomic_mass']
df['radial_depth'] = np.log2(df['number_of_elements'] + 1)
df['entanglement_proxy'] = df['plasma'] * np.log(df['radial_depth'] + 1)

print(f"Total materials: {len(df):,}")
print(f"Cuprate (known high-Tc): {len(df[df['family']=='Cuprate']):,}")
print(f"Other (potential new candidates): {len(df[df['family']=='Other']):,}\n")

# Features for ML
feature_cols = [col for col in df.columns if col not in ['material', 'critical_temp', 'family']]
X = df[feature_cols].values.astype(np.float32)
y = df['critical_temp'].values.astype(np.float32)

class TcPredictor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.net(x)

model = TcPredictor(X.shape[1])
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

X_tensor = torch.from_numpy(X)
y_tensor = torch.from_numpy(y).unsqueeze(1)

print("Training (holographic features included)...")
for epoch in range(8):
    optimizer.zero_grad()
    pred = model(X_tensor)
    loss = criterion(pred, y_tensor)
    loss.backward()
    optimizer.step()
    if epoch % 2 == 0:
        print(f"Epoch {epoch} loss: {loss.item():.2f}")

# Predict on "Other" family
other = df[df['family'] == 'Other'].copy()
X_other = other[feature_cols].values.astype(np.float32)
X_other_tensor = torch.from_numpy(X_other)
with torch.no_grad():
    other['predicted_Tc'] = model(X_other_tensor).numpy().flatten().clip(0)

# Top candidates
top_candidates = other.nlargest(30, 'predicted_Tc')[['material', 'predicted_Tc', 'plasma', 'radial_depth']]
print("\n=== Top 30 predicted new superconductor candidates ('Other' family) ===")
print(top_candidates.to_string(index=False))

top_candidates.to_csv('ufuu_predicted_new_superconductors.csv', index=False)
print("\nSaved to 'ufuu_predicted_new_superconductors.csv'")

plt.figure(figsize=(10, 5))
plt.scatter(other['plasma'], other['predicted_Tc'], alpha=0.6, s=10)
plt.xlabel('Plasma (holographic collective mode)')
plt.ylabel('Predicted Tc')
plt.title('Predicted New Superconductors — Plasma vs Tc')
plt.grid(True, alpha=0.3)
plt.show()

print("\n✅ Predictor complete!")
print("   • Top candidates are real materials from the dataset")
print("   • Ranked using holographic plasma + radial depth features")