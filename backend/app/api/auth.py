from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserRegister, UserLogin, Token, UserResponse, MessageResponse
from app.services.supabase_service import supabase_service
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Registra um novo usuário
    """
    try:
        user = await supabase_service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        
        # Criar token JWT
        access_token = create_access_token(
            data={
                "sub": user["id"],
                "email": user["email"],
                "is_premium": user["is_premium"]
            }
        )
        
        return Token(
            access_token=access_token,
            user=UserResponse(**user)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar usuário: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Autentica usuário e retorna token JWT
    """
    user = await supabase_service.authenticate_user(
        email=credentials.email,
        password=credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Criar token JWT
    access_token = create_access_token(
        data={
            "sub": user["id"],
            "email": user["email"],
            "is_premium": user["is_premium"]
        }
    )
    
    return Token(
        access_token=access_token,
        user=UserResponse(**user)
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
