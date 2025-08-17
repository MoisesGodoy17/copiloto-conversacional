import { useState, useEffect } from "react";
import { UploadFile, GetUploadedFiles, Compare_documents } from "../services/UploadFile.js";

function UploadFileView() {
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState("");
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [selectedFiles, setSelectedFiles] = useState([]); // ✅ Estado para checkboxes

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

    // ✅ Manejar selección/deselección de archivos
    const handleCheckboxChange = (e, fileName) => {
        if (e.target.checked) {
            setSelectedFiles([...selectedFiles, fileName]);
        } else {
            setSelectedFiles(selectedFiles.filter((f) => f !== fileName));
        }
    };

    // ✅ Enviar archivos seleccionados al servidor
    const handleCompare = async () => {
        if (selectedFiles.length < 2) {
            alert("Selecciona al menos 2 archivos para comparar ⚠️");
            return;
        }

        try {
            const res = await Compare_documents(selectedFiles)
            console.log("Respuesta comparación:", res);
            alert("Comparación enviada ✅");
        } catch (error) {
            console.error("Error al enviar comparación:", error);
            alert("Error al enviar comparación ❌");
        }
    };

    return (
        <div>
            <h1>Upload File View</h1>

            {/* Formulario para subir */}
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} accept=".pdf" />
                <button type="submit">Subir PDF</button>
            </form>

            {response && (
                <div>
                    <h2>Respuesta del servidor:</h2>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}

            {/* Lista de archivos con checkboxes */}
            <h2>Archivos subidos:</h2>
            <ul style={{ listStyleType: "none", padding: 0 }}>
                {uploadedFiles.map((file, index) => (
                    <li key={index}>
                        <label>
                            <input
                                type="checkbox"
                                checked={selectedFiles.includes(file)}
                                onChange={(e) => handleCheckboxChange(e, file)}
                            />
                            {file}
                        </label>
                    </li>
                ))}
            </ul>

            {/* Botón para enviar archivos seleccionados */}
            {uploadedFiles.length > 0 && (
                <button onClick={handleCompare} disabled={selectedFiles.length < 2}>
                    Comparar seleccionados
                </button>
            )}
        </div>
    );
}

export default UploadFileView;
