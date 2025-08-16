import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import ChatView from './components/ChatView.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChatView />
  </StrictMode>,
)
