import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

COLORS = {
    "primary": "#292949",
    "secondary": "#101931",
    "accent": "#ff4c05",
    "text": "#eaeaea",
    "success": "#4caf50",
    "warning": "#ff9800",
    "background": "#000000",
}
