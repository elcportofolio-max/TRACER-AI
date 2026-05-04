import streamlit as st
import google.generativeai as genai
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TRACER-AI Framework Dashboard", layout="wide")

# --- 2. KONEKSI API (MENGGUNAKAN SECRETS) ---
# Kode ini akan mengambil API Key dari settingan Streamlit Cloud nanti
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("API Key tidak ditemukan. Mohon atur GEMINI_API_KEY di Secrets Streamlit Cloud.")
    st.stop()

model = genai.GenerativeModel('gemini-pro')

# --- 3. ANTARMUKA PENGGUNA (UI) ---
st.title("🛡️ TRACER-AI Framework Dashboard")
st.markdown("### *Transparent, Real-time, Accountable Collaborative Evaluation Record*")
st.caption("Prototype Penelitian R&D - Program Doktor Pendidikan Bahasa Inggris")

st.divider()

# Membuat dua kolom: Kolom Kiri untuk Input Mahasiswa, Kolom Kanan untuk Hasil AI
col_input, col_display = st.columns([1, 2])

with col_input:
    st.header("📝 Student Portal")
    with st.form("input_form"):
        st.subheader("Informasi Mahasiswa")
        name = st.text_input("Nama Lengkap Mahasiswa")
        role = st.selectbox("Peran dalam Proyek", ["Lead Writer", "Researcher", "Designer", "Editor", "Coordinator"])
        
        st.subheader("Historical Record (Proses)")
        week = st.selectbox("Minggu Pengerjaan", ["Week 12", "Week 13", "Week 14", "Week 15"])
        logs = st.text_area("Log Aktivitas Mingguan (Jelaskan detail apa yang Anda kerjakan)", height=150)
        evidence = st.text_input("Link Bukti/Artifact (Google Docs/Drive/PDF)")
        
        submitted = st.form_submit_button("Kirim ke TRACER-AI")

with col_display:
    st.header("🔍 Lecturer Dashboard")
    if submitted:
        if name and logs and evidence:
            with st.spinner("AI sedang menganalisis data historis sesuai rubrik TRACER..."):
                # LOGIKA PROMPT (OTAK AI)
                prompt = f"""
                Evaluate this student contribution based on the TRACER-AI Analytic Rubric.
                
                STUDENT DATA:
                Name: {name}
                Role: {role}
                Week: {week}
                Log Activity: {logs}
                Evidence: {evidence}
                
                CRITERIA TO EVALUATE (Weight 25% each):
                1. Ability to Maintain Process Transparency.
                2. Ability to Exhibit Consistent Real-time Progress.
                3. Ability to Substantiate Individual Accountability.
                4. Communication (based on the clarity of logs).

                OUTPUT REQUIREMENT:
                - Give a Score (0-100) for each criteria.
                - Provide a Category (Very Good, Good, Fair, Poor).
                - Write a 'Historical Description' summary.
                - Detect if this student is a 'Free-rider' or a true contributor.
                - Format the result in a clean Table and bullet points.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success(f"Analisis untuk {name} Selesai!")
                    st.markdown("#### Hasil Evaluasi AI:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gagal menghubungi AI: {e}")
        else:
            st.warning("Mohon isi semua kolom (Nama, Log, dan Link Bukti) untuk memulai analisis.")
    else:
        st.info("Silakan isi form di sebelah kiri dan klik 'Kirim' untuk melihat hasil penilaian AI.")

st.divider()
st.caption("TRACER-AI Framework - Research Prototype 2026")