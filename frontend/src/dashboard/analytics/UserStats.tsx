import { useState, useEffect } from 'react'
import './UserStats.css'

interface Stats {
  total_questions: number
  builds_consulted: number
  gameplay_questions: number
  favorite_position?: string
  most_searched_player?: string
  last_active: string
}

function UserStats() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        setError('Você precisa estar autenticado')
        return
      }

      const response = await fetch('http://localhost:8000/api/v1/users/stats', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Erro ao carregar estatísticas')
      }

      const data = await response.json()
      setStats(data)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar estatísticas')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="dashboard-content"><div className="stats-loading">Carregando estatísticas...</div></div>
  }

  if (error) {
    return <div className="dashboard-content"><div className="stats-error">{error}</div></div>
  }

  if (!stats) {
    return null
  }

  return (
    <div className="dashboard-content">
      <div className="user-stats">
        <h2>📊 Suas Estatísticas</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">❓</div>
          <div className="stat-value">{stats.total_questions}</div>
          <div className="stat-label">Perguntas Totais</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚽</div>
          <div className="stat-value">{stats.builds_consulted}</div>
          <div className="stat-label">Builds Consultadas</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🎮</div>
          <div className="stat-value">{stats.gameplay_questions}</div>
          <div className="stat-label">Dicas de Gameplay</div>
        </div>

        {stats.favorite_position && (
          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-value">{stats.favorite_position}</div>
            <div className="stat-label">Posição Favorita</div>
          </div>
        )}

        {stats.most_searched_player && (
          <div className="stat-card">
            <div className="stat-icon">⭐</div>
            <div className="stat-value">{stats.most_searched_player}</div>
            <div className="stat-label">Jogador Mais Buscado</div>
          </div>
        )}
      </div>

      <div className="stats-footer">
        <p>Última atividade: {new Date(stats.last_active).toLocaleString('pt-BR')}</p>
      </div>
      </div>
    </div>
  )
}

export default UserStats
