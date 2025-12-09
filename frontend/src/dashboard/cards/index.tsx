import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Cards.css';
import FotoPadraoImage from '../../assets/Foto_padrao.png';

interface CardFormData {
  name: string;
  version: string;
  card_type: string;
  position: string;
  overall_rating: string;
  photo_url: string;
}

function Cards() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<CardFormData>({
    name: '',
    version: '',
    card_type: '',
    position: '',
    overall_rating: '',
    photo_url: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [isVerifyingUrl, setIsVerifyingUrl] = useState(false);

  useEffect(() => {
    if (formData.photo_url) {
      setIsVerifyingUrl(true);
      setErrors(prev => ({ ...prev, photo_url: 'Verificando URL...' }));
      const img = new Image();
      img.onload = () => {
        setIsVerifyingUrl(false);
        setErrors(prev => {
          const newErrors = { ...prev };
          if (newErrors.photo_url === 'Verificando URL...' || newErrors.photo_url === 'Link inválido ou bloqueado') {
            delete newErrors.photo_url;
          }
          return newErrors;
        });
      };
      img.onerror = () => {
        setIsVerifyingUrl(false);
        setErrors(prev => ({ ...prev, photo_url: 'Link inválido ou bloqueado' }));
      };
      img.src = formData.photo_url;
    } else {
      setIsVerifyingUrl(false);
      setErrors(prev => {
        const newErrors = { ...prev };
        if (newErrors.photo_url === 'Verificando URL...' || newErrors.photo_url === 'Link inválido ou bloqueado') {
          delete newErrors.photo_url;
        }
        return newErrors;
      });
    }
  }, [formData.photo_url]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    if (errors[name] && name !== 'photo_url') {
      setErrors({ ...errors, [name]: '' });
    }
    if (name === 'photo_url') {
      setImageError(false);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = 'Nome do Jogador é obrigatório';
    if (!formData.version.trim()) newErrors.version = 'Versão é obrigatória';
    if (!formData.card_type.trim()) newErrors.card_type = 'Tipo de Carta é obrigatório';
    if (!formData.position.trim()) newErrors.position = 'Posição é obrigatória';
    if (!formData.overall_rating.trim()) newErrors.overall_rating = 'Overall Rating é obrigatório';
    if (!formData.photo_url.trim()) newErrors.photo_url = 'URL da Foto é obrigatório';
    
    // Merge with existing errors (like URL validation)
    setErrors(prev => ({ ...prev, ...newErrors }));
    return Object.keys(newErrors).length === 0 && !errors.photo_url;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(false);

    if (validateForm() && !isVerifyingUrl) {
      console.log('Form Data:', formData);
      setSuccess(true);
    }
  };

  const placeholderImg = FotoPadraoImage;
  const isSubmitDisabled = isVerifyingUrl || Object.keys(errors).some(key => errors[key] && key !== 'submit');

  return (
    <div className="cards-content">
      <div className="cards-header">
        <h1 className="cards-title">Criar Nova Carta</h1>
        <p className="cards-subtitle">Preencha os detalhes da nova carta do jogador.</p>
      </div>

      {success && (
        <div className="success-message">
          ✅ Carta salva com sucesso!
        </div>
      )}

      {errors.submit && (
        <div className="error-message">
          ❌ {errors.submit}
        </div>
      )}

      <form className="cards-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h3 className="section-title">Informações da Carta</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">Nome do Jogador *</label>
              <input type="text" id="name" name="name" value={formData.name} onChange={handleChange} placeholder="Ex: Neymar Jr." className={errors.name ? 'error' : ''} />
              {errors.name && <span className="error-text">{errors.name}</span>}
            </div>
            <div className="form-group">
                <label htmlFor="overall_rating">Overall Rating *</label>
                <input type="number" name="overall_rating" value={formData.overall_rating} onChange={handleChange} placeholder="Ex: 99" className={errors.overall_rating ? 'error' : ''} />
                {errors.overall_rating && <span className="error-text">{errors.overall_rating}</span>}
             </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="card_type">Tipo de Carta *</label>
              <input type="text" id="card_type" name="card_type" value={formData.card_type} onChange={handleChange} placeholder="Ex: Lendário" className={errors.card_type ? 'error' : ''} />
              {errors.card_type && <span className="error-text">{errors.card_type}</span>}
            </div>
            <div className="form-group">
              <label htmlFor="position">Posição *</label>
              <input type="text" id="position" name="position" value={formData.position} onChange={handleChange} placeholder="Ex: CA, PTE, SA" className={errors.position ? 'error' : ''} />
              {errors.position && <span className="error-text">{errors.position}</span>}
            </div>
          </div>
           <div className="form-row">
            <div className="form-group">
              <label htmlFor="version">Versão *</label>
              <input type="text" id="version" name="version" value={formData.version} onChange={handleChange} placeholder="Ex: Summer Stars" className={errors.version ? 'error' : ''} />
              {errors.version && <span className="error-text">{errors.version}</span>}
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="photo_url">URL da Foto *</label>
              <input type="text" id="photo_url" name="photo_url" value={formData.photo_url} onChange={handleChange} placeholder="Ex: https://example.com/image.jpg" className={errors.photo_url ? 'error' : ''} />
              <p style={{ color: '#a8a8a8', fontSize: '0.85rem', marginTop: '0.25rem' }}>
                Dica: Clique com botão direito na imagem do site e escolha 'Copiar Endereço da Imagem'.
              </p>
              {errors.photo_url && <span className="error-text">{errors.photo_url}</span>}
              <img
                src={imageError || !formData.photo_url ? placeholderImg : formData.photo_url}
                alt="Pré-visualização da Carta"
                className="card-image-preview"
                style={{ marginTop: '1rem', width: '200px', height: '200px', objectFit: 'cover', borderRadius: '8px', border: '1px solid #2a2a2a' }}
                onError={() => setImageError(true)}
              />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => navigate('/dashboard')}>
            Cancelar
          </button>
          <button type="submit" className="btn-primary" disabled={isSubmitDisabled} style={{ opacity: isSubmitDisabled ? 0.5 : 1 }}>
            {isVerifyingUrl ? 'Verificando...' : 'Salvar Carta'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default Cards;
