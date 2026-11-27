# 🛠️ SAP Basis Incident Diagnostic RAG Copilot

An AI-powered troubleshooting assistant built using **Retrieval-Augmented Generation (RAG)**, **ChromaDB**, and **Google Gemini** to diagnose SAP ABAP dumps (`ST22`) and system logs (`SM21`).

## 🚀 Problem Statement
SAP Basis consultants spend significant time manually analyzing runtime dumps and searching across SAP Notes during critical production incidents. This Copilot automates root-cause identification and provides step-by-step T-Code resolutions.

## 🏗️ Architecture
`SAP Error Log (ST22/SM21)` ➔ `Vector Search (ChromaDB)` ➔ `Retrieved SAP Note Context` ➔ `LLM Diagnosis (Gemini 2.5 Flash)` ➔ `Actionable Basis Resolution`

## 💻 Tech Stack
- **Language:** Python
- **LLM:** Google Gemini (`google-genai`)
- **Vector Database:** ChromaDB
- **Frontend UI:** Streamlit

## ⚙️ How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`
3. Enter your free Gemini API Key in the sidebar and paste an SAP error log.
