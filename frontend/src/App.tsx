import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Chat from './chat/Chat'
import Login from './login/Login'
import Registro from './registro/Registro'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Router>
  )
}

export default App
