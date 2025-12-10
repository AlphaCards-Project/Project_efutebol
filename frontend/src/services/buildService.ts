const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface Build {
  id: number
  user_id: string
  card_id: number
  title: string
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
  overall_rating?: number
  is_official_meta: boolean
  meta_content?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface BuildCreate {
  card_id: number
  title: string
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
  overall_rating?: number
  is_official_meta?: boolean
  meta_content?: Record<string, any>
}

export interface BuildUpdate {
  title?: string
  shooting?: number
  passing?: number
  dribbling?: number
  dexterity?: number
  lower_body_strength?: number
  aerial_strength?: number
  defending?: number
  gk_1?: number
  gk_2?: number
  gk_3?: number
  overall_rating?: number
  is_official_meta?: boolean
  meta_content?: Record<string, any>
}

export interface BuildQuery {
  player_name: string
  position: string
}

export interface BuildRecommendation {
  player_name: string
  position: string
  priority_points: Array<{ skill: string; points: number }>
  playstyle: string
  tips: string
  from_cache: boolean
}

class BuildService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  async getBuildRecommendation(query: BuildQuery): Promise<BuildRecommendation> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(query)
    })

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Limite diário de perguntas atingido. Faça upgrade para Premium!')
      }
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar recomendação')
    }

    return response.json()
  }

  async createBuild(buildData: BuildCreate): Promise<Build> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds/create`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(buildData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao criar build')
    }

    return response.json()
  }

  async getMyBuilds(): Promise<Build[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds/my-builds`, {
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar minhas builds')
    }

    return response.json()
  }

  async getBuildsByCard(cardId: number): Promise<Build[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds/card/${cardId}`, {
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar builds da carta')
    }

    return response.json()
  }

  async getBuildById(buildId: number): Promise<Build> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds/${buildId}`, {
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar build')
    }

    return response.json()
  }

  async updateBuild(buildId: number, buildData: BuildUpdate): Promise<Build> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds/${buildId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(buildData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao atualizar build')
    }

    return response.json()
  }

  async deleteBuild(buildId: number): Promise<{ message: string; detail: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/builds/${buildId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao deletar build')
    }

    return response.json()
  }

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
}

export const buildService = new BuildService()
