import { useState, useEffect } from 'react'
import { playersService, type Player, type PlayerCreate } from '../../services/playersService'
import './Admin.css'

function PlayersManager() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState<PlayerCreate>({
    name: '',
    nationality: ''
  })

  useEffect(() => {
    loadPlayers()
  }, [])

  const loadPlayers = async () => {
    try {
      setLoading(true)
      const data = await playersService.listPlayers({ limit: 100 })
      setPlayers(data)
    } catch (error: any) {
      console.error('Erro ao carregar jogadores:', error)
      alert('Erro ao carregar jogadores: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    try {
      setLoading(true)
      const data = await playersService.listPlayers({ 
        search: searchTerm,
        limit: 100 
      })
      setPlayers(data)
    } catch (error: any) {
      console.error('Erro ao buscar jogadores:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePlayer = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await playersService.createPlayer(formData)
      setFormData({ name: '', nationality: '' })
      setShowCreateForm(false)
      loadPlayers()
      alert('Jogador criado com sucesso!')
    } catch (error: any) {
      alert('Erro ao criar jogador: ' + error.message)
    }
  }

  const handleDeletePlayer = async (playerId: number) => {
    if (window.confirm('Tem certeza que deseja deletar este jogador?')) {
      try {
        await playersService.deletePlayer(playerId)
        loadPlayers()
      } catch (error: any) {
        alert('Erro ao deletar jogador: ' + error.message)
      }
    }
  }

  return (
    <div className="admin-content">
      <div className="admin-header">
        <h1>Gerenciar Jogadores</h1>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancelar' : 'Novo Jogador'}
        </button>
      </div>

      {showCreateForm && (
        <form className="create-form" onSubmit={handleCreatePlayer}>
          <h2>Criar Novo Jogador</h2>
          <div className="form-row">
            <div className="form-group">
              <label>Nome do Jogador *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Ex: Lionel Messi"
                required
              />
            </div>
            <div className="form-group">
              <label>Nacionalidade *</label>
              <input
                type="text"
                value={formData.nationality}
                onChange={(e) => setFormData({ ...formData, nationality: e.target.value })}
                placeholder="Ex: Argentina"
                required
              />
            </div>
          </div>
          <button type="submit" className="btn-primary">Criar Jogador</button>
        </form>
      )}

      <div className="search-section">
        <input
          type="text"
          className="search-input"
          placeholder="Buscar jogador..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button className="btn-primary" onClick={handleSearch}>Buscar</button>
      </div>

      {loading ? (
        <div className="loading">Carregando...</div>
      ) : (
        <div className="players-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Nacionalidade</th>
                <th>Criado em</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {players.map((player) => (
                <tr key={player.id}>
                  <td>{player.id}</td>
                  <td>{player.name}</td>
                  <td>{player.nationality}</td>
                  <td>{new Date(player.created_at).toLocaleDateString('pt-BR')}</td>
                  <td>
                    <button
                      className="btn-delete"
                      onClick={() => handleDeletePlayer(player.id)}
                    >
                      Deletar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {players.length === 0 && (
            <p className="no-results">Nenhum jogador encontrado</p>
          )}
        </div>
      )}
    </div>
  )
}

export default PlayersManager
