// Serviço para gerenciar builds do usuário

export interface Build {
  id: string
  title: string
  card_id: string
  platform: string
  shooting: number
  passing: number
  dribbling: number
  dexterity: number
  lower_body_strength: number
  aerial_strength: number
  defending: number
  gk_1: number
  gk_2: number
  gk_3: number
  overall_rating: number
  is_official_meta: boolean
  meta_content: string
  created_at: string
  updated_at: string
}

class BuildService {
  private storageKey = 'user_builds'
  private listeners: Array<(builds: Build[]) => void> = []

  constructor() {
    // Inicializar localStorage se não existir
    if (!localStorage.getItem(this.storageKey)) {
      localStorage.setItem(this.storageKey, JSON.stringify([]))
    }
  }

  // Obter todas as builds
  getBuilds(): Build[] {
    const stored = localStorage.getItem(this.storageKey)
    if (stored) {
      try {
        return JSON.parse(stored)
      } catch {
        return []
      }
    }
    return []
  }

  // Obter uma build por ID
  getBuildById(id: string): Build | null {
    const builds = this.getBuilds()
    return builds.find(b => b.id === id) || null
  }

  // Criar nova build
  createBuild(buildData: Omit<Build, 'id' | 'created_at' | 'updated_at'>): Build {
    const builds = this.getBuilds()
    const newBuild: Build = {
      ...buildData,
      id: this.generateId(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    builds.push(newBuild)
    localStorage.setItem(this.storageKey, JSON.stringify(builds))
    this.notifyListeners(builds)
    
    return newBuild
  }

  // Atualizar build existente
  updateBuild(id: string, buildData: Partial<Build>): Build | null {
    const builds = this.getBuilds()
    const index = builds.findIndex(b => b.id === id)
    
    if (index === -1) return null
    
    builds[index] = {
      ...builds[index],
      ...buildData,
      updated_at: new Date().toISOString()
    }
    
    localStorage.setItem(this.storageKey, JSON.stringify(builds))
    this.notifyListeners(builds)
    
    return builds[index]
  }

  // Deletar build
  deleteBuild(id: string): boolean {
    const builds = this.getBuilds()
    const filteredBuilds = builds.filter(b => b.id !== id)
    
    if (filteredBuilds.length === builds.length) return false
    
    localStorage.setItem(this.storageKey, JSON.stringify(filteredBuilds))
    this.notifyListeners(filteredBuilds)
    
    return true
  }

  // Calcular overall médio
  calculateOverall(build: Partial<Build>): number {
    const stats = [
      build.shooting || 0,
      build.passing || 0,
      build.dribbling || 0,
      build.dexterity || 0,
      build.lower_body_strength || 0,
      build.aerial_strength || 0,
      build.defending || 0
    ]
    
    const sum = stats.reduce((acc, val) => acc + val, 0)
    return Math.round(sum / stats.length)
  }

  // Inscrever-se para mudanças
  subscribe(listener: (builds: Build[]) => void) {
    this.listeners.push(listener)
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  private notifyListeners(builds: Build[]) {
    this.listeners.forEach(listener => listener(builds))
  }

  private generateId(): string {
    return `build_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
  }

  // Limpar todas as builds (útil para testes)
  clearAllBuilds() {
    localStorage.setItem(this.storageKey, JSON.stringify([]))
    this.notifyListeners([])
  }
}

export const buildService = new BuildService()
