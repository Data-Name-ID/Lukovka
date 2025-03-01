from functools import cached_property
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AppConfig(BaseModel):
    origins: str = "http://localhost,http://localhost:8000"


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class DatabaseConfig(BaseModel):
    user: str | None = "postgres"
    password: str | None = "postgres"  # noqa: S105
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @cached_property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

    access_token_expiration_minutes: int = 15
    refresh_token_expiration_days: int = 30


class MailSettings(BaseModel):
    smtp_server: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_use_tls: bool = True


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR.parent / ".env.template", BASE_DIR.parent / ".env"),
        case_sensitive=False,
        env_prefix="BACKEND__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app: AppConfig
    run: RunConfig
    db: DatabaseConfig
    redis: RedisConfig
    jwt: AuthJWT
    email: MailSettings

    static_dir: Path = BASE_DIR / "static"
    templates_dir: Path = BASE_DIR / "templates"


config = Config()
