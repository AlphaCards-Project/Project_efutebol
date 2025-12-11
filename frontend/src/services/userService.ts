// Serviço para gerenciar dados do usuário compartilhados entre componentes

export interface UserData {
  email: string
  full_name: string
  nickname: string
  platform: string
  is_premium: boolean
  role?: string
  avatar_url?: string
}

class UserService {
  private userData: UserData | null = null
  private listeners: Array<(user: UserData | null) => void> = []

  // Dados padrão
  private defaultUser: UserData = {
    email: 'usuario@email.com',
    full_name: 'User Padrão',
    nickname: 'User Padrão',
    platform: 'PC',
    is_premium: true,
    role: 'free',
    avatar_url: ''
  }

  constructor() {
    // Carregar dados do localStorage se disponíveis
    const stored = localStorage.getItem('userData')
    if (stored) {
      try {
        this.userData = JSON.parse(stored)
      } catch {
        this.userData = this.defaultUser
      }
    } else {
      this.userData = this.defaultUser
    }
  }

  getUserData(): UserData {
    return this.userData || this.defaultUser
  }

  setUserData(data: UserData) {
    this.userData = data
    localStorage.setItem('userData', JSON.stringify(data))
    this.notifyListeners()
  }

  updateUserData(updates: Partial<UserData>) {
    this.userData = { ...this.getUserData(), ...updates }
    localStorage.setItem('userData', JSON.stringify(this.userData))
    this.notifyListeners()
  }

  subscribe(listener: (user: UserData | null) => void) {
    this.listeners.push(listener)
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.userData))
  }

  clearUserData() {
    this.userData = null
    localStorage.removeItem('userData')
    this.notifyListeners()
  }
}

export const userService = new UserService()
