const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface Card {
  id: number
  player_id: number
  name: string
  version: string
  card_type: string
  position: string
  overall_rating: number
  image_url?: string
  created_at: string
  updated_at: string
}

export interface CardCreate {
  player_id: number
  name: string
  version: string
  card_type: string
  position: string
  overall_rating: number
  image_url?: string
}

export interface CardUpdate {
  name?: string
  version?: string
  card_type?: string
  position?: string
  overall_rating?: number
  image_url?: string
}

class CardsService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  async listCards(params?: {
    player_id?: number
    position?: string
    card_type?: string
    search?: string
    limit?: number
    offset?: number
  }): Promise<Card[]> {
    const queryParams = new URLSearchParams()
    if (params?.player_id) queryParams.append('player_id', params.player_id.toString())
    if (params?.position) queryParams.append('position', params.position)
    if (params?.card_type) queryParams.append('card_type', params.card_type)
    if (params?.search) queryParams.append('search', params.search)
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.offset) queryParams.append('offset', params.offset.toString())

    const response = await fetch(
      `${API_BASE_URL}/api/v1/cards?${queryParams}`,
      { headers: this.getAuthHeaders() }
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar cartas')
    }

    return response.json()
  }

  async getCard(cardId: number): Promise<Card> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/cards/${cardId}`,
      { headers: this.getAuthHeaders() }
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar carta')
    }

    return response.json()
  }

  async createCard(cardData: CardCreate): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cards`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(cardData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao criar carta')
    }

    return response.json()
  }

  async updateCard(cardId: number, cardData: CardUpdate): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cards/${cardId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(cardData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao atualizar carta')
    }

    return response.json()
  }

  async deleteCard(cardId: number): Promise<{ message: string; detail: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cards/${cardId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao deletar carta')
    }

    return response.json()
  }
}

export const cardsService = new CardsService()
