import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Chat.css'
import { apiService } from '../services/api'
import type { GameplayResponse, QuotaResponse } from '../services/api'
import { userService, type UserData } from '../services/userService'

function Chat() {
  const navigate = useNavigate()
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean; category?: string }>>([])
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [quota, setQuota] = useState<QuotaResponse | null>(null)
  const [user, setUser] = useState<UserData | null>(null)
  const [chats] = useState([
    'New chat',
    'Como posso melhorar meus passes no efutebool?',
    'Qual a melhor formação para atacar?',
    'Como defender melhor?',
    'Melhor maneira de trocar a seta?',
  ])

  useEffect(() => {
    // Carregar dados do userService
    setUser(userService.getUserData())
    
    // Inscrever-se para mudanças
    const unsubscribe = userService.subscribe((userData) => {
      setUser(userData)
    })

    if (apiService.isAuthenticated()) {
      loadUserData()
      loadQuota()
    }

    return () => unsubscribe()
  }, [])

  const loadUserData = async () => {
    try {
      const userData = await apiService.getCurrentUser()
      const mappedUser: UserData = {
        email: userData.email || 'usuario@email.com',
        full_name: userData.name || 'Administrador',
        nickname: userData.nickname || 'Admin',
        platform: userData.platform || 'PC',
        is_premium: userData.is_premium || true,
        avatar_url: ''
      }
      userService.setUserData(mappedUser)
      setUser(mappedUser)
      console.log('Dados do usuário carregados:', userData)
    } catch (err) {
      console.error('Erro ao carregar dados do usuário:', err)
      // Usar dados padrão do userService
      setUser(userService.getUserData())
    }
  }

  const loadQuota = async () => {
    try {
      const quotaData = await apiService.getQuota()
      setQuota(quotaData)
    } catch (err) {
      console.error('Erro ao carregar quota:', err)
    }
  }

  const handleSendMessage = async () => {
    if (!message.trim()) return

    const userMessage = message
    setMessages(prev => [...prev, { text: userMessage, isUser: true }])
    setMessage('')
    setLoading(true)
    setError('')

    try {
      const response: GameplayResponse = await apiService.askGameplay(userMessage)
      
      setMessages(prev => [...prev, { 
        text: response.answer, 
        isUser: false,
        category: response.category 
      }])

      if (apiService.isAuthenticated()) {
        await loadQuota()
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao processar pergunta'
      setError(errorMessage)
      
      if (errorMessage.includes('login') || errorMessage.includes('autenticar')) {
        setMessages(prev => [...prev, { 
          text: `💡 ${errorMessage}\n\nVocê pode fazer login para acessar a IA completa ou continuar com respostas comuns do FAQ.`, 
          isUser: false 
        }])
      } else {
        setMessages(prev => [...prev, { 
          text: `❌ ${errorMessage}`, 
          isUser: false 
        }])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    apiService.logout()
    navigate('/login')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="chat-container">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''} ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" strokeWidth="2"/>
              <path d="M12 2a10 10 0 0 1 0 20" strokeWidth="2"/>
            </svg>
          </div>
          <button className="sidebar-toggle" onClick={() => setSidebarCollapsed(!sidebarCollapsed)} title={sidebarCollapsed ? 'Expandir' : 'Ocultar'}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" strokeWidth="2"/>
              <line x1="9" y1="3" x2="9" y2="21" strokeWidth="2"/>
            </svg>
          </button>
        </div>

        <nav className="sidebar-nav">
          <button className="sidebar-item" onClick={() => navigate('/dashboard')}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <circle cx="12" cy="7" r="4" strokeWidth="2"/>
            </svg>
            <span>Administrador</span>
          </button>

          <button className="sidebar-item" onClick={() => navigate('/user/settings')}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="3" strokeWidth="2"/>
              <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24" strokeWidth="2"/>
            </svg>
            <span>Configurações</span>
          </button>

          <button className="sidebar-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 20h9" strokeWidth="2" strokeLinecap="round"/>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" strokeWidth="2"/>
            </svg>
            <span>Novo chat</span>
          </button>
          
          <button className="sidebar-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8" strokeWidth="2"/>
              <path d="m21 21-4.35-4.35" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            <span>Buscar em chats</span>
          </button>

          <button className="sidebar-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" strokeWidth="2"/>
              <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/>
              <path d="m21 15-5-5L5 21" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            <span>Galeria</span>
          </button>

          <button className="sidebar-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" strokeWidth="2"/>
              <path d="M12 2a10 10 0 0 1 0 20" strokeWidth="2"/>
            </svg>
            <span>Sobre nós</span>
          </button>

          <button className="sidebar-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" strokeWidth="2"/>
            </svg>
            <span>Projetos</span>
          </button>
        </nav>

        <div className="sidebar-divider">
          <span>Seus chats</span>
        </div>

        <div className="sidebar-chats">
          {chats.map((chat, index) => (
            <button key={index} className="chat-item">
              {chat}
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          {apiService.isAuthenticated() && (
            <div className="user-profile-card">
              <div className="user-profile-header">
                <div className="user-avatar-gold">
                  {user?.full_name?.[0]?.toUpperCase() || 'A'}
                </div>
                <div className="user-profile-info">
                  <span className="user-name-large">
                    {user?.full_name || 'Administrador'}
                  </span>
                  <span className="user-plan-badge">{user?.is_premium ? 'PRO' : 'Grátis'}</span>
                </div>
                <button 
                  className="btn-edit-profile" 
                  onClick={() => navigate('/user/settings')}
                  title="Editar Perfil"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" strokeWidth="2"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" strokeWidth="2"/>
                  </svg>
                </button>
              </div>
              
              <button className="btn-upgrade-footer" onClick={() => navigate('/user/settings')}>
                Fazer upgrade
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Overlay */}
      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)}></div>}

      <div className={`main-content ${sidebarCollapsed ? 'expanded' : ''}`}>
      <header className="chat-header">
        <button className="menu-toggle" onClick={() => setSidebarOpen(true)}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="3" y1="12" x2="21" y2="12" strokeWidth="2" strokeLinecap="round"/>
            <line x1="3" y1="6" x2="21" y2="6" strokeWidth="2" strokeLinecap="round"/>
            <line x1="3" y1="18" x2="21" y2="18" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>
        <div className="chat-logo">
          <span className="logo-icon">⚽</span>
          <span className="logo-text">Efutebool</span>
        </div>
        <nav className="chat-nav">

        </nav>
        <div className="chat-auth">
          {!apiService.isAuthenticated() ? (
            <>
              <button className="btn-entrar" onClick={() => navigate('/login')}>Login</button>
              <button className="btn-cadastrar" onClick={() => navigate('/registro')}>Register</button>
            </>
          ) : (
            <button className="btn-logout-header" onClick={handleLogout}>Sair</button>
          )}
        </div>
      </header>

      <main className="chat-main">
        <div className="chat-content">
          {error && !messages.length && (
            <div className="chat-error">
              <p>{error}</p>
            </div>
          )}
          
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <h1 className="welcome-title">Como posso ajudar?</h1>
              {quota && (
                <p className="welcome-quota">
                  Você tem {quota.questions_remaining} perguntas restantes hoje
                </p>
              )}
            </div>
          ) : (
            <div className="chat-messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.isUser ? 'user-message' : 'bot-message'}`}>
                  {msg.category && (
                    <div className="message-category">📌 {msg.category}</div>
                  )}
                  <div className="message-content">{msg.text}</div>
                </div>
              ))}
              {loading && (
                <div className="message bot-message">
                  <div className="message-content typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <textarea
              className="chat-input"
              placeholder={loading ? "Aguarde a resposta..." : "Pergunte algo sobre eFootball..."}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              rows={1}
              disabled={loading}
            />

            <button 
              className="input-btn send-btn" 
              title="Enviar"
              onClick={handleSendMessage}
              disabled={loading || !message.trim()}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <line x1="22" y1="2" x2="11" y2="13" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
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
    </div>
  )
}

export default Chat
