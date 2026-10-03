# 🧬 Plastic_AI: PETase Discovery Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://plasticai-9cmswusega9ylw8eav9z2s.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An *in-silico* machine learning pipeline that screens protein sequences to discover novel PET-degrading enzymes (**PETases**). By extracting 26 primary physicochemical and compositional descriptors, **Plastic_AI** eliminates slow, expensive wet-lab testing and identifies biological plastic degradation potential in seconds.

🔗 **Live Web Application:** [https://plasticai-9cmswusega9ylw8eav9z2s.streamlit.app/](https://plasticai-9cmswusega9ylw8eav9z2s.streamlit.app/)

---

## ⚡ Key Features

- **Automated Feature Extraction:** Computes 26 sequence descriptors using BioPython (20-D Amino Acid Composition, Aromaticity, GRAVY, Isoelectric Point, Instability Index, Molecular Weight).
- **High-Precision ML Classification:** Powered by a Random Forest Classifier trained on authenticated UniProt data (`EC 3.1.1.101` vs. non-PETase esterases).
- **Explainable AI (XAI):** Highlights top feature drivers behind predictions to explain underlying biochemical mechanisms.
- **Database Cross-Matching:** Automatically checks sequences against known repository entries (*IsPETase*, *LCC*, *TfCut2*).

---

## 📊 Model Performance

Evaluated on an unseen, stratified 20% test set ($N=129$):

| Metric | Score |
| :--- | :---: |
| **Accuracy** | **99%** |
| **F1-Score (PETase)** | **0.99** |
| **Recall (PETase)** | **1.00** |
| **Precision** | **0.97** |

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Machine Learning & Analysis:** Scikit-learn, BioPython, Pandas, NumPy
- **Data Ingestion:** UniProt REST API
- **Web App & Hosting:** Streamlit, Streamlit Cloud

---

## 🧪 Benchmark Test Sequences

Copy and paste these sample sequences into the live web application to test the model:

<details>
<summary><b>1. IsPETase (Ideonella sakaiensis) — Positive Control</b></summary>

```text
MNPAQQLAMVNFSWMALCAAANLAAAQSVEHVDITVQTNGANVQGQRCFTINVSRGPTSAWNAKTRFTTWTQNCNLTNCTATIQNNGPFTIAPQLISNTFSSNDPVAIVITGAIGENACAPNQVPAAALAGAAAPGAIGALIAENAVQAADTAEASQAAQAAQAAQAAQS
```
</details>

<details>
<summary><b>2. LCC (Leaf-Branch Compost Cutinase) — Positive Control</b></summary>

```text
MDGVLWRVRTAALMAALLAALAAWALVWASPSVEAQSNPYQRGPNPTRSALTADGPFSVATYTVSRLSVSGFGGGVIYYPTGTSLTFGGIAMSPGYTADASSLAWLGRRGCGLVSSYSWQGTTIGTPVWGGISLIGALTSDAQTFAAWAGIAVAGIGVNTATAGAAWGTSGLLAASTGLLQAASAAAGGVQTAA
```
</details>

<details>
<summary><b>3. Human Pancreatic Lipase — Negative Control</b></summary>

```text
MLPLLLLLLAAPTAASAKLGIAMVSVAQQGQLVLLGSSRGSSVTSATAAAGSSVQGVVIGVAAANSAASAQVSGGASGSAASTSSVAAAGVSVAAAGASTGVSASGAAQSVTASAGSGAGASVTSSVSASASGVSGASVTSSSSAGSAS
```
</details>

---

## 🚀 Quickstart (Local Setup)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_GITHUB_USERNAME/plastic_AI.git
cd plastic_AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit application
streamlit run app.py
```

---

## 📁 Repository Structure

```text
plastic_AI/
├── data/               # Raw and processed UniProt datasets
├── models/             # Trained Random Forest model & StandardScaler artifacts
├── src/                # Modular scripts (fetch_data, features, train_models)
├── app.py              # Streamlit web UI script
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.