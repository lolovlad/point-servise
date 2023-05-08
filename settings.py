from pydantic import BaseSettings


class Settings(BaseSettings):
    host_server: str
    port_server: int

    host_frontend: str
    port_frontend: int

    static_file: str


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")