import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Jogador.css';

interface PlayerFormData {
  name: string;
  nationality: string;
}

function Jogador() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<PlayerFormData>({
    name: '',
    nationality: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = 'Nome do Jogador é obrigatório';
    if (!formData.nationality.trim()) newErrors.nationality = 'Nacionalidade é obrigatória';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(false);

    if (validateForm()) {
      console.log('Form Data:', formData);
      setSuccess(true);
      // Here you would typically send the data to a server
      // For now, we'll just log it and show a success message.
    }
  };

  return (
    <div className="jogador-content">
      <div className="jogador-header">
        <h1 className="jogador-title">Criar Novo Jogador</h1>
        <p className="jogador-subtitle">Preencha os detalhes do novo jogador.</p>
      </div>

      {success && (
        <div className="success-message">
          ✅ Jogador salvo com sucesso!
        </div>
      )}

      {errors.submit && (
        <div className="error-message">
          ❌ {errors.submit}
        </div>
      )}

      <form className="jogador-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h3 className="section-title">Informações do Jogador</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">Nome do Jogador *</label>
              <input type="text" id="name" name="name" value={formData.name} onChange={handleChange} placeholder="Ex: Neymar Jr." className={errors.name ? 'error' : ''} />
              {errors.name && <span className="error-text">{errors.name}</span>}
            </div>
            <div className="form-group">
              <label htmlFor="nationality">Nacionalidade *</label>
              <input type="text" id="nationality" name="nationality" value={formData.nationality} onChange={handleChange} placeholder="Ex: Brasil" className={errors.nationality ? 'error' : ''} />
              {errors.nationality && <span className="error-text">{errors.nationality}</span>}
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => navigate('/dashboard')}>
            Cancelar
          </button>
          <button type="submit" className="btn-primary">
            Salvar Jogador
          </button>
        </div>
      </form>
    </div>
  );
}

export default Jogador;
