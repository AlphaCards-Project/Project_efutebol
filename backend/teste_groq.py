import os
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("API_KEY"))

print("🤖 Testando API Groq (Llama 3)...\n")

# Simulando o RAG (Contexto do Sócio + Pergunta)
contexto_socio = """
Regra do Pro Player: Para zagueiros (CB), a velocidade mínima deve ser 75. 
Zagueiros lentos sofrem contra atacantes rápidos no eFootball 2024.
"""

pergunta_usuario = "Meu zagueiro tem 60 de velocidade, ele é bom?"

print(f"📝 Contexto RAG:\n{contexto_socio}")
print(f"❓ Pergunta: {pergunta_usuario}\n")
print("⏳ Gerando resposta...\n")

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Você é um técnico de eFootball. Responda com base APENAS no contexto abaixo.\nContexto: {contexto_socio}"
            },
            {
                "role": "user",
                "content": pergunta_usuario,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=500
    )
    
    resposta = chat_completion.choices[0].message.content
    print(f"✅ Resposta da IA:\n{resposta}\n")
    print(f"📊 Tokens usados: {chat_completion.usage.total_tokens}")
    
except Exception as e:
    print(f"❌ Erro ao conectar com Groq: {e}")
