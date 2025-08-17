import axios from "axios";

export async function UploadFile(files) {
    const API_URL = "http://127.0.0.1:5000/upload"
    try {
        const res = await axios.post(API_URL, files, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });
        return res.data;
    } catch (error) {
        console.error("Error al subir el archivo:", error);
    }
}

export async function GetUploadedFiles(){
    const API_URL = "http://127.0.0.1:5000/get_name_pdf";
    try {
        const res = await axios.get(API_URL);
        return res.data.documentos;
    } catch (error) {
        console.error("Error al obtener los archivos subidos:", error);
    }
}

export async function Compare_documents(filesList) {
    const API_URL = "http://127.0.0.1:5000/compare_documents"
    try {
        const res = await axios.post(API_URL, { "doc_names" : filesList });
        return res.data;
    } catch (error) {
        console.error("Error al comparar documentos:", error);
    }
    
}