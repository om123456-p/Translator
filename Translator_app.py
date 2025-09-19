import streamlit as st
import openai
import pdfplumber
import docx

st.title("🌍 Multilingual Document Translator")

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload your document (PDF or Word)", type=["pdf", "docx"])
target_lang = st.text_input("Enter target language (e.g., Hindi, English, French)")

if uploaded_file and target_lang:
    text = ""

    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    if st.button("Translate"):
        with st.spinner("Translating..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional multilingual document translator."},
                    {"role": "user", "content": f"Translate this text into {target_lang}: \n\n{text}"}
                ]
            )
            translated_text = response["choices"][0]["message"]["content"]
            st.subheader("✅ Translated Document:")
            st.write(translated_text)
