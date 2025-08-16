from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pypdf import PdfReader
import json
import re
import os

# LangChain 0.3
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate

# -----------------------------
# Configuración de entorno
# -----------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env-api', '.env'))

# Configurar credenciales de Google desde variables del sistema
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_por_defecto")

# -----------------------------
# Inicializar el modelo Gemini y embeddings
# -----------------------------
# Usar las credenciales del JSON configurado en el sistema
model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai"
)

# Inicializar embeddings separadamente usando las credenciales del sistema
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

# Ruta donde Chroma guardara la DB
VECTOR_DB_PATH = "vector_store" 

# Inicializar Vector Store
if not os.path.exists(VECTOR_DB_PATH):
    os.makedirs(VECTOR_DB_PATH)

# Crear directorio de uploads si no existe
if not os.path.exists("uploads"):
    os.makedirs("uploads")

db = Chroma(
    collection_name="vector_store_agente", 
    persist_directory=VECTOR_DB_PATH, 
    embedding_function=embeddings
)

# -----------------------------
# Leer documentos PDF
# -----------------------------
# Leer el pdf
def process_pdf(file_path):
    try:
        render = PdfReader(file_path)
        text = ""  # almacena el texto del pdf
        for page in render.pages:
            text += page.extract_text()

        if not text.strip():
            raise ValueError("El PDF no contiene texto extraible")

        # Dividir en chunks 
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)

        # Añadir los chunks a la base de datos
        docs = [
            Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks
            ]

        topics = classify_documents(docs)  # Clasificar los chunks por temas
        for doc in docs:
            doc.metadata["topics"] = topics[0]

        print(f"Clasificación de temas: {doc.metadata['topics']}")

        db.add_documents(docs) # Almacena los chunks clasificados en el sistema
        
        print(f"Procesado exitosamente: {file_path} - {len(chunks)} chunks añadidos")
        
    except Exception as e:
        print(f"Error procesando {file_path}: {str(e)}")
        raise e
    
# -----------------------------
# Comparaciones automáticas entre documentos
# -----------------------------
# Crear resumen entre documentos ingresados en el sistema
def create_summary(doc_names):
    summaries = []
    for doc_name in doc_names:
        retriever = db.as_retriever(
            search_kwargs={
                "filter": {"source": doc_name}  # Se filtra por file_path ["source"]
            }
        )
        chunks = retriever.get_relevant_documents("")  # Trae los chunks del documento
        text = " ".join([chunk.page_content for chunk in chunks[:2]])  # configurado para tomar 2 chunks de cada documento
        summaries.append(text)
    return summaries

# Comparar documentos y generar diferencias
def compare_documents(doc_names):
    texts = create_summary(doc_names)

    combined_text = "\n\n---\n\n".join(
        [f"Documento {i+1}:\n{text}" for i, text in enumerate(texts)]
    )

    # Mensajes para el LLM
    messages = [
        SystemMessage(content=f"Compara los siguientes documentos y resalta diferencias clave y similitudes:\n\n{combined_text}"),
        HumanMessage(content="Genera un resumen de las diferencias y similitudes encontradas.")
    ]

    # Ejecutar el modelo y guardar la respuesta
    response = model.invoke(messages)
    print(f"Respuesta del modelo: {response.content}")

    return response

# -----------------------------
# Clasificación por temas o mezcla de tópicos
# -----------------------------
# Función para clasificar documentos
def classify_documents(chunks):
    prompt = PromptTemplate.from_template("""
        Analiza el siguiente texto y clasifícalo en una o más categorías temáticas
        (ej: legal, financiero, técnico, recursos humanos, marketing, contratos, salud, educación).
        Texto:
        {text}

        Responde SOLO en formato JSON, NO en MARKDOWN, con el campo "topics", ejemplo:
        {{"topics": ["legal"]}}
    """)

    text_chunks = " ".join([chunk.page_content for chunk in chunks[:2]])  # Tomar los primeros 2 chunks para la clasificación
    response = model.invoke([{"role": "user", "content": prompt.format(text=text_chunks)}])

    raw_output = response.content.strip()

    # Formatea documento (modelo retorna un markdown)
    raw_output = re.sub(r"^```json\s*", "", raw_output)
    raw_output = re.sub(r"^```", "", raw_output)
    raw_output = re.sub(r"```$", "", raw_output)

    topics = json.loads(raw_output)["topics"]

    return topics

# Prompt general del sistema (comportamiento del asistente)
system_prompt = """Eres un asistente útil que responde preguntas basándose en el contenido de documentos PDF. 
Proporciona respuestas precisas y concisas basadas en la información disponible. Si no encuentras información 
relevante en los documentos, indica claramente que no tienes esa información.

Contexto de los documentos:
{context}

Pregunta del usuario:
{question}
"""
QA_PROMPT = PromptTemplate(
    template=system_prompt,
    input_variables=["context", "question"],
)

# -----------------------------
# Endpoints Flask
# -----------------------------

@app.route("/compare_documents", methods=["POST"])
def compare_docs():
    try:
        data = request.get_json()
        if not data or 'doc_names' not in data:
            return jsonify({"error": "No se proporcionaron nombres de documentos"}), 400
            
        doc_names = data.get("doc_names")
        if not isinstance(doc_names, list) or len(doc_names) < 2:
            return jsonify({"error": "Se requieren al menos dos nombres de documentos para comparar"}), 400

        # Comparar documentos
        response = compare_documents(doc_names)
        response_text = getattr(response, "content", str(response))

        return jsonify({
            "response": response_text,
            "sources": doc_names
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error en comparacion de documentos: {str(e)}"}), 500

@app.route("/upload", methods=["POST"])
def upload_pdfs():
    try:
        files = request.files.getlist("files")
        if not files or files[0].filename == '':
            return jsonify({"error": "No se proporcionaron archivos"}), 400
        
        processed_files = []
        
        for file in files:
            if file and file.filename.endswith('.pdf'):
                file_path = os.path.join("uploads", file.filename)
                file.save(file_path)
                process_pdf(file_path)
                processed_files.append(file.filename)
            else:
                return jsonify({"error": f"Archivo {file.filename} no es un PDF válido"}), 400
        
        return jsonify({
            "message": "Archivos procesados exitosamente", 
            "processed_files": processed_files
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error procesando archivos: {str(e)}"}), 500

# Endpoint para el chat, donde se realizan las consultas
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({"error": "No se proporciono input en el request"}), 400
            
        user_input = data.get("input")
        if not user_input.strip():
            return jsonify({"error": "El input no puede estar vacío"}), 400

        # Crear retriever
        retriever = db.as_retriever(search_kwargs={"k": 3})  # Obtener los 3 documentos mas cercanos a la consulta

        # Crear la cadena QA
        qa_chain = RetrievalQA.from_chain_type(
            llm=model,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_PROMPT }
        )

        # Ejecutar la consulta
        result = qa_chain.invoke({"query": user_input})

        response_text = result["result"]
        sources = [doc.metadata.get("source", "Desconocido") for doc in result.get("source_documents", [])]
        topics = [doc.metadata.get("topics", "Desconocido") for doc in result.get("source_documents", [])]

        return jsonify({
            "response": response_text,
            "sources": list(set(sources)),  # Eliminar duplicados
            "topics": list(set(topics))
        })
        
    except Exception as e:
        return jsonify({"error": f"Error en chat: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "¡Hola! API de LangChain + ChromaDB está funcionando",
    })

# -----------------------------
# Ejecutar la app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

