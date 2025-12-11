import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Login.css'

function Login() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Aqui você fará a integração com a API
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password
        })
      })

      if (!response.ok) {
        throw new Error('Credenciais inválidas')
      }

      const data = await response.json()
      console.log('🔐 Resposta do login:', data)
      console.log('👤 Dados do usuário:', data.user)
      console.log('🎭 Role do usuário:', data.user?.role)
      
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      console.log('💾 Dados salvos no localStorage:', {
        token: data.access_token.substring(0, 20) + '...',
        user: JSON.parse(localStorage.getItem('user') || '{}')
      })
      
      navigate('/chat')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer login')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <button className="btn-back" onClick={() => navigate('/')} title="Voltar">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M19 12H5M12 19l-7-7 7-7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
      <div className="login-box">
        <div className="login-header">
          <div className="login-logo">
            <span className="logo-icon">⚽</span>
            <span className="logo-text">eFutebol</span>
          </div>
          <h1 className="login-title">Bem-vindo de volta</h1>
          <p className="login-subtitle">Entre com sua conta para continuar</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="email">E-mail</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="seu@email.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </div>

          <div className="form-footer">
            <a href="#" className="forgot-password">Esqueceu a senha?</a>
          </div>

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <div className="login-divider">
          <span>ou</span>
        </div>

        <div className="login-register">
          <p>Não tem uma conta?</p>
          <button onClick={() => navigate('/registro')} className="btn-register">
            Cadastre-se gratuitamente
          </button>
        </div>
      </div>
    </div>
  )
}

export default Login
