from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Obter URL do banco de dados do ambiente
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no arquivo .env!")

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