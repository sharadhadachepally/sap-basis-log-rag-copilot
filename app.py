import streamlit as st
import chromadb

st.set_page_config(page_title="SAP Basis RAG Copilot", page_icon="🛠️")
st.title("🛠️ SAP Basis Incident Diagnostic Copilot")
st.caption("Vector-Search RAG Engine for SAP ST22 Dumps & SM21 System Logs")

@st.cache_resource
def setup_vector_db():
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="sap_notes")
    if collection.count() == 0:
        with open("knowledge_base.txt", "r") as f:
            content = f.read()
        chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        ids = [f"note_{i}" for i in range(len(chunks))]
        collection.add(documents=chunks, ids=ids)
    return collection

collection = setup_vector_db()

if "log_text" not in st.session_state:
    st.session_state.log_text = ""

st.markdown("**1. Click any sample error below (or paste your own):**")
col1, col2, col3 = st.columns(3)
if col1.button("ST22 Memory Dump"):
    st.session_state.log_text = "Runtime Errors TSV_TNEW_PAGE_ALLOC_FAILED occurred during batch job Z_FI_EXTRACT on table BSEG."
if col2.button("DB Tablespace Full"):
    st.session_state.log_text = "DBIF_RSQL_SQL_ERROR ORA-01653 unable to extend table in tablespace PSAPSR3."
if col3.button("RFC Gateway Error"):
    st.session_state.log_text = "RFC_COMMUNICATION_FAILURE CPIC-RC 001 target host sapgw00 port 3300 unreachable."

log_input = st.text_area(
    "2. Active SAP Error Log:",
    value=st.session_state.log_text,
    height=110
)

if st.button("Diagnose Issue", type="primary"):
    if not log_input.strip():
        st.warning("Please click a sample button above or paste an SAP error log.")
    else:
        results = collection.query(query_texts=[log_input], n_results=1)
        matched_note = results["documents"][0][0]
        distance = results["distances"][0][0]
        confidence = max(0, round((1 - distance / 2) * 100, 1))

        st.success(f"Diagnosis Complete! (Vector Match Confidence: {confidence}%)")
        
        lines = matched_note.split("\n")
        st.subheader(lines[0])
        for line in lines[1:]:
            if line.startswith("Category:") or line.startswith("Root Cause:"):
                parts = line.split(":", 1)
                st.markdown(f"**{parts[0]}:** {parts[1]}")
            elif line.startswith("Resolution:"):
                st.markdown("### ✅ Step-by-Step Basis Resolution")
            else:
                st.write(line)
