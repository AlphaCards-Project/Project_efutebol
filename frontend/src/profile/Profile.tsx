import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Profile.css'

interface UserProfile {
  email: string
  full_name: string
  nickname: string
  platform: string
  is_premium: boolean
  role?: string
}

function Profile() {
  const navigate = useNavigate()
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [profileData, setProfileData] = useState<UserProfile>({
    email: '',
    full_name: '',
    nickname: '',
    platform: '',
    is_premium: false,
    role: 'free'
  })
  const [editData, setEditData] = useState<UserProfile>({
    email: '',
    full_name: '',
    nickname: '',
    platform: '',
    is_premium: false,
    role: 'free'
  })

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        navigate('/login')
        return
      }

      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem('token')
          navigate('/login')
          return
        }
        throw new Error('Erro ao carregar perfil')
      }

      const userData = await response.json()
      const mappedData: UserProfile = {
        email: userData.email,
        full_name: userData.name || '',
        nickname: userData.nickname || '',
        platform: userData.platform || '',
        is_premium: userData.is_premium,
        role: userData.role || 'free'
      }
      
      setProfileData(mappedData)
      setEditData(mappedData)
    } catch (err) {
      setError('Erro ao carregar perfil')
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setEditData({
      ...editData,
      [e.target.name]: e.target.value
    })
  }

  const handleSave = async () => {
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const token = localStorage.getItem('token')
      if (!token) {
        navigate('/login')
        return
      }

      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          full_name: editData.full_name,
          nickname: editData.nickname,
          platform: editData.platform
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Erro ao atualizar perfil')
      }

      const updatedUser = await response.json()
      const mappedData: UserProfile = {
        email: updatedUser.email,
        full_name: updatedUser.name || '',
        nickname: updatedUser.nickname || '',
        platform: updatedUser.platform || '',
        is_premium: updatedUser.is_premium,
        role: updatedUser.role || 'free'
      }
      
      setProfileData(mappedData)
      setIsEditing(false)
      setSuccess('Perfil atualizado com sucesso!')
      
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError(err.message || 'Erro ao atualizar perfil')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    setEditData(profileData)
    setIsEditing(false)
    setError('')
  }

  return (
    <div className="profile-container">
      <button className="btn-back" onClick={() => navigate('/chat')} title="Voltar ao Chat">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M19 12H5M12 19l-7-7 7-7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      <div className="profile-box">
        <div className="profile-header">
          <div className="profile-avatar-large">
            {profileData.full_name?.[0]?.toUpperCase() || 'U'}
          </div>
          <h1 className="profile-title">{profileData.full_name}</h1>
          <p className="profile-subtitle">
            {profileData.role === 'admin' 
              ? '👑 Administrador' 
              : profileData.role === 'premium' 
                ? '⭐ Conta Premium' 
                : '🎮 Conta Grátis'}
          </p>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <div className="profile-form">
          <div className="form-group">
            <label htmlFor="full_name">Nome Completo</label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              value={editData.full_name}
              onChange={handleChange}
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
              onChange={handleChange}
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
              onChange={handleChange}
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
              onChange={handleChange}
              disabled={!isEditing}
              className={!isEditing ? 'disabled' : ''}
            >
              <option value="PC">PC</option>
              <option value="PlayStation">PlayStation</option>
              <option value="Xbox">Xbox</option>
              <option value="Mobile">Mobile</option>
            </select>
          </div>

          <div className="profile-actions">
            {!isEditing ? (
              <>
                <button className="btn-edit" onClick={() => setIsEditing(true)}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" strokeWidth="2"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" strokeWidth="2"/>
                  </svg>
                  Editar Perfil
                </button>
                {profileData.role === 'free' && (
                  <button className="btn-upgrade">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" strokeWidth="2"/>
                    </svg>
                    Fazer Upgrade Premium
                  </button>
                )}
              </>
            ) : (
              <>
                <button 
                  className="btn-cancel" 
                  onClick={handleCancel}
                  disabled={loading}
                >
                  Cancelar
                </button>
                <button 
                  className="btn-save" 
                  onClick={handleSave}
                  disabled={loading}
                >
                  {loading ? 'Salvando...' : 'Salvar Alterações'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
