import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './styles/style-main.css'
import ChatView from './components/ChatView.jsx'
import UploadFileView from './components/UploadFileView.jsx'

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <div className="container">
      <div className="sidebar">
        <UploadFileView />
      </div>
      <div className="chat">
        <ChatView />
      </div>
    </div>
  </StrictMode>
);
