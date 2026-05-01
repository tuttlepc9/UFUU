import pandas as pd

print("=== UFUU Superconductivity Dataset Column Diagnostic ===")
print()

df_unique = pd.read_csv('unique_m.csv')
print(f"unique_m.csv shape: {df_unique.shape}")
print("Columns in unique_m.csv:")
print(df_unique.columns.tolist())
print("\nFirst 3 rows of unique_m.csv:")
print(df_unique.head(3).to_string())

print("\n" + "="*70)
df_train = pd.read_csv('train.csv')
print(f"train.csv shape: {df_train.shape}")
print("Columns in train.csv:")
print(df_train.columns.tolist()[:20])
print("\ncritical_temp column exists:", 'critical_temp' in df_train.columns)