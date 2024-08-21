from pydantic_settings import BaseSettings
from yarl import URL


class Settings(BaseSettings):
    # llm
    llm_host: str = "localhost"  # 66.114.112.70
    llm_port: str = ""  # 21098
    llm_tokens: int = 1024
    llm_model_name: str = "qwen"

    # vlm
    vlm_host: str = "localhost"  # 66.114.112.70
    vlm_port: str = ""  # 31121
    vlm_tokens: int = 1024
    vlm_model_name: str = "qwen"

    # database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "user"
    db_pass: str = "pass"
    db_base: str = "base"

    @property
    def llm_url(self) -> str:
        return f"http://{self.llm_host}:{self.llm_port}/v1"

    @property
    def vlm_url(self) -> str:
        return f"http://{self.vlm_host}:{self.vlm_port}/v1"

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
