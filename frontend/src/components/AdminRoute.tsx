import { Navigate } from 'react-router-dom'

interface AdminRouteProps {
  children: React.ReactNode
}

function AdminRoute({ children }: AdminRouteProps) {
  const token = localStorage.getItem('token')
  const userData = localStorage.getItem('user')
  
  if (!token) {
    return <Navigate to="/login" replace />
  }

  if (!userData) {
    return <Navigate to="/login" replace />
  }

  try {
    const user = JSON.parse(userData)
    
    if (user.role !== 'admin') {
      // Se não for admin, redireciona para o chat
      return <Navigate to="/chat" replace />
    }
  } catch (error) {
    // Se houver erro ao parsear, redireciona para login
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export default AdminRoute
