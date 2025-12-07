-- VERIFICAR E CORRIGIR TABELA USERS
-- Execute no Supabase SQL Editor

-- Deletar tabela antiga se existir problemas
-- DROP TABLE IF EXISTS users CASCADE;

-- Criar tabela users correta
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100),
    nickname VARCHAR(50),
    platform VARCHAR(20),
    role VARCHAR(20) DEFAULT 'free',
    is_premium BOOLEAN DEFAULT FALSE,
    daily_questions_used INTEGER DEFAULT 0,
    last_reset TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Desabilitar RLS
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- Verificar estrutura
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;
