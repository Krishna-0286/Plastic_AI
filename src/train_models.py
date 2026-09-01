# src/train_models.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def train_and_evaluate():
    print("--- Phase 4: Model Training ---")
    
    # 1. Load the features dataset
    df = pd.read_csv("data/processed/features_petase.csv")
    
    # 2. Separate Features (X) and Target (y)
    # We drop Accession, Protein_Name, and Target from the features
    X = df.drop(columns=["Accession", "Protein_Name", "Target"])
    y = df["Target"]
    
    # 3. Train-Test Split (80% Training, 20% Testing)
    # stratify=y ensures the 195:448 ratio is maintained in both sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Training on {len(X_train)} proteins, Testing on {len(X_test)} proteins.\n")
    
    # 4. Standardize the Features (Critical for Logistic Regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ---------------------------------------------------------
    # MODEL 1: Logistic Regression
    # ---------------------------------------------------------
    print("🤖 Training Logistic Regression...")
    lr_model = LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)
    
    lr_preds = lr_model.predict(X_test_scaled)
    lr_probs = lr_model.predict_proba(X_test_scaled)[:, 1]
    
    print("Logistic Regression Results:")
    print(f"ROC-AUC Score: {roc_auc_score(y_test, lr_probs):.4f}")
    print(classification_report(y_test, lr_preds, target_names=["Non-PETase (0)", "PETase (1)"]))
    
    # ---------------------------------------------------------
    # MODEL 2: Random Forest
    # ---------------------------------------------------------
    print("\n🌲 Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
    
    # Random Forest doesn't strictly need scaled data, but it's fine to use it
    rf_model.fit(X_train_scaled, y_train)
    
    rf_preds = rf_model.predict(X_test_scaled)
    rf_probs = rf_model.predict_proba(X_test_scaled)[:, 1]
    
    print("Random Forest Results:")
    print(f"ROC-AUC Score: {roc_auc_score(y_test, rf_probs):.4f}")
    print(classification_report(y_test, rf_preds, target_names=["Non-PETase (0)", "PETase (1)"]))
    
    # ---------------------------------------------------------
    # Save the Best Model and the Scaler
    # ---------------------------------------------------------
    # We will save the Random Forest model and the Scaler to use in our Web App
    joblib.dump(rf_model, "models/rf_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    print("\n✅ Saved Random Forest model to 'models/rf_model.pkl'")
    print("✅ Saved Feature Scaler to 'models/scaler.pkl'")

if __name__ == "__main__":
    train_and_evaluate()