import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Chat from './chat/Chat'
import Login from './login/Login'
import Registro from './registro/Registro'
import UserSettings from './user/UserSettings'
import DashboardLayout from './dashboard/DashboardLayout'
import Dashboard from './dashboard'
import Builds from './dashboard/builds'
import Catalog from './dashboard/catalog'
import Cards from './dashboard/cards'
import Jogador from './dashboard/jogador'
import { UserStats } from './dashboard/analytics'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/user/settings" element={
          <ProtectedRoute>
            <UserSettings />
          </ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="builds" element={<Builds />} />
          <Route path="catalog" element={<Catalog />} />
          <Route path="cards" element={<Cards />} />
          <Route path="jogador" element={<Jogador />} />
          <Route path="analytics" element={<UserStats />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
