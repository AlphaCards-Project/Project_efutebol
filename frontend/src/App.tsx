import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Chat from './chat/Chat'
import Login from './login/Login'
import Registro from './registro/Registro'
import DashboardLayout from './dashboard/DashboardLayout'
import Dashboard from './dashboard'
import Builds from './dashboard/builds'
import Catalog from './dashboard/catalog'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="builds" element={<Builds />} />
          <Route path="catalog" element={<Catalog />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
