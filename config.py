from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=".env",
    env_ignore_empty=True,
    extra="ignore",
)

class DatabaseConfig(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    model_config = _base_config

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    
class SecurityConfig(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    
    model_config = _base_config

security_config = SecurityConfig()
db_config = DatabaseConfig()