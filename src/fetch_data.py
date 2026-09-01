# src/fetch_data.py
import requests
import pandas as pd
import time

def fetch_uniprot_data(query, label, max_records=500):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "tsv",
        "fields": "accession,protein_name,sequence,length",
        "size": max_records
    }
    
    print(f"Querying UniProt for: {query}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        if len(lines) <= 1:
            print("No records found.")
            return pd.DataFrame()
            
        headers = lines[0].split('\t')
        data = [line.split('\t') for line in lines[1:]]
        
        df = pd.DataFrame(data, columns=headers)
        df['Target'] = label 
        print(f"✅ Successfully fetched {len(df)} authentic records.")
        return df
    else:
        print(f"❌ API Request Failed. Status code: {response.status_code}")
        return pd.DataFrame()

if __name__ == "__main__":
    print("--- Starting Authentic Data Collection ---")
    
    # 1. Fetch Positives: Official PET hydrolases (EC 3.1.1.101)
    query_petase = "ec:3.1.1.101"
    df_positives = fetch_uniprot_data(query_petase, label=1, max_records=200)
    
    time.sleep(2)
    
    # 2. Fetch Negatives: Standard Esterases (EC 3.1.1.1) that are NOT PETases
    # Added parentheses for safer query syntax, and lowered max_records to the API limit of 500
    query_esterase = "(ec:3.1.1.1) NOT (ec:3.1.1.101)"
    df_negatives = fetch_uniprot_data(query_esterase, label=0, max_records=500)   
    if not df_positives.empty and not df_negatives.empty:
        df_final = pd.concat([df_positives, df_negatives], ignore_index=True)
        df_final.columns = ['Accession', 'Protein_Name', 'Sequence', 'Length', 'Target']
        
        output_path = "data/raw/petase_dataset.csv"
        df_final.to_csv(output_path, index=False)
        print(f"\n🎉 Success! Authentic dataset saved to {output_path} with {len(df_final)} total proteins.")