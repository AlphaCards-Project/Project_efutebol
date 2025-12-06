-- ============================================================================
-- SETUP DEFINITIVO DO BANCO DE DADOS - eFootball Assistant
-- Versão: 7 (Definitiva)
-- Data: 2025-12-06
-- ============================================================================
-- Este script cria TUDO do zero com as configurações corretas
-- IMPORTANTE: Este script deleta TODOS os dados existentes!
-- ============================================================================


-- 2. CRIAR TIPOS ENUM
-- ============================================================================
CREATE TYPE user_platform AS ENUM ('console', 'pc', 'mobile');
CREATE TYPE user_role AS ENUM ('admin', 'premium', 'free');

-- 3. TABELA USERS (Usuários do sistema - sincronizado com Supabase Auth)
-- ============================================================================
CREATE TABLE users (
    id UUID PRIMARY KEY,  -- UUID do Supabase Auth
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100),
    nickname VARCHAR(50) UNIQUE,
    platform user_platform,
    role user_role NOT NULL DEFAULT 'free',
    is_premium BOOLEAN DEFAULT FALSE,
    daily_questions_used INTEGER DEFAULT 0,
    last_reset TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE users IS 'Usuários do sistema (sincronizado com Supabase Auth via UUID)';
COMMENT ON COLUMN users.id IS 'UUID do usuário no Supabase Auth';
COMMENT ON COLUMN users.is_premium IS 'Se o usuário é premium (desabilita limite de perguntas)';
COMMENT ON COLUMN users.daily_questions_used IS 'Contador de perguntas feitas hoje';
COMMENT ON COLUMN users.last_reset IS 'Data do último reset do contador diário';

-- 4. TABELA PLAYERS (Jogadores reais do eFootball)
-- ============================================================================
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    konami_player_id INTEGER UNIQUE,
    real_position VARCHAR(50),
    nationality VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE players IS 'Jogadores reais do eFootball (ex: Messi, Neymar, CR7)';
COMMENT ON COLUMN players.konami_player_id IS 'ID oficial do jogador na base Konami';
COMMENT ON COLUMN players.real_position IS 'Posição principal do jogador na vida real';

-- 5. TABELA CARDS (Versões/Cartas específicas dos jogadores)
-- ============================================================================
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    konami_id INTEGER UNIQUE,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(100),  -- Ex: "Featured 2024", "Legend", "Icon"
    card_type VARCHAR(50),
    position VARCHAR(10),
    overall_rating INTEGER,
    stats_base JSONB,  -- Stats base da carta em JSON
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE cards IS 'Cartas/versões específicas dos jogadores (ex: Messi Icon, Messi Featured 2024)';
COMMENT ON COLUMN cards.player_id IS 'Referência ao jogador real';
COMMENT ON COLUMN cards.version IS 'Versão da carta (Featured, Legend, Icon, etc)';
COMMENT ON COLUMN cards.stats_base IS 'Estatísticas base da carta em formato JSON';

-- 6. TABELA BUILDS (Configurações de pontos de habilidade para cartas)
-- ============================================================================
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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
    meta_content JSONB,  -- Conteúdo adicional da build (dicas, playstyle, etc)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE builds IS 'Configurações de pontos de habilidade para cada carta';
COMMENT ON COLUMN builds.is_official_meta IS 'Se é uma build oficial recomendada pela IA';
COMMENT ON COLUMN builds.meta_content IS 'Conteúdo adicional: dicas, playstyle, instruções, etc';

-- 7. TABELA GAMEPLAY_TIPS (Dicas e soluções de gameplay)
-- ============================================================================
CREATE TABLE gameplay_tips (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    pain_description TEXT,
    solution TEXT NOT NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE gameplay_tips IS 'Dicas e soluções de gameplay (defesa, ataque, passes, etc)';
COMMENT ON COLUMN gameplay_tips.category IS 'Categoria da dica (defesa, ataque, drible, passe, etc)';
COMMENT ON COLUMN gameplay_tips.pain_description IS 'Descrição do problema que o jogador enfrenta';
COMMENT ON COLUMN gameplay_tips.solution IS 'Solução detalhada do problema';

-- 8. TABELA AI_CACHE (Cache de respostas da IA para economizar API calls)
-- ============================================================================
CREATE TABLE ai_cache (
    id SERIAL PRIMARY KEY,
    prompt_hash VARCHAR(64) NOT NULL UNIQUE,  -- Hash SHA256 da pergunta
    response_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE  -- Data de expiração (opcional)
);

COMMENT ON TABLE ai_cache IS 'Cache de respostas da IA para economizar chamadas de API';
COMMENT ON COLUMN ai_cache.prompt_hash IS 'Hash SHA256 da pergunta do usuário para busca rápida';
COMMENT ON COLUMN ai_cache.expires_at IS 'Data de expiração do cache (para invalidar respostas antigas)';

-- 9. ÍNDICES PARA PERFORMANCE
-- ============================================================================

-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_premium ON users(is_premium);

-- Players
CREATE INDEX idx_players_name ON players(name);
CREATE INDEX idx_players_konami_id ON players(konami_player_id);
CREATE INDEX idx_players_nationality ON players(nationality);

-- Cards
CREATE INDEX idx_cards_player_id ON cards(player_id);
CREATE INDEX idx_cards_konami_id ON cards(konami_id);
CREATE INDEX idx_cards_name ON cards(name);
CREATE INDEX idx_cards_version ON cards(version);
CREATE INDEX idx_cards_position ON cards(position);

-- Builds
CREATE INDEX idx_builds_user_id ON builds(user_id);
CREATE INDEX idx_builds_card_id ON builds(card_id);
CREATE INDEX idx_builds_is_official_meta ON builds(is_official_meta);
CREATE INDEX idx_builds_meta_content ON builds USING GIN (meta_content);

-- Gameplay Tips
CREATE INDEX idx_gameplay_tips_category ON gameplay_tips(category);
CREATE INDEX idx_gameplay_tips_created_by ON gameplay_tips(created_by_user_id);

-- AI Cache
CREATE INDEX idx_ai_cache_prompt_hash ON ai_cache(prompt_hash);
CREATE INDEX idx_ai_cache_expires_at ON ai_cache(expires_at);

-- 10. TRIGGERS DE UPDATE (auto-update do campo updated_at)
-- ============================================================================
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER tr_users_update BEFORE UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER tr_players_update BEFORE UPDATE ON players
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER tr_cards_update BEFORE UPDATE ON cards
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER tr_builds_update BEFORE UPDATE ON builds
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER tr_gameplay_tips_update BEFORE UPDATE ON gameplay_tips
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

-- 11. DADOS DE EXEMPLO (Para testes e desenvolvimento)
-- ============================================================================

-- Inserir jogadores exemplo
INSERT INTO players (name, konami_player_id, real_position, nationality) VALUES
('Neymar Jr', 117366, 'LW/CF', 'Brazil'),
('Cristiano Ronaldo', 44, 'CF/LWF', 'Portugal'),
('Lionel Messi', 112558, 'RWF/AMF', 'Argentina'),
('Kylian Mbappé', 231747, 'CF/LWF', 'France'),
('Erling Haaland', 133543, 'CF', 'Norway'),
('Vinícius Jr', 238794, 'LWF', 'Brazil'),
('Kevin De Bruyne', 192985, 'AMF', 'Belgium'),
('Pedri', 251854, 'CMF', 'Spain'),
('Virgil van Dijk', 203376, 'CB', 'Netherlands'),
('Thibaut Courtois', 44383, 'GK', 'Belgium')
ON CONFLICT (konami_player_id) DO NOTHING;

-- Inserir cartas exemplo (vinculadas aos jogadores)
INSERT INTO cards (player_id, konami_id, name, version, card_type, position, overall_rating, stats_base) VALUES
-- Neymar
(1, 117366001, 'Neymar Jr', 'Big Time 2015', 'Legendary', 'LWF', 96, '{"pace": 95, "shooting": 88, "passing": 87, "dribbling": 96, "defending": 30, "physical": 65}'::jsonb),
(1, 117366002, 'Neymar Jr', 'Featured 2024', 'Featured', 'LWF', 94, '{"pace": 93, "shooting": 86, "passing": 85, "dribbling": 94, "defending": 28, "physical": 63}'::jsonb),

-- Cristiano Ronaldo
(2, 44001, 'C. Ronaldo', 'Legend', 'Legendary', 'CF', 98, '{"pace": 92, "shooting": 96, "passing": 83, "dribbling": 90, "defending": 35, "physical": 92}'::jsonb),
(2, 44002, 'C. Ronaldo', 'Icon 2008', 'Legendary', 'LWF', 97, '{"pace": 95, "shooting": 94, "passing": 82, "dribbling": 92, "defending": 33, "physical": 85}'::jsonb),

-- Messi
(3, 112558001, 'L. Messi', 'Icon', 'Legendary', 'RWF', 97, '{"pace": 89, "shooting": 94, "passing": 93, "dribbling": 97, "defending": 35, "physical": 70}'::jsonb),
(3, 112558002, 'L. Messi', 'Featured 2024', 'Featured', 'RWF', 93, '{"pace": 87, "shooting": 92, "passing": 91, "dribbling": 95, "defending": 33, "physical": 68}'::jsonb),

-- Mbappé
(4, 231747001, 'K. Mbappé', 'Featured 2024', 'Featured', 'CF', 95, '{"pace": 98, "shooting": 91, "passing": 84, "dribbling": 92, "defending": 36, "physical": 80}'::jsonb),

-- Haaland
(5, 133543001, 'E. Haaland', 'Featured 2024', 'Featured', 'CF', 94, '{"pace": 92, "shooting": 95, "passing": 75, "dribbling": 82, "defending": 40, "physical": 93}'::jsonb),

-- Vinícius Jr
(6, 238794001, 'Vinícius Jr', 'Featured 2024', 'Featured', 'LWF', 92, '{"pace": 97, "shooting": 85, "passing": 82, "dribbling": 93, "defending": 32, "physical": 72}'::jsonb),

-- De Bruyne
(7, 192985001, 'K. De Bruyne', 'Featured 2024', 'Featured', 'AMF', 93, '{"pace": 78, "shooting": 89, "passing": 96, "dribbling": 88, "defending": 65, "physical": 82}'::jsonb),

-- Pedri
(8, 251854001, 'Pedri', 'Featured 2024', 'Featured', 'CMF', 89, '{"pace": 78, "shooting": 75, "passing": 88, "dribbling": 86, "defending": 68, "physical": 70}'::jsonb),

-- Van Dijk
(9, 203376001, 'V. van Dijk', 'Featured 2024', 'Featured', 'CB', 92, '{"pace": 80, "shooting": 65, "passing": 75, "dribbling": 72, "defending": 93, "physical": 92}'::jsonb),

-- Courtois
(10, 44383001, 'T. Courtois', 'Featured 2024', 'Featured', 'GK', 91, '{"diving": 90, "handling": 88, "kicking": 82, "reflexes": 92, "speed": 75, "positioning": 89}'::jsonb)

ON CONFLICT (konami_id) DO NOTHING;

-- Inserir dicas de gameplay exemplo
INSERT INTO gameplay_tips (category, title, pain_description, solution) VALUES
('defesa', 'Como defender contra velocistas', 'Meu adversário sempre me vence com jogadores rápidos nas pontas', 'Use zagueiros com boa velocidade (mínimo 80) e sempre mantenha um defensor de cobertura. Não saia correndo atrás da bola, use L2/LT para jockey e acompanhe o movimento. Ajuste a tática para "Defensive" quando necessário.'),
('ataque', 'Como finalizar melhor no 1v1', 'Eu sempre erro gols cara a cara com o goleiro', 'No 1v1, aproxime-se do goleiro e finalize com curva (R1/RB + Quadrado/X) para o canto oposto do movimento do goleiro. Se ele avançar, use toque colocado (L1/LB + Quadrado/X). Evite finalizar de primeira em velocidade máxima.'),
('passe', 'Como fazer passes entre linhas', 'Meus passes sempre são interceptados', 'Use passes com efeito (R2/RT + X/A) para curvar em volta dos defensores. Espere o momento certo quando o defensor estiver se movendo lateralmente. Jogadores com "Through Passing" alto executam melhor esses passes.'),
('drible', 'Como usar o sprint efetivamente', 'Quando eu corro rápido demais, perco a bola facilmente', 'Não use R2/RT o tempo todo. Use apenas em espaços abertos. Em áreas congestionadas, use apenas o analógico esquerdo com toques curtos. Alterne entre velocidade normal e sprint para confundir a defesa.'),
('tática', 'Melhor formação para iniciantes', 'Não sei qual formação usar', 'Para iniciantes, recomendo 4-3-3 ou 4-2-3-1. São formações equilibradas com boa cobertura defensiva e opções de ataque. Use táticas "Possession Game" ou "Quick Counter" dependendo do seu estilo.')
ON CONFLICT DO NOTHING;

-- 12. PERMISSÕES E POLÍTICAS RLS (Row Level Security) - Supabase
-- ============================================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE builds ENABLE ROW LEVEL SECURITY;
ALTER TABLE gameplay_tips ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_cache ENABLE ROW LEVEL SECURITY;

-- Políticas para USERS
-- Usuários podem ler seu próprio perfil
CREATE POLICY "Usuários podem ver seu próprio perfil"
ON users FOR SELECT
USING (auth.uid() = id);

-- Usuários podem atualizar seu próprio perfil
CREATE POLICY "Usuários podem atualizar seu próprio perfil"
ON users FOR UPDATE
USING (auth.uid() = id);

-- Políticas para PLAYERS (leitura pública)
CREATE POLICY "Qualquer um pode ver jogadores"
ON players FOR SELECT
USING (true);

-- Políticas para CARDS (leitura pública)
CREATE POLICY "Qualquer um pode ver cartas"
ON cards FOR SELECT
USING (true);

-- Políticas para BUILDS
-- Qualquer um pode ver builds
CREATE POLICY "Qualquer um pode ver builds"
ON builds FOR SELECT
USING (true);

-- Usuários autenticados podem criar builds
CREATE POLICY "Usuários autenticados podem criar builds"
ON builds FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Usuários podem atualizar suas próprias builds
CREATE POLICY "Usuários podem atualizar suas próprias builds"
ON builds FOR UPDATE
USING (auth.uid() = user_id);

-- Usuários podem deletar suas próprias builds
CREATE POLICY "Usuários podem deletar suas próprias builds"
ON builds FOR DELETE
USING (auth.uid() = user_id);

-- Políticas para GAMEPLAY_TIPS (leitura pública)
CREATE POLICY "Qualquer um pode ver dicas"
ON gameplay_tips FOR SELECT
USING (true);

-- Usuários autenticados podem criar dicas
CREATE POLICY "Usuários autenticados podem criar dicas"
ON gameplay_tips FOR INSERT
WITH CHECK (auth.uid() = created_by_user_id);

-- Políticas para AI_CACHE (apenas sistema pode manipular)
-- Service role terá acesso total via backend

-- ============================================================================
-- FIM DO SETUP DEFINITIVO
-- ============================================================================

-- Verificar criação das tabelas
SELECT 
    tablename,
    schemaname
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;

-- Contar registros iniciais
SELECT 'players' as tabela, COUNT(*) as registros FROM players
UNION ALL
SELECT 'cards', COUNT(*) FROM cards
UNION ALL
SELECT 'gameplay_tips', COUNT(*) FROM gameplay_tips;
