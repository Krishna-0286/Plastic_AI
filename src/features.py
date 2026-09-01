# src/features.py
import pandas as pd
import numpy as np
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# The 20 standard amino acids in alphabetical order
AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")

def extract_features_from_sequence(seq):
    """
    Extracts 26 biochemical and compositional features from a single protein sequence.
    """
    analysis = ProteinAnalysis(seq)
    seq_length = len(seq)
    
    # 1. Amino Acid Composition (AAC) - 20 features
    # Manually calculate to avoid Biopython version errors!
    feature_dict = {f"AAC_{aa}": seq.count(aa) / seq_length for aa in AMINO_ACIDS}
    
    # 2. Physicochemical Properties - 6 features
    feature_dict["Length"] = seq_length
    feature_dict["Molecular_Weight"] = analysis.molecular_weight()
    feature_dict["Aromaticity"] = analysis.aromaticity()
    feature_dict["Instability_Index"] = analysis.instability_index()
    feature_dict["Isoelectric_Point"] = analysis.isoelectric_point()
    feature_dict["GRAVY"] = analysis.gravy()  # Grand Average of Hydropathicity
    
    return feature_dict

def generate_features_dataset(input_csv, output_csv):
    print("--- Starting Feature Extraction ---")
    df = pd.read_csv(input_csv)
    print(f"Extracting features for {len(df)} sequences...")
    
    feature_list = []
    for idx, row in df.iterrows():
        seq = str(row['Sequence']).strip().upper()
        feats = extract_features_from_sequence(seq)
        
        # Keep metadata and target alongside features
        feats["Accession"] = row["Accession"]
        feats["Protein_Name"] = row["Protein_Name"]
        feats["Target"] = row["Target"]
        
        feature_list.append(feats)
    
    df_features = pd.DataFrame(feature_list)
    
    # Reorder columns so metadata & target are clean
    meta_cols = ["Accession", "Protein_Name", "Target"]
    feature_cols = [c for c in df_features.columns if c not in meta_cols]
    df_features = df_features[meta_cols + feature_cols]
    
    df_features.to_csv(output_csv, index=False)
    print(f"\n✅ Feature extraction complete!")
    print(f"Generated {len(feature_cols)} numerical features per protein.")
    print(f"Feature dataset saved to: {output_csv}")

if __name__ == "__main__":
    input_file = "data/processed/clean_petase_dataset.csv"
    output_file = "data/processed/features_petase.csv"
    
    generate_features_dataset(input_file, output_file)