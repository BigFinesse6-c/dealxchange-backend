from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DealXchange"
    DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = "f085aef684d4b2b01384268deb5b113db00b28c68a3a96e77740414e8832730ea9ef8613d2949b5c8e75460528c1585e4d01956611ccae9963326548e876f57d"
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    CORS_ORIGINS: str = "http://localhost:3000" # <-- add this

    class Config:
        env_file = ".env"

settings = Settings()

# Debug: print loaded settings (without secrets)
print("Loaded settings:", {
    "DATABASE_URL": settings.DATABASE_URL,
    "ALGORITHM": settings.ALGORITHM,
    "ACCESS_TOKEN_EXPIRE_MINUTES": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
})

