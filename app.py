# app.py
import streamlit as st
import pandas as pd
import joblib
import re
from src.features import extract_features_from_sequence, AMINO_ACIDS

# --- Page Configuration ---
st.set_page_config(page_title="PETase AI Screener", page_icon="🧬", layout="wide")

# --- Load Models & Database Safely ---
@st.cache_resource
def load_data():
    try:
        model = joblib.load("models/rf_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        # Load our cleaned database to look up protein names!
        db = pd.read_csv("data/processed/clean_petase_dataset.csv")
        return model, scaler, db
    except Exception as e:
        st.error("Error loading files. Did you run Phase 4?")
        return None, None, None

rf_model, scaler, sequence_db = load_data()

feature_names = [f"AAC_{aa}" for aa in AMINO_ACIDS] + [
    "Length", "Molecular_Weight", "Aromaticity", 
    "Instability_Index", "Isoelectric_Point", "GRAVY"
]

# --- UI Header ---
st.title("🧬 AI-Driven PETase Discovery")
st.markdown("""
This tool uses a Machine Learning classification model (Random Forest) to predict 
whether a given protein sequence has the potential to degrade PET plastic.
""")

# --- Input Section ---
st.subheader("1. Enter Protein Sequence")
sample_sequence = "MNPAQQLAMVNFSWMALCAAANLAAAQSVEHVDITVQTNGANVQGQRCFTINVSRGPTSAWNAKTRFTTWTQNCNLTNCTATIQNNGPFTIAPQLISNTFSSNDPVAIVITGAIGENACAPNQVPAAALAGAAAPGAIGALIAENAVQAADTAEASQAAQAAQAAQAAQS"

user_input = st.text_area(
    "Paste Amino Acid Sequence (A-Z) below:", 
    value=sample_sequence, 
    height=150
)

# --- Processing & Prediction ---
if st.button("Analyze Protein", type="primary"):
    
    seq = str(user_input).strip().upper()
    seq = re.sub(r'\s+', '', seq) 
    
    if not re.match(r'^[ACDEFGHIKLMNPQRSTVWY]+$', seq):
        st.error("❌ Invalid sequence! Please ensure it only contains standard amino acid letters.")
    elif len(seq) < 50:
        st.error("❌ Sequence too short. Must be at least 50 amino acids.")
    else:
        with st.spinner("Analyzing sequence..."):
            
            # Extract and predict
            feats = extract_features_from_sequence(seq)
            df_candidate = pd.DataFrame([feats])[feature_names]
            X_scaled = scaler.transform(df_candidate)
            probability = rf_model.predict_proba(X_scaled)[0][1]
            
            # --- DATABASE LOOKUP: Find the Name! ---
            st.markdown("---")
            st.subheader("2. Identity & AI Screening Results")
            
            # Check if this sequence exists in our database
            match = sequence_db[sequence_db['Sequence'] == seq]
            
            if not match.empty:
                protein_name = match.iloc[0]['Protein_Name']
                st.info(f"🔍 **Database Match Found!** This protein is known as: **{protein_name}**")
            else:
                st.info("🔍 **Novel Sequence!** This sequence is not in our database. It is a completely new candidate.")

            # --- Display AI Results ---
            col1, col2 = st.columns(2)
            
            with col1:
                if probability >= 0.5:
                    st.success("✅ **Classification: High PET-Degradation Potential (PETase)**")
                else:
                    st.warning("⚠️ **Classification: Non-PETase (Standard Esterase/Hydrolase)**")
                    
                st.metric(label="AI Confidence (Probability)", value=f"{probability:.2%}")
                
            with col2:
                st.markdown("**Biochemical Properties:**")
                st.write(f"- **Length:** {feats['Length']} amino acids")
                st.write(f"- **Molecular Weight:** {feats['Molecular_Weight']:.2f} Daltons")
                st.write(f"- **GRAVY (Hydropathicity):** {feats['GRAVY']:.4f}")

            # --- Feature Importance Chart ---
            st.markdown("---")
            st.subheader("3. Explainable AI (Why did the model make this decision?)")
            
            importances = rf_model.feature_importances_
            importance_df = pd.DataFrame({
                "Feature": feature_names,
                "Importance": importances
            }).sort_values(by="Importance", ascending=False).head(10)
            
            st.bar_chart(data=importance_df, x="Feature", y="Importance", color="#00ff00")