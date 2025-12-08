import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- CORREÇÃO DE CAMINHO ---
# Pega o caminho absoluto da pasta onde este env.py está
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para chegar na pasta 'backend' (onde está a pasta 'app')
sys.path.insert(0, os.path.dirname(current_dir))

# --- CORREÇÃO DO IMPORT ---
# Agora que o Python vê a pasta 'backend', podemos importar direto de 'app'
# NÃO use 'Project_efutebol...', use apenas 'app...'
from app.database import Base
from app.models import Build, User # Importe seus modelos aqui

target_metadata = Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ... (O resto do arquivo padrão do Alembic continua igual abaixo) ...
# Apenas certifique-se que o run_migrations_online usa o target_metadata correto