import { useState } from "react";
import SendQuery from "../services/SendQuery";
import UploadFileView from "./UploadFileView";

function ChatView() {
    const [messages, setMessages] = useState([]);
    const [query, setQuery] = useState("");

    const querySend = { input: query };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        // Agregar mensaje del usuario
        setMessages(prev => [...prev, { role: "user", text: query }]);

        // Limpiar input
        setQuery("");

        SendQuery(querySend)
            .then(response => {
                console.log("Respuesta recibida:", response);

                // Agregar mensaje del bot
                setMessages(prev => [...prev, { role: "bot", text: response.response }]);
            })
            .catch(error => {
                console.error("Error al enviar la consulta:", error);
            });
    };

    return (
        <div>
            <UploadFileView />
            <h1>Chat View</h1>
            <ul>
                {messages.map((msg, index) => (
                    <li key={index}>
                        <b>{msg.role === "user" ? "Tú:" : "Bot:"}</b> {msg.text}
                    </li>
                ))}
            </ul>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Escribe un mensaje..."
                />
                <button type="submit">Enviar</button>
            </form>
        </div>
    );
}
export default ChatView;