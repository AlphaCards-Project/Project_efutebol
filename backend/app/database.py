from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# COLOCAR AQUI A URL DO SUPABASE (Use o driver postgresql padrão, não o async para o Alembic não chiar agora)
# Ex: postgresql://postgres:suasenha@db.supabase.co:5432/postgres
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Fr33D0m_4_AllC0nFiD3nc3@db.egydaqgczfhrpqejnhtp.supabase.co:5432/postgres"

# Cria a conexão    
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Essa é a classe mágica que seus models vão herdar
Base = declarative_base()

# Dependency (Para usar nas rotas do FastAPI depois)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()