import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Builds.css'

interface BuildFormData {
  title: string
  card_id: string
  platform: string
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
  is_official_meta: boolean
  meta_content: string
}

function Builds() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState<BuildFormData>({
    title: '',
    card_id: '',
    platform: '',
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
    overall_rating: '',
    is_official_meta: false,
    meta_content: '{}'
  })

  const [errors, setErrors] = useState<Record<string, string>>({})
  const [success, setSuccess] = useState(false)

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
      newErrors.title = 'Título é obrigatório'
    }

    if (!formData.card_id.trim()) {
      newErrors.card_id = 'ID do card é obrigatório'
    }

    // Validar JSON
    if (formData.meta_content) {
      try {
        JSON.parse(formData.meta_content)
      } catch {
        newErrors.meta_content = 'JSON inválido'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSuccess(false)

    if (!validateForm()) {
      return
    }

    try {
      // Aqui você fará a integração com a API
      console.log('Build Data:', formData)
      
      // Simular sucesso
      setSuccess(true)
      setTimeout(() => {
        setSuccess(false)
      }, 3000)

    } catch (error) {
      console.error('Erro ao salvar build:', error)
    }
  }

  return (
    <div className="builds-content">
      <div className="builds-header">
        <h1 className="builds-title">Criar Nova Build</h1>
        <p className="builds-subtitle">Configure os atributos da sua build personalizada</p>
      </div>

      {success && (
        <div className="success-message">
          ✅ Build salva com sucesso!
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
              <label htmlFor="platform">Plataforma</label>
              <input
                type="text"
                id="platform"
                name="platform"
                value={formData.platform}
                onChange={handleChange}
                placeholder="Ex: PC, PlayStation, Xbox, Mobile"
              />
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

        {/* Meta Config */}
        <div className="form-section">
          <h3 className="section-title">Configuração Meta</h3>
          
          <div className="form-group checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="is_official_meta"
                checked={formData.is_official_meta}
                onChange={handleChange}
              />
              <span>Build Oficial Meta</span>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="meta_content">Meta Content (JSON)</label>
            <textarea
              id="meta_content"
              name="meta_content"
              value={formData.meta_content}
              onChange={handleChange}
              rows={6}
              placeholder='{"tactics": "4-3-3", "style": "Possession"}'
              className={errors.meta_content ? 'error' : ''}
            />
            {errors.meta_content && <span className="error-text">{errors.meta_content}</span>}
          </div>
        </div>

        {/* Botões */}
        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => navigate('/dashboard')}>
            Cancelar
          </button>
          <button type="submit" className="btn-primary">
            Salvar Build
          </button>
        </div>
      </form>
    </div>
  )
}

export default Builds
