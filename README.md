# Gemini_Streamlit
# Hazle preguntas a Gemini!

Este proyecto es una aplicación web interactiva construida con **Streamlit**, que utiliza **LangChain** y la API de Cohere para analizar el contenido de un archivo PDF subido por el usuario y responder preguntas relacionadas. Además, aprovecha la potencia del modelo **Gemini** de Google para generar respuestas inteligentes en español.

## Características

1. **Carga de PDF**: Permite al usuario subir un archivo PDF y extraer su contenido.
2. **División de texto**: El contenido del PDF se divide en chunks (fragmentos de texto) para un mejor manejo y contexto.
3. **Embeddings con Cohere**: Crea embeddings del contenido para facilitar la búsqueda y el recupero de información relevante.
4. **VectorStore con Chroma**: Los embeddings generados se almacenan en una base de datos vectorial persistente.
5. **Preguntas y respuestas**: Integra el modelo **Gemini** para responder preguntas en base al contenido subido.
6. **Respuesta en español**: Las respuestas generadas están diseñadas para ser claras, concisas y en español.

---

## Requisitos

### Instalación de dependencias

1. Clonar este repositorio.
2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```
3. Instalar las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

### Configuración de variables de entorno

Crear un archivo `.env` en el directorio del proyecto con las siguientes variables de entorno:

```
COHERE_API_KEY=tu_clave_de_api_de_cohere
GOOGLE_API_KEY=tu_clave_de_api_de_google
```

---

## Uso

1. Ejecutar la aplicación:
   ```bash
   streamlit run streamlit_langchain.py
   ```
2. Abrir el enlace proporcionado por Streamlit en el navegador.
3. Subir un archivo PDF a través del cargador de archivos.
4. Ver el contenido extraído del PDF y los chunks generados.
5. Presionar el botón **RUN QUERY** para realizar una pregunta y obtener una respuesta.

---

## Estructura del código

1. **Carga de PDF**:
   - Usa `PyPDF2` para extraer el texto del archivo PDF subido.
2. **División de texto**:
   - Implementa el `RecursiveCharacterTextSplitter` de LangChain para dividir el contenido en fragmentos manejables.
3. **Embeddings**:
   - Genera embeddings usando `CohereEmbeddings`.
4. **Base de datos vectorial**:
   - Utiliza `Chroma` para almacenar los embeddings y habilitar una recuperación eficiente del contexto relevante.
5. **Generación de respuestas**:
   - Emplea el modelo de lenguaje `ChatGoogleGenerativeAI` para responder preguntas con base en el contenido recuperado.
6. **Interfaz de usuario**:
   - Streamlit proporciona una interfaz sencilla para interactuar con las funcionalidades.

---

## Dependencias principales

- **Streamlit**: Para crear la interfaz de usuario.
- **LangChain**: Para la división de texto, embeddings y manejo del flujo de preguntas y respuestas.
- **Cohere**: Para generar embeddings del texto.
- **Chroma**: Para almacenar los embeddings en una base de datos vectorial.
- **Google Generative AI**: Para la generación de respuestas con el modelo Gemini.
- **PyPDF2**: Para leer y extraer el texto de archivos PDF.

---

## Consideraciones

1. **Embeddings y API keys**:
   - Asegúrate de que las claves de API de Cohere y Google sean válidas y estén configuradas correctamente en el archivo `.env`.
2. **PDFs complejos**:
   - Si un PDF tiene un formato muy complicado, la extracción del texto podría no ser perfecta. Puedes preprocesar manualmente los documentos si es necesario.
3. **Persistencia**:
   - Los embeddings generados se almacenan localmente en la carpeta `./content/VectorDB`.

---

## Ejemplo de flujo

1. Subir un archivo PDF que contenga información relevante (por ejemplo, un manual o reporte).
2. La aplicación divide el contenido en chunks y genera embeddings.
3. Ingresar una pregunta relacionada con el contenido, como: *¿Cuáles son los principales hallazgos del reporte?*
4. Recibir una respuesta generada en español por el modelo Gemini.

---

## Contacto

Si tienes preguntas o encuentras problemas, por favor abre un *issue* en el repositorio o contáctame por correo electrónico.

