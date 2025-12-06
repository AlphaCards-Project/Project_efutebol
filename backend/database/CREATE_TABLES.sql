-- Versão 5: FINAL - Tabela de votos removida e adicionada tabela de cache para a IA.

-- 1. ENUMS (Mantidos)
CREATE TYPE user_platform AS ENUM ('console', 'pc', 'mobile');
CREATE TYPE user_role AS ENUM ('admin', 'premium', 'free');

-- 2. TABELA DE USUÁRIOS (Mantida)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50) UNIQUE, 
    email VARCHAR(255) NOT NULL UNIQUE, 
    password_hash VARCHAR(255) NOT NULL, 
    platform user_platform, 
    role user_role NOT NULL DEFAULT 'free', 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. TABELA DE CARTAS (Mantida)
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    konami_id INTEGER UNIQUE,
    name VARCHAR(100) NOT NULL,
    card_type VARCHAR(50),
    position VARCHAR(10)
);

-- 4. TABELA DE BUILDS (Mantida)
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    card_id INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE, 
    title VARCHAR(100) NOT NULL,
    shooting INTEGER CHECK (shooting BETWEEN 0 AND 99) DEFAULT 0,
    passing INTEGER CHECK (passing BETWEEN 0 AND 99) DEFAULT 0,
    dribbling INTEGER CHECK (dribbling BETWEEN 0 AND 99) DEFAULT 0,
    dexterity INTEGER CHECK (dexterity BETWEEN 0 AND 99) DEFAULT 0,
    lower_body_strength INTEGER CHECK (lower_body_strength BETWEEN 0 AND 99) DEFAULT 0,
    aerial_strength INTEGER CHECK (aerial_strength BETWEEN 0 AND 99) DEFAULT 0,
    defending INTEGER CHECK (defending BETWEEN 0 AND 99) DEFAULT 0,
    gk_1 INTEGER CHECK (gk_1 BETWEEN 0 AND 99) DEFAULT 0,
    gk_2 INTEGER CHECK (gk_2 BETWEEN 0 AND 99) DEFAULT 0,
    gk_3 INTEGER CHECK (gk_3 BETWEEN 0 AND 99) DEFAULT 0,
    overall_rating INTEGER,
    is_official_meta BOOLEAN DEFAULT FALSE,
    meta_content JSONB, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. TABELA: GAMEPLAY_TIPS (Mantida)
CREATE TABLE gameplay_tips (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    pain_description TEXT,
    solution TEXT NOT NULL,
    created_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. NOVA TABELA: AI_CACHE (Para economizar chamadas de API)
CREATE TABLE ai_cache (
    id SERIAL PRIMARY KEY,
    -- Hash (SHA256, por exemplo) da pergunta do usuário para busca rápida
    prompt_hash VARCHAR(64) NOT NULL UNIQUE,
    -- O texto da resposta da IA
    response_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    -- Data de expiração do cache (opcional, para invalidar respostas antigas)
    expires_at TIMESTAMP WITH TIME ZONE
);

-- 7. TRIGGERS DE UPDATE (Mantidos)
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER tr_users_update BEFORE UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER tr_builds_update BEFORE UPDATE ON builds
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER tr_gameplay_tips_update BEFORE UPDATE ON gameplay_tips
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();


-- 8. ÍNDICES (CRUCIAL PARA PERFORMANCE)
/* 
Sem eles, quando seu site tiver 10 mil builds, buscar "Todas as builds do Messi" vai ficar lento.
Para aplicar estes índices, apenas execute os comandos no seu banco de dados PostgreSQL.

-- Acelera a busca de builds por usuário ou por carta
CREATE INDEX idx_builds_user_id ON builds(user_id);
CREATE INDEX idx_builds_card_id ON builds(card_id);

-- Acelera a busca de dicas por categoria (muito útil para a IA)
CREATE INDEX idx_gameplay_tips_category ON gameplay_tips(category);

-- Acelera a busca no cache da IA pelo hash da pergunta
CREATE INDEX idx_ai_cache_prompt_hash ON ai_cache(prompt_hash);

-- Acelera buscas dentro do JSON 'meta_content' (se a IA precisar filtrar por algo no JSON).
CREATE INDEX idx_builds_meta_content ON builds USING GIN (meta_content);
*/