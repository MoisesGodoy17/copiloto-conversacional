import { useState, useEffect } from "react";
import {UploadFile, GetUploadedFiles} from "../services/UploadFile.js";

function UploadFileView() {
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState("");
    const [uploadedFiles, setUploadedFiles] = useState([]);

    useEffect(() => {
        const fetchUploadedFiles = async () => {
            const files = await GetUploadedFiles();
            setUploadedFiles(files);
        };
        fetchUploadedFiles();
    }, []);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append("files", file);

        try {
            const res = await UploadFile(formData);
            setResponse(res);
            console.log("Archivo subido exitosamente:", res);
            alert("PDF subido con éxito ✅");
        } catch (error) {
            console.error("Error al subir el archivo:", error);
            alert("Error al subir el PDF ❌");
        }
    };
    return (
        <div>
            <h1>Upload File View</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} accept=".pdf" />
                <button type="submit">Subir PDF</button>
            </form>
            {response && <div><h2>Respuesta del servidor:</h2><pre>{JSON.stringify(response, null, 2)}</pre></div>}
            <h2>Archivos subidos:</h2>
            <ul>
                {uploadedFiles.map((file, index) => (
                    <li key={index}>
                        <label>
                            <input
                                type="checkbox"
                            />
                            {file}
                        </label>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default UploadFileView;