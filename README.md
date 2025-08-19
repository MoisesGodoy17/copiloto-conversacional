# Copiloto Conversacional

Proyecto de prueba técnica: asistente conversacional que utiliza **Google Gemini**, **LangChain** y **Chroma DB**.  
Incluye backend en **Flask** y frontend en **React**.

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Flask, Flask-CORS  
- **Frontend:** React  
- **Procesamiento de documentos:** PyPDF
- **Framewrok** LangChain
- **Vector DB:** Chroma DB  
- **Modelo generativo:** Google Gemini (Gemini 2.0)  
- **Variables de entorno:** python-dotenv  
- **Contenedores:** Docker y Docker Compose  

---


## 💼 Descargar proyecto
En la CMD copie el siguiente comando:
```shell
git clone https://github.com/MoisesGodoy17/copiloto-conversacional.git
cd copiloto-conversacional
```
---

## 📁 Preparación del ambiente 
### Creación de las variables de entorno
En la ruta raíz del proyecto `copiloto-conversacional/`, crear una carpeta llamada env-api. Ahora en necesario crear el archivo de variable de entorno. Dentro de la carpeta `env-api/`, crear un archivo llamado `.env`.
Una vez creado, abrir el archivo `.env` recién creado y agregar la siguiente configuración:
```shell
GOOGLE_APPLICATION_CREDENTIALS=/app/env-api/gen-lang-client.json
```
### Obtener credenciales de servicio
1. **Acceder a Google Cloud Console**
   - Ir a [Google Cloud Console](https://console.cloud.google.com/)
   - Navegar a **IAM & Admin** → **Service Accounts**

2. **Crear/seleccionar cuenta de servicio**
   - Crear una nueva cuenta de servicio o seleccionar una existente
   - Asegurar que tenga permisos para usar Gemini API

3. **Generar clave JSON**
   - Ir a la pestaña **"Keys"**
   - Clic en **"Add key"** → **"Create new key"**
   - Seleccionar formato **JSON**
   - Descargar el archivo (solo disponible una vez)

4. **Configurar archivo de credenciales**
   - Renombrar el archivo descargado a `gen-lang-client.json`
   - Mover el archivo a `copiloto-conversacional/env-api/`

#### Estructura final esperada
```
copiloto-conversacional/
├── env-api/
│   ├── .env
│   └── gen-lang-client.json
....
```
---

## 🐳 Levantar el proyecto con Docker
Para ejecutar el proyecto con docker abra la CMD en la ruta raíz del proyecto `copiloto-conversacional\` e ingrese el comando:
```shell
docker-compose up --build
```
---

## 📐 Arquitectura del Sistema
### Diagrama de arquitectura de la solución
<img width="420" height="420" alt="Diagramas tesis-Arquitectura IA Copiloto drawio" src="https://github.com/user-attachments/assets/07487585-0087-4798-a976-e41b94a3147b" />

---

## 💡Justificaciones técnicas

### Backend: Flask
Se eligió Flask por su simplicidad y flexibilidad al momento de crear APIs ligeras. Es fácil de integrar con librerías externas (como LangChain o ChromaDB) y permite un rápido desarrollo. Además de poseer experiencia previa con esta tecnología.
### Frontend: React
React fue seleccionado por su modularidad y la facilidad para construir interfaces dinámicas e interactivas. Además de poseer experiencia previa con esta tecnología.

### Framework: LangChain
LangChain se emplea como capa de orquestación para conectar modelos de lenguaje con el almacenamiento vectorial (ChromaDB). Su capacidad para trabajar con cadenas de prompts y manejar grandes volúmenes de texto lo hace ideal para este sistema.

### Vector DB: ChromaDB
Se eligió ChromaDB como base de datos vectorial por su integración sencilla con LangChain, su eficiencia en búsquedas semánticas y su diseño pensado específicamente para aplicaciones de IA.

### Modelo generativo: Google Gemini (Gemini 2.0)
Gemini 2.0 se seleccionó como modelo principal por su capacidad de comprensión en lenguaje natural y su habilidad para generar respuestas contextuales y precisas. Además, de ser un modelo gratuito y facil de implementar en LangChain.

---

## 🌊 Flujo y funcionamiento del sistema
### Subida de documentos
El usuario puede subir hasta 5 PDFs al sistema. Una vez que un archivo llega al backend en Flask, este lo procesa para extraer su contenido en texto. 
Si el PDF no tiene texto legible (por ejemplo, si es solo una imagen), se notifica como error

### Procesamiento y división en fragmentos
El texto extraído no se guarda como un bloque gigante, sino que se divide en fragmentos más pequeños (chunks). Esto se hace para que después sea más fácil buscar información específica dentro del documento y para que el modelo de IA pueda trabajar con partes manejables del texto

###  Clasificación por temas
Cada texto se analiza con ayuda del modelo Gemini, que intenta detectar el tema principal (ejemplo: "recursos humanos", "educación", "tecnología"). Esa etiqueta de tema se guarda junto con el fragmento, como metadato

###  Almacenamiento en la base de conocimiento (ChromaDB)
Todos los fragmentos de todos los documentos se guardan en una base vectorial llamada ChromaDB. Esta base permite que, en lugar de hacer una búsqueda por palabras exactas, se pueda hacer una búsqueda "semántica", es decir, encontrar texto con un significado similar a lo que preguntó el usuario

### Consultas del usuario
Cuando el usuario hace una pregunta en el chat (ejemplo: "¿Cuál es la experiencia laboral de Moisés?"), el sistema primero busca en ChromaDB los fragmentos de texto más relevantes. Luego, esos fragmentos se envían junto con la consulta al modelo Gemini. Gemini responde tomando en cuenta la pregunta y la información de los documentos que se habían subido

### Comparación de documentos
El usuario también puede seleccionar varios documentos (por ejemplo, dos CVs) y pedir una comparación automática. En este caso, el backend extrae fragmentos relevantes de cada documento, se los pasa al modelo Gemini y este genera un análisis de las similitudes y diferencias

### Búsqueda por temas
Como cada texto está clasificado por un tema principal, el usuario puede pedir: "Muéstrame los documentos relacionados con educación". El sistema filtra en ChromaDB usando esas etiquetas de temas y devuelve los documentos que coinciden

### Interfaz de usuario
En el frontend, el chat muestra los mensajes en orden: primero lo que escribe el usuario y luego la respuesta del modelo. Cuando se suben archivos, aparecen listados, y el usuario puede marcar con checkboxes cuáles quiere usar para ciertas consultas (como comparaciones)

---

## 🔧 Limitaciones y mejoras futuras 

### Limitaciones de la solución

- Actualmente, la solución está pensada para ejecutarse en PC y no está optimizada para dispositivos móviles.
- La búsqueda semántica con ChromaDB puede verse limitada según el formato del PDF (por ejemplo, si el documento contiene muchas tablas, imágenes o texto escaneado sin OCR).
- La asignación de temas a los documentos se basa únicamente en los dos primeros fragmentos (chunks), que luego se replican para el resto del texto. Esto reduce el consumo del modelo Gemini, pero afecta la precisión de la clasificación temática.
- La comparación entre documentos también se hace tomando solo los dos primeros fragmentos de cada uno. Esto permite ahorrar recursos del modelo Gemini, pero no garantiza un análisis completo ni detallado.

### Posibles mejoras futuras

- Despliegue en la web: Publicar la aplicación en un servidor o nube (ejemplo: AWS, Azure, GCP, Vercel) para que se pueda usar desde cualquier dispositivo.
- Compatibilidad móvil: Adaptar la interfaz para celulares y tablets.
- OCR avanzado: Incorporar reconocimiento óptico de caracteres para extraer texto de PDFs escaneados o con imágenes.
- Clasificación más precisa: Asignar temas de manera dinámica a cada fragmento (no solo a los primeros) para mejorar la coherencia y granularidad de la información.
- Comparación más completa: Analizar múltiples fragmentos de cada documento en lugar de solo los primeros, logrando comparaciones más ricas y contextuales.
- Optimización del consumo de IA: Implementar cacheo de resultados y embeddings pre-generados para reducir llamadas innecesarias a Gemini.
- Interfaz interactiva: Agregar filtros, resúmenes automáticos y visualización de documentos por temas.
- Soporte multilenguaje: Permitir búsquedas y respuestas en distintos idiomas.
- Integración con otras fuentes: Conectar el sistema no solo a PDFs, sino también a Word, Excel o incluso bases de datos empresariales.

---

## 📄 Licencia

Este proyecto está bajo la Licencia GPL-3.0 license. Ver archivo `LICENSE.txt` para más detalles.

---

## 📧 Contacto
- **Desarrollador**: Moisés Godoy
- **Perfil**: [LinkedIn](https://www.linkedin.com/in/moises-andres-godoy-carreño-58b4a4370)
- **Repositorio**: [GitHub](https://github.com/MoisesGodoy17/)
- **Correo**: moisesgodoy1704@outlook.com




