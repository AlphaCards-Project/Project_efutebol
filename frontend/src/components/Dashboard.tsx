import { useAuth } from '../contexts/AuthContext';
import './Auth/Auth.css';

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="dashboard-title">
          <h1>eFootball Assistant</h1>
          <p>Dashboard</p>
        </div>
        <div className="user-info">
          <p>
            <strong>Usuário:</strong> {user?.name || user?.email}
          </p>
          {user?.nickname && (
            <p>
              <strong>Nickname:</strong> {user.nickname}
            </p>
          )}
          <p>
            <strong>Premium:</strong> {user?.is_premium ? 'Sim' : 'Não'}
          </p>
          <button onClick={logout} className="btn-logout">
            Sair
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <h2>Bem-vindo ao eFootball Assistant! 🎮</h2>
        <p>
          Sua conta foi criada com sucesso. Em breve você terá acesso a:
        </p>
        <ul style={{ color: '#cccccc', lineHeight: '1.8' }}>
          <li>Consultoria de builds de jogadores com IA</li>
          <li>Dicas de gameplay personalizadas</li>
          <li>Base de conhecimento do eFootball</li>
          <li>Sistema de perguntas diárias ({user?.daily_questions_used || 0} usadas hoje)</li>
        </ul>
      </div>
    </div>
  );
}
