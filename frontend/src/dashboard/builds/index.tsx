import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Builds.css'
import { buildService, type BuildCreate } from '../../services/buildService'
import { cardsService, type Card } from '../../services/cardsService'

interface BuildFormData {
  title: string
  card_id: string
  shooting: string
  passing: string
  dribbling: string
  dexterity: string
  lower_body_strength: string
  aerial_strength: string
  defending: string
  gk_1: string
  gk_2: string
  gk_3: string
  overall_rating: string
}

function Builds() {
  const navigate = useNavigate()
  const [step, setStep] = useState<'select-card' | 'create-card' | 'create-build'>('select-card')
  const [cards, setCards] = useState<Card[]>([])
  const [selectedCard, setSelectedCard] = useState<Card | null>(null)
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  
  const [formData, setFormData] = useState<BuildFormData>({
    title: '',
    card_id: '',
    shooting: '',
    passing: '',
    dribbling: '',
    dexterity: '',
    lower_body_strength: '',
    aerial_strength: '',
    defending: '',
    gk_1: '',
    gk_2: '',
    gk_3: '',
    overall_rating: ''
  })

  const [errors, setErrors] = useState<Record<string, string>>({})
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    loadCards()
  }, [])

  const loadCards = async () => {
    try {
      setLoading(true)
      const data = await cardsService.listCards({ limit: 100 })
      setCards(data)
    } catch (error) {
      console.error('Erro ao carregar cartas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCardSelect = (card: Card) => {
    setSelectedCard(card)
    setFormData({ ...formData, card_id: card.id.toString(), title: card.name })
    setStep('create-build')
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    const checked = (e.target as HTMLInputElement).checked

    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    })
    
    // Limpa erro do campo
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' })
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.title.trim()) {
      newErrors.title = 'Nome do Jogador é obrigatório'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSuccess(false)
    setErrors({})

    if (!validateForm()) {
      return
    }

    if (!formData.card_id) {
      setErrors({ card_id: 'Selecione uma carta primeiro' })
      return
    }

    try {
      setLoading(true)
      
      const buildData: BuildCreate = {
        card_id: parseInt(formData.card_id),
        title: formData.title,
        shooting: parseInt(formData.shooting) || 0,
        passing: parseInt(formData.passing) || 0,
        dribbling: parseInt(formData.dribbling) || 0,
        dexterity: parseInt(formData.dexterity) || 0,
        lower_body_strength: parseInt(formData.lower_body_strength) || 0,
        aerial_strength: parseInt(formData.aerial_strength) || 0,
        defending: parseInt(formData.defending) || 0,
        gk_1: parseInt(formData.gk_1) || 0,
        gk_2: parseInt(formData.gk_2) || 0,
        gk_3: parseInt(formData.gk_3) || 0,
        is_official_meta: false
      }

      // Calcular overall se não fornecido
      if (formData.overall_rating) {
        buildData.overall_rating = parseInt(formData.overall_rating)
      }

      const createdBuild = await buildService.createBuild(buildData)
      console.log('Build criada com sucesso:', createdBuild)
      
      setSuccess(true)
      alert('✅ Build criada com sucesso!')
      
      setTimeout(() => {
        navigate('/dashboard/catalog')
      }, 1500)

    } catch (error: any) {
      console.error('Erro ao salvar build:', error)
      setErrors({ submit: error.message || 'Erro ao salvar build. Tente novamente.' })
    } finally {
      setLoading(false)
    }
  }

  const filteredCards = cards.filter(card => 
    card.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (step === 'select-card') {
    return (
      <div className="builds-content">
        <div className="builds-header">
          <h1 className="builds-title">Selecionar Carta</h1>
          <p className="builds-subtitle">Escolha uma carta para criar sua build</p>
        </div>

        <div className="card-selection">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Buscar carta..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>

          {loading ? (
            <div className="loading">Carregando cartas...</div>
          ) : (
            <div className="cards-grid">
              {filteredCards.map((card) => (
                <div key={card.id} className="card-item" onClick={() => handleCardSelect(card)}>
                  {card.image_url && (
                    <img src={card.image_url} alt={card.name} className="card-image" />
                  )}
                  <div className="card-info">
                    <h3>{card.name}</h3>
                    <p className="card-version">{card.version}</p>
                    <p className="card-position">{card.position}</p>
                    <p className="card-overall">Overall: {card.overall_rating}</p>
                  </div>
                </div>
              ))}
              {filteredCards.length === 0 && (
                <p className="no-results">Nenhuma carta encontrada</p>
              )}
            </div>
          )}

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => navigate('/dashboard')}>
              Voltar
            </button>
            <button type="button" className="btn-primary" onClick={() => setStep('create-card')}>
              Criar Nova Carta
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="builds-content">
      <div className="builds-header">
        <h1 className="builds-title">Criar Nova Build</h1>
        <p className="builds-subtitle">
          {selectedCard ? `Build para: ${selectedCard.name}` : 'Configure os atributos da sua build'}
        </p>
      </div>

      {success && (
        <div className="success-message">
          ✅ Build salva com sucesso! Redirecionando...
        </div>
      )}

      {errors.submit && (
        <div className="error-message">
          ❌ {errors.submit}
        </div>
      )}

      <form className="builds-form" onSubmit={handleSubmit}>
        {/* Informações Básicas */}
        <div className="form-section">
          <h3 className="section-title">Informações Básicas</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="title">Nome do Jogador *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Ex: Lionel Messi"
                className={errors.title ? 'error' : ''}
              />
              {errors.title && <span className="error-text">{errors.title}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="overall_rating">Overall Rating</label>
              <input
                type="text"
                id="overall_rating"
                name="overall_rating"
                value={formData.overall_rating}
                onChange={handleChange}
                placeholder="Ex: 85"
              />
            </div>
          </div>
        </div>

        {/* Atributos de Campo */}
        <div className="form-section">
          <h3 className="section-title">Atributos de Campo (0-99)</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="shooting">Shooting</label>
              <input
                type="text"
                id="shooting"
                name="shooting"
                value={formData.shooting}
                onChange={handleChange}
                placeholder="Ex: 85"
                className={errors.shooting ? 'error' : ''}
              />
              {errors.shooting && <span className="error-text">{errors.shooting}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="passing">Passing</label>
              <input
                type="text"
                id="passing"
                name="passing"
                value={formData.passing}
                onChange={handleChange}
                placeholder="Ex: 80"
                className={errors.passing ? 'error' : ''}
              />
              {errors.passing && <span className="error-text">{errors.passing}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="dribbling">Dribbling</label>
              <input
                type="text"
                id="dribbling"
                name="dribbling"
                value={formData.dribbling}
                onChange={handleChange}
                placeholder="Ex: 90"
                className={errors.dribbling ? 'error' : ''}
              />
              {errors.dribbling && <span className="error-text">{errors.dribbling}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="dexterity">Dexterity</label>
              <input
                type="text"
                id="dexterity"
                name="dexterity"
                value={formData.dexterity}
                onChange={handleChange}
                placeholder="Ex: 75"
                className={errors.dexterity ? 'error' : ''}
              />
              {errors.dexterity && <span className="error-text">{errors.dexterity}</span>}
            </div>
          </div>
        </div>

        {/* Atributos Físicos */}
        <div className="form-section">
          <h3 className="section-title">Atributos Físicos (0-99)</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="lower_body_strength">Lower Body Strength</label>
              <input
                type="text"
                id="lower_body_strength"
                name="lower_body_strength"
                value={formData.lower_body_strength}
                onChange={handleChange}
                placeholder="Ex: 80"
                className={errors.lower_body_strength ? 'error' : ''}
              />
              {errors.lower_body_strength && <span className="error-text">{errors.lower_body_strength}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="aerial_strength">Aerial Strength</label>
              <input
                type="text"
                id="aerial_strength"
                name="aerial_strength"
                value={formData.aerial_strength}
                onChange={handleChange}
                placeholder="Ex: 85"
                className={errors.aerial_strength ? 'error' : ''}
              />
              {errors.aerial_strength && <span className="error-text">{errors.aerial_strength}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="defending">Defending</label>
              <input
                type="text"
                id="defending"
                name="defending"
                value={formData.defending}
                onChange={handleChange}
                placeholder="Ex: 70"
                className={errors.defending ? 'error' : ''}
              />
              {errors.defending && <span className="error-text">{errors.defending}</span>}
            </div>
          </div>
        </div>

        {/* Atributos de Goleiro */}
        <div className="form-section">
          <h3 className="section-title">Atributos de Goleiro (0-99)</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="gk_1">GK 1</label>
              <input
                type="text"
                id="gk_1"
                name="gk_1"
                value={formData.gk_1}
                onChange={handleChange}
                placeholder="Ex: 80"
                className={errors.gk_1 ? 'error' : ''}
              />
              {errors.gk_1 && <span className="error-text">{errors.gk_1}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="gk_2">GK 2</label>
              <input
                type="text"
                id="gk_2"
                name="gk_2"
                value={formData.gk_2}
                onChange={handleChange}
                placeholder="Ex: 75"
                className={errors.gk_2 ? 'error' : ''}
              />
              {errors.gk_2 && <span className="error-text">{errors.gk_2}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="gk_3">GK 3</label>
              <input
                type="text"
                id="gk_3"
                name="gk_3"
                value={formData.gk_3}
                onChange={handleChange}
                placeholder="Ex: 70"
                className={errors.gk_3 ? 'error' : ''}
              />
              {errors.gk_3 && <span className="error-text">{errors.gk_3}</span>}
            </div>
          </div>
        </div>

        {/* Botões */}
        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => setStep('select-card')}>
            Voltar
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Salvando...' : 'Salvar Build'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Builds
