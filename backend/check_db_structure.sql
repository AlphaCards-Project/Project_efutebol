-- Verificar estrutura da tabela users
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Ver se há registros
SELECT id, email, name, role, created_at
FROM users
LIMIT 5;
