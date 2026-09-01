# src/preprocess.py
import pandas as pd
import re

def clean_dataset(input_path, output_path):
    print("--- Starting Data Preprocessing ---")
    
    # 1. Load the raw data
    df = pd.read_csv(input_path)
    initial_count = len(df)
    print(f"Loaded {initial_count} raw protein sequences.")
    
    # 2. Drop missing values (just in case the API returned empty rows)
    df = df.dropna(subset=['Sequence', 'Target'])
    
    # 3. Drop exact duplicate sequences
    df = df.drop_duplicates(subset=['Sequence'], keep='first')
    dup_count = initial_count - len(df)
    print(f"Removed {dup_count} duplicate sequences.")
    
    # 4. Filter out non-standard amino acids
    # The 20 standard amino acids. Anything else (X, B, Z, J, O, U) is non-standard.
    standard_aa_pattern = re.compile(r'^[ACDEFGHIKLMNPQRSTVWY]+$')
    
    valid_mask = df['Sequence'].apply(lambda seq: bool(standard_aa_pattern.match(str(seq).upper())))
    df_clean = df[valid_mask]
    non_standard_count = len(df) - len(df_clean)
    print(f"Removed {non_standard_count} sequences containing unknown/non-standard amino acids.")
    
    # 5. Filter by Length (Keep proteins between 50 and 1500 amino acids)
    # This removes broken fragments and massive un-foldable complexes
    length_mask = (df_clean['Length'] >= 50) & (df_clean['Length'] <= 1500)
    df_final = df_clean[length_mask]
    length_count = len(df_clean) - len(df_final)
    print(f"Removed {length_count} sequences with abnormal lengths (<50 or >1500).")
    
    # 6. Final Statistics & Save
    print("\n--- Final Dataset Statistics ---")
    print(f"Total clean sequences: {len(df_final)}")
    print(f"PETases (Label 1): {len(df_final[df_final['Target'] == 1])}")
    print(f"Non-PETases (Label 0): {len(df_final[df_final['Target'] == 0])}")
    
    df_final.to_csv(output_path, index=False)
    print(f"\n🎉 Clean data successfully saved to {output_path}")

if __name__ == "__main__":
    raw_data_path = "data/raw/petase_dataset.csv"
    clean_data_path = "data/processed/clean_petase_dataset.csv"
    
    clean_dataset(raw_data_path, clean_data_path)