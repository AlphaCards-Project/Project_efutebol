import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './UserSettings.css'
import { userService, type UserData } from '../services/userService'

interface UserPreferences {
  theme: string
  language: string
  notifications: boolean
  email_updates: boolean
  auto_save_chats: boolean
}

function UserSettings() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'profile' | 'preferences' | 'subscription'>('profile')
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  
  const [profileData, setProfileData] = useState<UserData>(userService.getUserData())
  
  const [editData, setEditData] = useState<UserData>(profileData)
  
  const [preferences, setPreferences] = useState<UserPreferences>({
    theme: 'dark',
    language: 'pt-BR',
    notifications: true,
    email_updates: false,
    auto_save_chats: true
  })

  useEffect(() => {
    loadUserData()
    
    // Inscrever-se para mudanças no userService
    const unsubscribe = userService.subscribe((userData) => {
      if (userData) {
        setProfileData(userData)
        if (!isEditing) {
          setEditData(userData)
        }
      }
    })

    return () => unsubscribe()
  }, [])

  const loadUserData = async () => {
    // Carregar dados do userService
    const userData = userService.getUserData()
    setProfileData(userData)
    setEditData(userData)
  }

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setEditData({
      ...editData,
      [e.target.name]: e.target.value
    })
  }

  const handlePreferenceChange = (key: keyof UserPreferences, value: string | boolean) => {
    setPreferences({
      ...preferences,
      [key]: value
    })
  }

  const handleSaveProfile = async () => {
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      setProfileData(editData)
      userService.setUserData(editData) // Atualizar no userService
      setIsEditing(false)
      setSuccess('Perfil atualizado com sucesso!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Erro ao atualizar perfil')
    } finally {
      setLoading(false)
    }
  }

  const handleSavePreferences = async () => {
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      setSuccess('Preferências salvas com sucesso!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Erro ao salvar preferências')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="user-settings-container">
      <button className="btn-back" onClick={() => navigate('/chat')} title="Voltar ao Chat">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M19 12H5M12 19l-7-7 7-7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      <div className="settings-box">
        {/* Header com Avatar */}
        <div className="settings-header">
          <div className="user-avatar-large">
            {profileData.full_name?.[0]?.toUpperCase() || 'U'}
          </div>
          <h1 className="settings-title">{profileData.full_name}</h1>
          <p className="settings-subtitle">{profileData.is_premium ? '⭐ Premium' : '🎮 Grátis'}</p>
        </div>

        {/* Tabs */}
        <div className="settings-tabs">
          <button 
            className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" strokeWidth="2"/>
              <circle cx="12" cy="7" r="4" strokeWidth="2"/>
            </svg>
            Perfil
          </button>
          <button 
            className={`tab-button ${activeTab === 'preferences' ? 'active' : ''}`}
            onClick={() => setActiveTab('preferences')}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="3" strokeWidth="2"/>
              <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24" strokeWidth="2"/>
            </svg>
            Preferências
          </button>
          <button 
            className={`tab-button ${activeTab === 'subscription' ? 'active' : ''}`}
            onClick={() => setActiveTab('subscription')}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" strokeWidth="2"/>
            </svg>
            Assinatura
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Tab Content */}
        <div className="tab-content">
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="profile-section">
              <div className="form-group">
                <label htmlFor="full_name">Nome Completo</label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={editData.full_name}
                  onChange={handleProfileChange}
                  disabled={!isEditing}
                  className={!isEditing ? 'disabled' : ''}
                />
              </div>

              <div className="form-group">
                <label htmlFor="nickname">Nickname</label>
                <input
                  type="text"
                  id="nickname"
                  name="nickname"
                  value={editData.nickname}
                  onChange={handleProfileChange}
                  disabled={!isEditing}
                  className={!isEditing ? 'disabled' : ''}
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">E-mail</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={editData.email}
                  onChange={handleProfileChange}
                  disabled={!isEditing}
                  className={!isEditing ? 'disabled' : ''}
                />
              </div>

              <div className="form-group">
                <label htmlFor="platform">Plataforma</label>
                <select
                  id="platform"
                  name="platform"
                  value={editData.platform}
                  onChange={handleProfileChange}
                  disabled={!isEditing}
                  className={!isEditing ? 'disabled' : ''}
                >
                  <option value="PC">PC</option>
                  <option value="Console">Console</option>
                  <option value="Mobile">Mobile</option>
                </select>
              </div>

              <div className="form-actions">
                {!isEditing ? (
                  <button className="btn-primary" onClick={() => setIsEditing(true)}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" strokeWidth="2"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" strokeWidth="2"/>
                    </svg>
                    Editar Perfil
                  </button>
                ) : (
                  <>
                    <button className="btn-secondary" onClick={() => {
                      setEditData(profileData)
                      setIsEditing(false)
                    }} disabled={loading}>
                      Cancelar
                    </button>
                    <button className="btn-primary" onClick={handleSaveProfile} disabled={loading}>
                      {loading ? 'Salvando...' : 'Salvar'}
                    </button>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Preferences Tab */}
          {activeTab === 'preferences' && (
            <div className="preferences-section">
              <div className="preference-group">
                <h3>Aparência</h3>
                <div className="preference-item">
                  <div className="preference-info">
                    <label>Tema</label>
                    <span>Escolha entre claro ou escuro</span>
                  </div>
                  <select
                    value={preferences.theme}
                    onChange={(e) => handlePreferenceChange('theme', e.target.value)}
                  >
                    <option value="dark">Escuro</option>
                    <option value="light">Claro</option>
                    <option value="auto">Automático</option>
                  </select>
                </div>

                <div className="preference-item">
                  <div className="preference-info">
                    <label>Idioma</label>
                    <span>Idioma da interface</span>
                  </div>
                  <select
                    value={preferences.language}
                    onChange={(e) => handlePreferenceChange('language', e.target.value)}
                  >
                    <option value="pt-BR">Português (BR)</option>
                    <option value="en">English</option>
                    <option value="es">Español</option>
                  </select>
                </div>
              </div>

              <div className="preference-group">
                <h3>Notificações</h3>
                <div className="preference-item">
                  <div className="preference-info">
                    <label>Notificações Push</label>
                    <span>Receba alertas no navegador</span>
                  </div>
                  <label className="toggle">
                    <input
                      type="checkbox"
                      checked={preferences.notifications}
                      onChange={(e) => handlePreferenceChange('notifications', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>

                <div className="preference-item">
                  <div className="preference-info">
                    <label>Atualizações por E-mail</label>
                    <span>Novidades e promoções</span>
                  </div>
                  <label className="toggle">
                    <input
                      type="checkbox"
                      checked={preferences.email_updates}
                      onChange={(e) => handlePreferenceChange('email_updates', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>

              <div className="preference-group">
                <h3>Chat</h3>
                <div className="preference-item">
                  <div className="preference-info">
                    <label>Salvar Conversas Automaticamente</label>
                    <span>Mantenha histórico de chats</span>
                  </div>
                  <label className="toggle">
                    <input
                      type="checkbox"
                      checked={preferences.auto_save_chats}
                      onChange={(e) => handlePreferenceChange('auto_save_chats', e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>

              <div className="form-actions">
                <button className="btn-primary" onClick={handleSavePreferences} disabled={loading}>
                  {loading ? 'Salvando...' : 'Salvar Preferências'}
                </button>
              </div>
            </div>
          )}

          {/* Subscription Tab */}
          {activeTab === 'subscription' && (
            <div className="subscription-section">
              <div className="current-plan">
                <h3>Plano Atual</h3>
                <div className="plan-card">
                  <div className="plan-header">
                    <span className="plan-icon">
                      {profileData.role === 'admin' ? '👑' : profileData.is_premium ? '⭐' : '🎮'}
                    </span>
                    <div>
                      <h4>
                        {profileData.role === 'admin' ? 'Administrador' : profileData.is_premium ? 'Premium' : 'Grátis'}
                      </h4>
                      <p>
                        {profileData.role === 'admin' 
                          ? 'Acesso total ao sistema' 
                          : profileData.is_premium 
                            ? 'Acesso ilimitado' 
                            : '5 perguntas por dia'}
                      </p>
                    </div>
                  </div>
                  {profileData.role === 'free' && (
                    <div className="plan-features">
                      <p className="feature">✓ 5 perguntas IA por dia</p>
                      <p className="feature">✓ Acesso ao FAQ</p>
                      <p className="feature">✓ Builds básicas</p>
                    </div>
                  )}
                </div>
              </div>

              {profileData.role === 'free' && (
                <div className="upgrade-plan">
                  <h3>Fazer Upgrade</h3>
                  <div className="plan-card premium">
                    <div className="plan-header">
                      <span className="plan-icon">⭐</span>
                      <div>
                        <h4>Premium</h4>
                        <p className="plan-price">R$ 19,90/mês</p>
                      </div>
                    </div>
                    <div className="plan-features">
                      <p className="feature">✓ Perguntas ilimitadas à IA</p>
                      <p className="feature">✓ Análise avançada de builds</p>
                      <p className="feature">✓ Táticas personalizadas</p>
                      <p className="feature">✓ Suporte prioritário</p>
                      <p className="feature">✓ Acesso antecipado a novidades</p>
                    </div>
                    <button className="btn-upgrade-premium">
                      Fazer Upgrade Premium
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default UserSettings
