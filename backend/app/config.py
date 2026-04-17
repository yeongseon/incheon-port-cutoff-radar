from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "Incheon Port Cut-off Risk Radar"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://radar:radar@localhost:5432/cutoff_radar"

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 300  # 5 minutes

    # External APIs
    traffic_api_base_url: str = ""
    traffic_api_key: str = ""
    port_api_base_url: str = ""
    port_api_key: str = ""

    # Auth
    api_key: str = ""  # empty = no auth required

    # Engine
    engine_version: str = "v1.0.0"
    default_buffer_minutes: int = 15
    conservative_extra_buffer_minutes: int = 20
    freshness_sla_seconds: int = 600  # 10 minutes

    # Scheduler
    ingestion_interval_seconds: int = 180  # 3 minutes

    model_config = {"env_file": ".env", "env_prefix": "RADAR_"}


settings = Settings()
