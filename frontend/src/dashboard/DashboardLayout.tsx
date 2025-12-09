import { useState } from 'react'
import { useNavigate, Outlet, useLocation } from 'react-router-dom'
import './Dashboard.css'

function DashboardLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  const menuItems = [
    { name: 'Home', icon: '🏠', path: '/dashboard' },
    { name: 'Cartas', icon: '🃏', path: '/dashboard/cards' },
    { name: 'Builds', icon: '⚙️', path: '/dashboard/builds' },
    { name: 'Catálogo', icon: '📚', path: '/dashboard/catalog' },
    { name: 'Analytics', icon: '📊', path: '/dashboard/analytics' },
    { name: 'Settings', icon: '🔧', path: '/dashboard/settings' },
  ]

  const isActive = (path: string) => {
    if (path === '/dashboard') {
      return location.pathname === '/dashboard'
    }
    return location.pathname.startsWith(path)
  }

  return (
    <div className="dashboard-container">
      {/* Sidebar da Dashboard */}
      <aside className={`dashboard-sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="dashboard-sidebar-header">
          <div className="dashboard-logo">
            <span className="dashboard-logo-icon">⚽</span>
            {!sidebarCollapsed && <span className="dashboard-logo-text">eFutebol</span>}
          </div>
          <button 
            className="dashboard-sidebar-toggle" 
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            title={sidebarCollapsed ? 'Expandir' : 'Ocultar'}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" strokeWidth="2"/>
              <line x1="9" y1="3" x2="9" y2="21" strokeWidth="2"/>
            </svg>
          </button>
        </div>

        <nav className="dashboard-nav">
          {menuItems.map((item) => (
            <button
              key={item.path}
              className={`dashboard-nav-item ${isActive(item.path) ? 'active' : ''}`}
              onClick={() => navigate(item.path)}
            >
              <span className="nav-icon">{item.icon}</span>
              {!sidebarCollapsed && <span className="nav-label">{item.name}</span>}
            </button>
          ))}
        </nav>

        <div className="dashboard-sidebar-footer">
          <button className="dashboard-nav-item" onClick={() => navigate('/')}>
            <span className="nav-icon">👈</span>
            {!sidebarCollapsed && <span className="nav-label">Voltar ao Chat</span>}
          </button>
        </div>
      </aside>

      {/* Conteúdo Principal */}
      <div className={`dashboard-main ${sidebarCollapsed ? 'expanded' : ''}`}>
        <Outlet />
      </div>
    </div>
  )
}

export default DashboardLayout
