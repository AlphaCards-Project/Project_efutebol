-- CRIAR USUÁRIO DE TESTE MANUALMENTE
-- Execute no Supabase Dashboard > SQL Editor

-- 1. Habilitar signups temporariamente OU criar usuário direto
-- Vá em: Dashboard > Authentication > Settings > Enable Sign ups: ON

-- 2. OU criar usuário direto via SQL (mais simples):

-- Gerar UUID aleatório para o usuário
DO $$
DECLARE
    new_user_id uuid := gen_random_uuid();
BEGIN
    -- Inserir na tabela auth.users (sistema de autenticação)
    INSERT INTO auth.users (
        id, 
        instance_id, 
        email, 
        encrypted_password,
        email_confirmed_at,
        created_at,
        updated_at,
        raw_app_meta_data,
        raw_user_meta_data,
        aud,
        role
    )
    VALUES (
        new_user_id,
        '00000000-0000-0000-0000-000000000000',
        'teste@teste.com',
        crypt('teste123', gen_salt('bf')),
        NOW(),
        NOW(),
        NOW(),
        '{"provider":"email","providers":["email"]}',
        '{}',
        'authenticated',
        'authenticated'
    );
    
    -- Inserir na tabela users (dados do perfil)
    INSERT INTO users (
        id,
        email,
        name,
        role,
        is_premium,
        daily_questions_used,
        last_reset,
        created_at
    )
    VALUES (
        new_user_id,
        'teste@teste.com',
        'Usuario Teste',
        'free',
        false,
        0,
        NOW(),
        NOW()
    );
    
    RAISE NOTICE 'Usuario criado com ID: %', new_user_id;
END $$;

-- Verificar se foi criado
SELECT email, email_confirmed_at, created_at 
FROM auth.users 
WHERE email = 'teste@teste.com';
