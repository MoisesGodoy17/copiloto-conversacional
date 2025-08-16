import axios from 'axios';
async function SendQuery(query) {
    const API_URL = "http://127.0.0.1:5000/chat"

    try {
        const response = await axios.post(API_URL, query);
        console.log("Respuesta de la API:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error al enviar la consulta:", error);
        throw error;
    }
}

export default SendQuery;