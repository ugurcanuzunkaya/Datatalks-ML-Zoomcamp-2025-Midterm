"""
Train SWaT intrusion detection model WITHOUT SMOTE
Uses class_weight only to handle imbalance
"""

import pickle
from copy import deepcopy

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Constants
RANDOM_STATE = 42

print("=" * 80)
print("SWaT INTRUSION DETECTION - NO SMOTE TRAINING")
print("=" * 80)

# 1. Load data
print("\n[1/6] Loading data...")
df = pd.read_csv("merged.csv")
print(f"✅ Loaded dataset: {df.shape}")

# 2. Clean data
print("\n[2/6] Cleaning data...")
df.columns = df.columns.str.strip()
df = df.fillna(0)
df = df.rename(columns={"Normal/Attack": "target"})
df["target"] = (df["target"] == "Attack").astype(int)

print("✅ Data cleaned. Target distribution:")
print(df["target"].value_counts())
print(f"Original attack rate: {df['target'].mean() * 100:.2f}%")

# 3. Stratified split (chronological within each class)
print("\n[3/6] Creating stratified splits...")
df = df.sort_values("Timestamp").reset_index(drop=True)

df_normal = df[df["target"] == 0].reset_index(drop=True)
df_attack = df[df["target"] == 1].reset_index(drop=True)

n_normal = len(df_normal)
n_attack = len(df_attack)
n_train_normal = int(n_normal * 0.8)
n_train_attack = int(n_attack * 0.8)

df_train = pd.concat(
    [
        deepcopy(df_normal.iloc[:n_train_normal]),
        deepcopy(df_attack.iloc[:n_train_attack]),
    ],
    ignore_index=True,
)

df_train = df_train.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print(f"✅ Training set created: {df_train.shape}")
print(f"   Attack rate: {df_train['target'].mean() * 100:.2f}%")

# 4. Prepare features
print("\n[4/6] Preparing features...")
columns_to_drop = ["Timestamp", "target"]
df_train_features = df_train.drop(columns=columns_to_drop)
y_train = df_train["target"].values

train_dicts = df_train_features.to_dict(orient="records")
dv = DictVectorizer(sparse=False)
X_train = dv.fit_transform(train_dicts)

print("✅ Features prepared:")
print(f"   X_train shape: {X_train.shape}")
print(f"   Number of features: {len(dv.feature_names_)}")

# 5. Train WITHOUT SMOTE - use class_weight only
print("\n[5/6] Training with class_weight ONLY (no SMOTE)...")
print("Settings:")
print("  - C=1.0 (standard regularization)")
print("  - class_weight='balanced'")
print("  - solver='lbfgs'")
print("  - NO synthetic samples - using original data only")

model = LogisticRegression(
    max_iter=1000,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    C=1.0,  # Standard regularization
    class_weight="balanced",  # Let scikit-learn handle imbalance
    solver="lbfgs",
)
model.fit(X_train, y_train)
print("✅ Model trained successfully!")

# 6. Quick validation
print("\n[6/6] Quick validation...")
y_train_pred = model.predict(X_train)
y_train_pred_proba = model.predict_proba(X_train)[:, 1]

accuracy = accuracy_score(y_train, y_train_pred)
precision = precision_score(y_train, y_train_pred)
recall = recall_score(y_train, y_train_pred)
f1 = f1_score(y_train, y_train_pred)

print("Training metrics:")
print(f"  Accuracy:  {accuracy:.4f}")
print(f"  Precision: {precision:.4f}")
print(f"  Recall:    {recall:.4f}")
print(f"  F1-Score:  {f1:.4f}")

# Check prediction distribution
print("\nPrediction distribution:")
print(f"  Predicted Normal: {(y_train_pred == 0).sum()}")
print(f"  Predicted Attack: {(y_train_pred == 1).sum()}")
print(f"  Predicted attack rate: {y_train_pred.mean() * 100:.2f}%")

# Save artifacts
print("\n" + "=" * 80)
print("SAVING MODEL ARTIFACTS")
print("=" * 80)

with open("dv.bin", "wb") as f:
    pickle.dump(dv, f)
print("✅ DictVectorizer saved to: dv.bin")

with open("model.bin", "wb") as f:
    pickle.dump(model, f)
print("✅ Model saved to: model.bin")

print("\n" + "=" * 80)
print("TRAINING COMPLETE!")
print("=" * 80)
print("\nModel trained with NO SMOTE - class_weight only")
print("This preserves original data distribution: 3.79% attacks")
print("\nNext step: Test with '.venv/bin/python diagnose_model.py'")
