import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Dashboard.css';
import { cardsService, type Card } from '../../services/cardsService';

function Catalog() {
  const navigate = useNavigate();
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCards();
  }, []);

  const loadCards = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await cardsService.listCards();
      setCards(data);
    } catch (err: any) {
      console.error('Erro ao carregar cartas:', err);
      setError(err.message || 'Erro ao carregar cartas');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteCard = async (id: number) => {
    if (window.confirm('Tem certeza que deseja deletar esta carta?')) {
      try {
        await cardsService.deleteCard(id);
        setCards(cards.filter(c => c.id !== id));
      } catch (err: any) {
        alert('Erro ao deletar carta: ' + err.message);
      }
    }
  };

  const displayError = error && error.includes('1 validation error for CardResponse player_id') 
    ? 'Não foi possível carregar as cartas. Por favor, tente novamente mais tarde.' 
    : error;

  return (
    <div className="dashboard-content">
      <div className="dashboard-header">
        <h1 className="dashboard-title">Catálogo de Cartas</h1>
        <p className="dashboard-subtitle">Visualize e gerencie todas as suas cartas criadas</p>
      </div>

      <div className="builds-catalog-section">
        <div className="catalog-header">
          <div className="catalog-stats">
            <div className="catalog-stat-item">
              <span className="catalog-stat-value">{cards.length}</span>
              <span className="catalog-stat-label">Total de Cartas</span>
            </div>
          </div>
          <button className="btn-new-build" onClick={() => navigate('/dashboard/cards')}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="12" y1="5" x2="12" y2="19" strokeWidth="2" strokeLinecap="round"/>
              <line x1="5" y1="12" x2="19" y2="12" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            Nova Carta
          </button>
        </div>

        {loading ? (
          <div className="empty-state">
            <p>Carregando cartas...</p>
          </div>
        ) : displayError ? (
          <div className="empty-state">
            <p style={{ color: '#f87171' }}>{displayError}</p>
          </div>
        ) : cards.length === 0 ? (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
            <h3>Nenhuma carta criada ainda</h3>
            <p>Clique em "Nova Carta" para criar sua primeira carta personalizada</p>
          </div>
        ) : (
          <div className="cards-grid">
            {cards.map((card) => (
              <div key={card.id} className="card-item">
                {card.image_url && <img src={card.image_url} alt={card.name} className="card-image" />}
                <div className="card-info">
                  <h3>{card.name}</h3>
                  <p className="card-version">{card.version}</p>
                  <p className="card-position">{card.position}</p>
                  <p className="card-overall">Overall: {card.overall_rating}</p>
                </div>
                <div className="card-actions">
                  <button 
                    className="btn-action btn-delete" 
                    onClick={() => handleDeleteCard(card.id)}
                    title="Excluir"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <polyline points="3 6 5 6 21 6" strokeWidth="2"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" strokeWidth="2"/>
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Catalog;
