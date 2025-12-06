from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserRegister, UserLogin, Token, UserResponse, MessageResponse
from app.services.supabase_service import supabase_service
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Registra um novo usuário no sistema
    
    - **email**: Email válido (será usado para login)
    - **password**: Senha com no mínimo 6 caracteres
    - **full_name**: Nome completo (opcional)
    - **nickname**: Apelido/gamertag (opcional)
    - **platform**: Plataforma de jogo - console, pc ou mobile (opcional)
    
    Retorna um token JWT e os dados do usuário criado.
    """
    try:
        user = await supabase_service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            nickname=user_data.nickname,
            platform=user_data.platform
        )
        
        # Criar token JWT
        access_token = create_access_token(
            data={
                "sub": user["id"],
                "email": user["email"],
                "is_premium": user.get("is_premium", False)
            }
        )
        
        return Token(
            access_token=access_token,
            user=UserResponse(**user)
        )
    
    except Exception as e:
        error_message = str(e)
        if "already exists" in error_message.lower() or "duplicate" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado no sistema"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar usuário: {error_message}"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Autentica usuário e retorna token JWT
    
    - **email**: Email cadastrado
    - **password**: Senha do usuário
    
    Retorna um token JWT válido por 7 dias e os dados do usuário.
    Use o token no header: `Authorization: Bearer <token>`
    """
    try:
        user = await supabase_service.authenticate_user(
            email=credentials.email,
            password=credentials.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Criar token JWT
        access_token = create_access_token(
            data={
                "sub": user["id"],
                "email": user["email"],
                "is_premium": user.get("is_premium", False)
            }
        )
        
        return Token(
            access_token=access_token,
            user=UserResponse(**user)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao autenticar: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = None):
    """
    Retorna informações do usuário autenticado
    (Implementar dependency injection depois)
    """
    user = await supabase_service.get_user(current_user["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return UserResponse(**user)
