# Librerías para la preparación de datos
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.document_loaders import PyPDFDirectoryLoader  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

# Librerías para el proceso de Retrieval
from langchain import hub  
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnablePassthrough 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.schema import Document

import streamlit as st
from io import StringIO
import os

import cohere
import numpy as np
from dotenv import load_dotenv
from langchain.embeddings import CohereEmbeddings

import PyPDF2


# Configuración de la página
st.set_page_config(
    page_title="Hazle preguntas a Gemini!",
    page_icon=":rocket:",
    layout="wide",
)

# Encabezados 
st.markdown("<h1 style='text-align: center;'>🤖 Hazle preguntas a Gemini</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Sube un archivo PDF, escribe una pregunta y obtén respuestas inteligentes.</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col2:
    st.image("Gemini.jpg", width=600)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<ol>
    <li>Sube tu archivo PDF</li>
    <li>Escribe tu pregunta en el campo de texto</li>
    <li>Haz clic en 'Pregunta!' para obtener una respuesta</li>
</ol>
""", unsafe_allow_html=True)

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"

file = st.file_uploader("Upload a PDF file", type="pdf")

splits = []
if file is not None:
    # Leer el archivo PDF
    pdf_reader = PyPDF2.PdfReader(file)
    # Extraer el contenido del PDF
    content = ""
    for page in pdf_reader.pages:  # Iterar directamente sobre las páginas
        content += page.extract_text()  # Usar el método correcto extract_text()

    # Convertir el texto extraído en una lista de objetos Document
    documents = [Document(page_content=content)]

    st.success("Archivo cargado exitosamente. ¡Puedes hacer tu pregunta ahora!")
# Particionando los datos. Con un tamaño delimitado (chunks) y 
# 200 caracters de overlapping para preservar el contexto
    text_splitter = RecursiveCharacterTextSplitter( 
        separators=["\n\n", "\n", ". ", " "],
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)

# Crea la instancia de embeddings con Cohere
embeddings_model = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"], user_agent="antonio")  

path_db = "./content/VectorDB"  # Ruta a la base de datos del vector store

# Crear el vector store a partir de tus documentos 'splits'
vectorstore = Chroma.from_documents(   
    documents=splits, 
    embedding=embeddings_model, 
    persist_directory=path_db # persist = guardarlos: Para que podamos persistir los datos y no generarlos todo el tiempo
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.environ["GOOGLE_API_KEY"])

retriever = vectorstore.as_retriever()

prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    # Funcion auxiliar para enviar el contexto al modelo como parte del prompt
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

prompt.messages[0].prompt.template = "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. Answer in spanish. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:"

user_input = st.text_input("Cuál es tu pregunta:")

if st.button("Pregunta!", type="primary"):
    if user_input:
        response = rag_chain.invoke(user_input)

        st.subheader("Generated Answer: " )
        st.write(response)
    else:
        st.warning("Por favor, ingresa una pregunta válida.")


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Aplicación desarrollada con ❤️ usando Streamlit y Cohere API, junto con el LLM de Gemini.</p>", unsafe_allow_html=True)