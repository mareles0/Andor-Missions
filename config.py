import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "defaultdb")
DB_USER = os.getenv("DB_USER", "doadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_SSLMODE = os.getenv("DB_SSLMODE", "prefer")

JWT_SECRET = os.getenv("JWT_SECRET", "andor_rebellion_secret_key_2024")

COLORS = {
    "primary": "#1a1a2e",
    "secondary": "#16213e",
    "accent": "#e94560",
    "text": "#eaeaea",
    "success": "#4caf50",
    "warning": "#ff9800",
    "background": "#0f0f1e",
}
