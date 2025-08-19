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


## 💼 Descarga proyecto
En la CMD copie el siguiente comando
```shell
git clone https://github.com/MoisesGodoy17/copiloto-conversacional.git
cd copiloto-conversacionale 
```

## 📁 Preparación del ambiente 
### Creación de las variables de entorno
En la ruta `copiloto-conversacional\` crear una carpeta con el nombre `env-api`, dentro de la capeta `\env-api` crear un archivo con el nombre `.env`, luego ingresar al archivo creado donde debe copiar y pegar
el nombre de la API de gemini y la ruta de lectura, de la siguiente forma: 
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

## 🐳 Levantar el proyecto con Docker
Para ejecutar el proyecto con docker abra la CMD en la ruta raíz del proyecto `copiloto-conversacional\` e ingrese el comando:
```shell
docker-compose up --build
```
## 📄 Licencia

Este proyecto está bajo la Licencia GPL-3.0 license. Ver archivo `LICENSE.txt` para más detalles.

---

## 📧 Contacto
- **Desarrollador**: Moisés Godoy
- **Perfil**: [LinkedIn](https://www.linkedin.com/in/moises-andres-godoy-carreño-58b4a4370)
- **Repositorio**: [GitHub](https://github.com/MoisesGodoy17/)
- **Correo**: moisesgodoy1704@outlook.com




