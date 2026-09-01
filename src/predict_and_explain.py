# src/predict_and_explain.py
import joblib
import pandas as pd
from src.features import extract_features_from_sequence, AMINO_ACIDS

def screen_candidate(sequence, sequence_name="Unknown Candidate"):
    print(f"\n--- Screening Sequence: {sequence_name} ---")
    
    # 1. Load the trained model and scaler
    try:
        rf_model = joblib.load("models/rf_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
    except FileNotFoundError:
        print("❌ Models not found. Please run train_models.py first.")
        return

    # 2. Extract features from the raw string
    feats = extract_features_from_sequence(sequence)
    
    # Ensure the columns match the exact order we used during training
    feature_names = [f"AAC_{aa}" for aa in AMINO_ACIDS] + [
        "Length", "Molecular_Weight", "Aromaticity", 
        "Instability_Index", "Isoelectric_Point", "GRAVY"
    ]
    
    # Create a 1-row DataFrame for the model
    df_candidate = pd.DataFrame([feats])[feature_names]
    
    # 3. Scale the features
    X_scaled = scaler.transform(df_candidate)
    
    # 4. Predict
    probability = rf_model.predict_proba(X_scaled)[0][1] # Probability of Class 1 (PETase)
    prediction = "PET-Degrading Enzyme (PETase)" if probability >= 0.5 else "Non-PETase"
    
    # 5. Output Results
    print(f"🤖 AI Prediction: {prediction}")
    print(f"📊 Confidence Score: {probability:.2%}")
    
    # 6. Explainable AI: Feature Importance
    print("\n🔬 Explainability (Top 5 Features driving this model's logic):")
    importances = rf_model.feature_importances_
    
    # Match feature names to their importance scores and sort them highest to lowest
    feature_importance = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    
    for feat, imp in feature_importance[:5]:
        # Print a visual bar using block characters
        bar = "█" * int(imp * 100)
        print(f"{feat:>20} | {bar} ({imp:.4f})")

if __name__ == "__main__":
    # Test Case 1: The famous IsPETase from Ideonella sakaiensis (Should be ~90%+ PETase)
    is_petase = "MNPAQQLAMVNFSWMALCAAANLAAAQSVEHVDITVQTNGANVQGQRCFTINVSRGPTSAWNAKTRFTTWTQNCNLTNCTATIQNNGPFTIAPQLISNTFSSNDPVAIVITGAIGENACAPNQVPAAALAGAAAPGAIGALIAENAVQAADTAEASQAAQAAQAAQAAQS"
    screen_candidate(is_petase, "IsPETase (Ideonella sakaiensis)")
    
    # Test Case 2: A random generic esterase (Should be Non-PETase)
    generic_esterase = "MTRKMTTQAQVIGTVTQGAIEAGYTVADLVRKIDGKQVRVVIADGGEVQAALEGAEAAIGTALLGAEQAGIGTLLQGAPGQAQA"
    screen_candidate(generic_esterase, "Generic Esterase Fragment")