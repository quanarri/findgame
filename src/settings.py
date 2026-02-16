from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  BOT_TOKEN: str
  ADMINS: str

  @property
  def get_db_url(self):
    return "sqlite+aiosqlite:///db.sqlite3"

  model_config = SettingsConfigDict(env_file=".env")

settings = Settings()