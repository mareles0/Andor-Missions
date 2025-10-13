"""
Cliente Supabase compartilhado para toda a aplicação
"""
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
from auth import AuthManager
from database import SupabaseDB

# Cliente normal (login)
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Cliente admin (registro com bypass)
supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Criar managers
auth_manager = AuthManager(supabase, supabase_admin)
db = SupabaseDB(supabase)
