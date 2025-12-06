import { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard';

function AuthPages() {
  const [showLogin, setShowLogin] = useState(true);
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%)',
        color: '#D4AF37',
        fontSize: '1.5rem'
      }}>
        Carregando...
      </div>
    );
  }

  if (user) {
    return <Dashboard />;
  }

  return showLogin ? (
    <Login onToggleForm={() => setShowLogin(false)} />
  ) : (
    <Register onToggleForm={() => setShowLogin(true)} />
  );
}

function App() {
  return (
    <AuthProvider>
      <AuthPages />
    </AuthProvider>
  );
}

export default App;
