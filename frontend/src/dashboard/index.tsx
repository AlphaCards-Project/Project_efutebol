import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import './Dashboard.css'
import { buildService } from '../services/buildService'

function Dashboard() {
  const [buildsCount, setBuildsCount] = useState(0)

  useEffect(() => {
    // Carregar contagem de builds
    const loadBuildsCount = async () => {
      try {
        const builds = await buildService.getMyBuilds()
        setBuildsCount(builds.length)
      } catch (error) {
        console.error('Erro ao carregar builds:', error)
      }
    }
    
    loadBuildsCount()
  }, [])
  // Dados para os gráficos
  const barData = [
    { name: 'Jan', value: 12 },
    { name: 'Fev', value: 15 },
    { name: 'Mar', value: 8 },
    { name: 'Abr', value: 20 },
    { name: 'Mai', value: 18 },
    { name: 'Jun', value: 25 },
  ]

  const lineData = [
    { name: 'Seg', wins: 8, losses: 3 },
    { name: 'Ter', wins: 6, losses: 4 },
    { name: 'Qua', wins: 10, losses: 2 },
    { name: 'Qui', wins: 12, losses: 3 },
    { name: 'Sex', wins: 9, losses: 5 },
    { name: 'Sáb', wins: 15, losses: 2 },
    { name: 'Dom', wins: 11, losses: 4 },
  ]

  const donutData = [
    { name: 'Vitórias', value: 66.6, color: '#d4af37' },
    { name: 'Derrotas', value: 33.4, color: '#6a6a6a' },
  ]

  const recentEvents = [
    { id: 1, title: 'Build "Meta Striker PC" criada', time: '5 min atrás' },
    { id: 2, title: 'Build "Defesa Sólida" atualizada', time: '30 min atrás' },
    { id: 3, title: 'Sequência de 5 vitórias alcançada', time: '1 hora atrás' },
    { id: 4, title: 'Nova build META adicionada ao catálogo', time: '2 horas atrás' },
    { id: 5, title: 'Build "Meio-Campo Criativo" compartilhada', time: '4 horas atrás' },
  ]

  return (
    <div className="dashboard-content">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-subtitle">Bem-vindo ao painel de controle do eFutebol</p>
      </div>

      {/* Cards de Estatísticas */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🎮</div>
          <div className="stat-info">
            <h3 className="stat-value">428</h3>
            <p className="stat-label">Partidas Jogadas</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🏆</div>
          <div className="stat-info">
            <h3 className="stat-value">285</h3>
            <p className="stat-label">Vitórias</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚙️</div>
          <div className="stat-info">
            <h3 className="stat-value">{buildsCount}</h3>
            <p className="stat-label">Builds Criadas</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-info">
            <h3 className="stat-value">66.6%</h3>
            <p className="stat-label">Taxa de Vitória</p>
          </div>
        </div>
      </div>

      {/* Gráficos e Eventos */}
      <div className="dashboard-grid">
        {/* Coluna Esquerda - Gráficos */}
        <div className="charts-column">
          {/* Gráfico de Barras */}
          <div className="chart-card">
            <h3 className="chart-title">Builds Criadas por Mês</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
                <XAxis dataKey="name" stroke="#a8a8a8" />
                <YAxis stroke="#a8a8a8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #d4af37', borderRadius: '8px' }}
                  labelStyle={{ color: '#e0e0e0' }}
                />
                <Bar dataKey="value" fill="#d4af37" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Gráfico de Linha */}
          <div className="chart-card">
            <h3 className="chart-title">Desempenho Semanal</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
                <XAxis dataKey="name" stroke="#a8a8a8" />
                <YAxis stroke="#a8a8a8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #d4af37', borderRadius: '8px' }}
                  labelStyle={{ color: '#e0e0e0' }}
                />
                <Legend />
                <Line type="monotone" dataKey="wins" stroke="#d4af37" strokeWidth={2} name="Vitórias" />
                <Line type="monotone" dataKey="losses" stroke="#6a6a6a" strokeWidth={2} name="Derrotas" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Coluna Direita - Donut e Eventos */}
        <div className="sidebar-column">
          {/* Gráfico Donut */}
          <div className="chart-card">
            <h3 className="chart-title">Taxa de Vitória</h3>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={donutData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {donutData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #d4af37', borderRadius: '8px' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="donut-legend">
              {donutData.map((item) => (
                <div key={item.name} className="donut-legend-item">
                  <span className="donut-legend-color" style={{ backgroundColor: item.color }}></span>
                  <span className="donut-legend-label">{item.name}: {item.value}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Lista de Eventos */}
          <div className="events-card">
            <h3 className="chart-title">Atividades Recentes</h3>
            <div className="events-list">
              {recentEvents.map((event) => (
                <div key={event.id} className="event-item">
                  <div className="event-dot"></div>
                  <div className="event-content">
                    <p className="event-title">{event.title}</p>
                    <p className="event-time">{event.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
