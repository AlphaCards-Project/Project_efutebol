import { useState, useEffect } from 'react'
import { cardsService, type Card, type CardCreate } from '../../services/cardsService'
import { playersService, type Player } from '../../services/playersService'
import './Admin.css'

function CardsManager() {
  const [cards, setCards] = useState<Card[]>([])
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState<CardCreate>({
    player_id: 0,
    name: '',
    version: '',
    card_type: '',
    position: '',
    overall_rating: 0,
    image_url: ''
  })

  useEffect(() => {
    loadCards()
    loadPlayers()
  }, [])

  const loadCards = async () => {
    try {
      setLoading(true)
      const data = await cardsService.listCards({ limit: 100 })
      setCards(data)
    } catch (error: any) {
      console.error('Erro ao carregar cartas:', error)
      alert('Erro ao carregar cartas: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const loadPlayers = async () => {
    try {
      const data = await playersService.listPlayers({ limit: 100 })
      setPlayers(data)
    } catch (error: any) {
      console.error('Erro ao carregar jogadores:', error)
    }
  }

  const handleSearch = async () => {
    try {
      setLoading(true)
      const data = await cardsService.listCards({ 
        search: searchTerm,
        limit: 100 
      })
      setCards(data)
    } catch (error: any) {
      console.error('Erro ao buscar cartas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateCard = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await cardsService.createCard(formData)
      setFormData({
        player_id: 0,
        name: '',
        version: '',
        card_type: '',
        position: '',
        overall_rating: 0,
        image_url: ''
      })
      setShowCreateForm(false)
      loadCards()
      alert('Carta criada com sucesso!')
    } catch (error: any) {
      alert('Erro ao criar carta: ' + error.message)
    }
  }

  const handleDeleteCard = async (cardId: number) => {
    if (window.confirm('Tem certeza que deseja deletar esta carta?')) {
      try {
        await cardsService.deleteCard(cardId)
        loadCards()
      } catch (error: any) {
        alert('Erro ao deletar carta: ' + error.message)
      }
    }
  }

  return (
    <div className="admin-content">
      <div className="admin-header">
        <h1>Gerenciar Cartas</h1>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancelar' : 'Nova Carta'}
        </button>
      </div>

      {showCreateForm && (
        <form className="create-form" onSubmit={handleCreateCard}>
          <h2>Criar Nova Carta</h2>
          <div className="form-row">
            <div className="form-group">
              <label>Jogador *</label>
              <select
                value={formData.player_id}
                onChange={(e) => setFormData({ ...formData, player_id: parseInt(e.target.value) })}
                required
              >
                <option value={0}>Selecione um jogador</option>
                {players.map((player) => (
                  <option key={player.id} value={player.id}>
                    {player.name} ({player.nationality})
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Nome da Carta *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Ex: Messi TOTY 2024"
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Versão *</label>
              <input
                type="text"
                value={formData.version}
                onChange={(e) => setFormData({ ...formData, version: e.target.value })}
                placeholder="Ex: TOTY, Base, Icon"
                required
              />
            </div>
            <div className="form-group">
              <label>Tipo *</label>
              <input
                type="text"
                value={formData.card_type}
                onChange={(e) => setFormData({ ...formData, card_type: e.target.value })}
                placeholder="Ex: Legend, Featured, Standard"
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Posição *</label>
              <input
                type="text"
                value={formData.position}
                onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                placeholder="Ex: RWF, CF, AMF"
                required
              />
            </div>
            <div className="form-group">
              <label>Overall *</label>
              <input
                type="number"
                value={formData.overall_rating}
                onChange={(e) => setFormData({ ...formData, overall_rating: parseInt(e.target.value) })}
                placeholder="Ex: 98"
                min="0"
                max="99"
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label>URL da Imagem</label>
            <input
              type="text"
              value={formData.image_url}
              onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
              placeholder="https://..."
            />
          </div>
          <button type="submit" className="btn-primary">Criar Carta</button>
        </form>
      )}

      <div className="search-section">
        <input
          type="text"
          className="search-input"
          placeholder="Buscar carta..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button className="btn-primary" onClick={handleSearch}>Buscar</button>
      </div>

      {loading ? (
        <div className="loading">Carregando...</div>
      ) : (
        <div className="cards-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Versão</th>
                <th>Tipo</th>
                <th>Posição</th>
                <th>Overall</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {cards.map((card) => (
                <tr key={card.id}>
                  <td>{card.id}</td>
                  <td>{card.name}</td>
                  <td>{card.version}</td>
                  <td>{card.card_type}</td>
                  <td>{card.position}</td>
                  <td>{card.overall_rating}</td>
                  <td>
                    <button
                      className="btn-delete"
                      onClick={() => handleDeleteCard(card.id)}
                    >
                      Deletar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {cards.length === 0 && (
            <p className="no-results">Nenhuma carta encontrada</p>
          )}
        </div>
      )}
    </div>
  )
}

export default CardsManager
