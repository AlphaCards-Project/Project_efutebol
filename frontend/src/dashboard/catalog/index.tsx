import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../Dashboard.css'
import { buildService, type Build } from '../../services/buildService'

function Catalog() {
  const navigate = useNavigate()
  const [builds, setBuilds] = useState<Build[]>([])

  useEffect(() => {
    // Carregar builds
    loadBuilds()

    // Inscrever-se para mudanças
    const unsubscribe = buildService.subscribe((updatedBuilds) => {
      setBuilds(updatedBuilds)
    })

    // Debug: verificar localStorage
    console.log('Builds do localStorage:', localStorage.getItem('user_builds'))
    console.log('Builds carregadas:', buildService.getBuilds())

    return () => unsubscribe()
  }, [])

  const loadBuilds = () => {
    const userBuilds = buildService.getBuilds()
    setBuilds(userBuilds)
  }

  const handleDeleteBuild = (id: string) => {
    if (window.confirm('Tem certeza que deseja deletar esta build?')) {
      buildService.deleteBuild(id)
      loadBuilds()
    }
  }

  const createTestBuild = () => {
    console.log('Criando build de teste...')
    const testBuild = buildService.createBuild({
      title: 'Build Teste',
      card_id: '1001',
      platform: 'PC',
      shooting: 85,
      passing: 80,
      dribbling: 90,
      dexterity: 75,
      lower_body_strength: 80,
      aerial_strength: 85,
      defending: 70,
      gk_1: 50,
      gk_2: 50,
      gk_3: 50,
      overall_rating: 80,
      is_official_meta: false,
      meta_content: '{}'
    })
    console.log('Build criada:', testBuild)
    console.log('Total de builds agora:', buildService.getBuilds().length)
    loadBuilds()
  }

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
              <span className="catalog-stat-value">{builds.filter(b => b.is_official_meta).length}</span>
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

        {builds.length === 0 ? (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
            <h3>Nenhuma build criada ainda</h3>
            <p>Clique em "Nova Build" para criar sua primeira build personalizada</p>
            <button onClick={createTestBuild} style={{ marginTop: '1rem', padding: '0.5rem 1rem', cursor: 'pointer' }}>
              [TESTE] Criar Build de Exemplo
            </button>
          </div>
        ) : (
          <div className="builds-grid">
            {builds.map((build) => (
              <div key={build.id} className="build-card">
                <div className="build-card-header">
                  <h3 className="build-card-title">{build.title}</h3>
                  <div className="build-card-badges">
                    {build.is_official_meta && (
                      <span className="build-meta-badge">⭐ META</span>
                    )}
                    <span className="build-platform-badge">{build.platform}</span>
                  </div>
                </div>

                <div className="build-overall">
                  <div className="overall-circle">
                    <span className="overall-value">{build.overall_rating}</span>
                  </div>
                  <span className="overall-label">Overall</span>
                </div>

                <div className="build-stats">
                  <div className="stat-row">
                    <span className="stat-icon-small">⚽</span>
                    <span className="stat-label">Shooting</span>
                    <div className="stat-bar">
                      <div className="stat-fill" style={{ width: `${build.shooting}%` }}></div>
                    </div>
                    <span className="stat-value">{build.shooting}</span>
                  </div>

                  <div className="stat-row">
                    <span className="stat-icon-small">🎯</span>
                    <span className="stat-label">Passing</span>
                    <div className="stat-bar">
                      <div className="stat-fill" style={{ width: `${build.passing}%` }}></div>
                    </div>
                    <span className="stat-value">{build.passing}</span>
                  </div>

                  <div className="stat-row">
                    <span className="stat-icon-small">⚡</span>
                    <span className="stat-label">Dribbling</span>
                    <div className="stat-bar">
                      <div className="stat-fill" style={{ width: `${build.dribbling}%` }}></div>
                    </div>
                    <span className="stat-value">{build.dribbling}</span>
                  </div>

                  {/* Add more stats here */}
                  <div className="stat-row">
                    <span className="stat-icon-small">🤸</span>
                    <span className="stat-label">Dexterity</span>
                    <div className="stat-bar">
                      <div className="stat-fill" style={{ width: `${build.dexterity}%` }}></div>
                    </div>
                    <span className="stat-value">{build.dexterity}</span>
                  </div>
                  <div className="stat-row">
                    <span className="stat-icon-small">🦵</span>
                    <span className="stat-label">Lower Body</span>
                    <div className="stat-bar">
                      <div className="stat-fill" style={{ width: `${build.lower_body_strength}%` }}></div>
                    </div>
                    <span className="stat-value">{build.lower_body_strength}</span>
                  </div>
                  <div className="stat-row">
                    <span className="stat-icon-small">🛡️</span>
                    <span className="stat-label">Defending</span>
                    <div className="stat-bar">
                      <div className="stat-fill" style={{ width: `${build.defending}%` }}></div>
                    </div>
                    <span className="stat-value">{build.defending}</span>
                  </div>
                </div>

                <div className="build-card-footer">
                  <span className="build-date">
                    Criada em {new Date(build.created_at).toLocaleDateString('pt-BR')}
                  </span>
                  <div className="build-actions">
                    <button 
                      className="btn-action btn-delete" 
                      onClick={() => handleDeleteBuild(build.id)}
                      title="Excluir"
                    >
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
        )}
      </div>
    </div>
  )
}

export default Catalog
