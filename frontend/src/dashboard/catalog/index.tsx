import { useNavigate } from 'react-router-dom'
import '../Dashboard.css'

function Catalog() {
  const navigate = useNavigate()

  // Catálogo de Builds
  const builds = [
    {
      id: 1,
      title: 'Meta Striker',
      overall: 92,
      shooting: 95,
      passing: 85,
      dribbling: 90,
      cardId: 1001,
      isOfficialMeta: true,
      createdAt: '2024-12-05'
    },
    {
      id: 2,
      title: 'Defensive Wall',
      overall: 88,
      shooting: 65,
      passing: 80,
      dribbling: 70,
      cardId: 1002,
      isOfficialMeta: false,
      createdAt: '2024-12-04'
    },
    {
      id: 3,
      title: 'Midfield Master',
      overall: 90,
      shooting: 80,
      passing: 95,
      dribbling: 88,
      cardId: 1003,
      isOfficialMeta: true,
      createdAt: '2024-12-03'
    },
    {
      id: 4,
      title: 'Speed Demon',
      overall: 89,
      shooting: 85,
      passing: 75,
      dribbling: 95,
      cardId: 1004,
      isOfficialMeta: false,
      createdAt: '2024-12-02'
    },
    {
      id: 5,
      title: 'Goalkeeper Pro',
      overall: 91,
      shooting: 50,
      passing: 70,
      dribbling: 60,
      cardId: 1005,
      isOfficialMeta: true,
      createdAt: '2024-12-01'
    },
    {
      id: 6,
      title: 'All-Rounder',
      overall: 87,
      shooting: 82,
      passing: 85,
      dribbling: 83,
      cardId: 1006,
      isOfficialMeta: false,
      createdAt: '2024-11-30'
    },
  ]

  return (
    <div className="dashboard-content">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Catálogo de Builds</h1>
        <p className="dashboard-subtitle">Visualize e gerencie todas as suas builds criadas</p>
      </div>

      {/* Catálogo de Builds */}
      <div className="builds-catalog-section">
        <div className="catalog-header">
          <div className="catalog-stats">
            <div className="catalog-stat-item">
              <span className="catalog-stat-value">{builds.length}</span>
              <span className="catalog-stat-label">Total de Builds</span>
            </div>
            <div className="catalog-stat-item">
              <span className="catalog-stat-value">{builds.filter(b => b.isOfficialMeta).length}</span>
              <span className="catalog-stat-label">Builds META</span>
            </div>
          </div>
          <button className="btn-new-build" onClick={() => navigate('/dashboard/builds')}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="12" y1="5" x2="12" y2="19" strokeWidth="2" strokeLinecap="round"/>
              <line x1="5" y1="12" x2="19" y2="12" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            Nova Build
          </button>
        </div>

        <div className="builds-grid">
          {builds.map((build) => (
            <div key={build.id} className="build-card">
              <div className="build-card-header">
                <h3 className="build-card-title">{build.title}</h3>
                {build.isOfficialMeta && (
                  <span className="build-meta-badge">⭐ META</span>
                )}
              </div>

              <div className="build-overall">
                <div className="overall-circle">
                  <span className="overall-value">{build.overall}</span>
                </div>
                <span className="overall-label">Overall</span>
              </div>

              <div className="build-stats">
                <div className="stat-row">
                  <span className="stat-label">⚽ Shooting</span>
                  <div className="stat-bar">
                    <div className="stat-fill" style={{ width: `${build.shooting}%` }}></div>
                  </div>
                  <span className="stat-value">{build.shooting}</span>
                </div>

                <div className="stat-row">
                  <span className="stat-label">🎯 Passing</span>
                  <div className="stat-bar">
                    <div className="stat-fill" style={{ width: `${build.passing}%` }}></div>
                  </div>
                  <span className="stat-value">{build.passing}</span>
                </div>

                <div className="stat-row">
                  <span className="stat-label">⚡ Dribbling</span>
                  <div className="stat-bar">
                    <div className="stat-fill" style={{ width: `${build.dribbling}%` }}></div>
                  </div>
                  <span className="stat-value">{build.dribbling}</span>
                </div>
              </div>

              <div className="build-card-footer">
                <span className="build-date">
                  Criada em {new Date(build.createdAt).toLocaleDateString('pt-BR')}
                </span>
                <div className="build-actions">
                  <button className="btn-action" title="Editar">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" strokeWidth="2"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" strokeWidth="2"/>
                    </svg>
                  </button>
                  <button className="btn-action btn-delete" title="Excluir">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <polyline points="3 6 5 6 21 6" strokeWidth="2"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" strokeWidth="2"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Catalog
