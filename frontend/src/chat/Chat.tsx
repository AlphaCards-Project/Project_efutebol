import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Chat.css'

function Chat() {
  const navigate = useNavigate()
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([])

  const handleSendMessage = () => {
    if (message.trim()) {
      setMessages([...messages, { text: message, isUser: true }])
      setMessage('')
      // Aqui você pode integrar com a API do chat
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="chat-logo">
          <span className="logo-icon">⚽</span>
          <span className="logo-text">Efutebool</span>
        </div>
        <nav className="chat-nav">
          <a href="#sobre">Sobre</a>
          <a href="#recursos">Recursos</a>
          <a href="#aprenda">Aprenda</a>
          <a href="#business">Business</a>
          <a href="#precos">Preços</a>
          <a href="#baixar">Baixar</a>
        </nav>
        <div className="chat-auth">
          <button className="btn-entrar" onClick={() => navigate('/login')}>Entrar</button>
          <button className="btn-cadastrar" onClick={() => navigate('/registro')}>Cadastre-se gratuitamente</button>
        </div>
      </header>

      <main className="chat-main">
        <div className="chat-content">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <h1 className="welcome-title">Como posso ajudar?</h1>
            </div>
          ) : (
            <div className="chat-messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.isUser ? 'user-message' : 'bot-message'}`}>
                  <div className="message-content">{msg.text}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <button className="input-btn" title="Anexar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            
            <button className="input-btn" title="Buscar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8" strokeWidth="2"/>
                <path d="m21 21-4.35-4.35" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </button>

            <textarea
              className="chat-input"
              placeholder="Pergunte alguma coisa"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              rows={1}
            />

            <button className="input-btn" title="Estudar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>

            <button className="input-btn" title="Criar imagem">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" strokeWidth="2"/>
                <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/>
                <path d="m21 15-5-5L5 21" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>

            <button className="input-btn voice-btn" title="Voz">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" strokeWidth="2"/>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <line x1="12" y1="19" x2="12" y2="23" strokeWidth="2" strokeLinecap="round"/>
                <line x1="8" y1="23" x2="16" y2="23" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <footer className="chat-footer">
          Ao enviar mensagens para o eFutebol, um chatbot de IA, você aceita nossos{' '}
          <a href="#termos">Termos</a> e reconhece nossa{' '}
          <a href="#privacidade">Política de Privacidade</a>. Confira as{' '}
          <a href="#preferencias">Preferências de cookies</a>.
        </footer>
      </main>
    </div>
  )
}

export default Chat
