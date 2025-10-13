
from typing import Optional, List, Dict, Any
import httpx
from config import SUPABASE_URL, SUPABASE_ANON_KEY


class SupabaseDB:
    """Gerencia operações de banco de dados usando Supabase REST API"""
    
    def __init__(self, supabase_client=None):
        self.base_url = f"{SUPABASE_URL}/rest/v1"
        self.anon_key = SUPABASE_ANON_KEY
        print("✅ Supabase client inicializado com sucesso!")
    
    def _get_headers(self, access_token: str = None) -> dict:
        """Retorna headers com token de autenticação"""
        token = access_token or self.anon_key
        return {
            "apikey": self.anon_key,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    # ====================
    # MÉTODOS DE MISSÕES
    # ====================
    
    def get_missions(self, access_token: str = None) -> List[Dict[str, Any]]:
        """Retorna todas as missões ordenadas por data de criação"""
        try:
            with httpx.Client() as client:
                response = client.get(
                    f"{self.base_url}/missions?order=created_at.desc",
                    headers=self._get_headers(access_token)
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"❌ Erro ao buscar missões: {e}")
            return []
    
    
    def search_missions(self, search_term: str, access_token: str = None) -> List[Dict[str, Any]]:
        """Busca missões por termo (nome, localização ou descrição)"""
        try:
            with httpx.Client() as client:
                # Busca usando or com ilike
                query = f"or=(name.ilike.%{search_term}%,location.ilike.%{search_term}%,description.ilike.%{search_term}%)&order=created_at.desc"
                response = client.get(
                    f"{self.base_url}/missions?{query}",
                    headers=self._get_headers(access_token)
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"❌ Erro ao buscar missões: {e}")
            return []
    
    def get_mission_by_id(self, mission_id: int, access_token: str = None) -> Optional[Dict[str, Any]]:
        """Retorna uma missão específica por ID"""
        try:
            with httpx.Client() as client:
                response = client.get(
                    f"{self.base_url}/missions?id=eq.{mission_id}",
                    headers=self._get_headers(access_token)
                )
                response.raise_for_status()
                data = response.json()
                return data[0] if data else None
        except Exception as e:
            print(f"❌ Erro ao buscar missão: {e}")
            return None
    
    def create_mission(self, name: str, location: str, description: str,
                      status: str = "pending", danger_level: int = 1, access_token: str = None) -> Optional[Dict[str, Any]]:
        """Cria uma nova missão"""
        try:
            with httpx.Client() as client:
                payload = {
                    "name": name,
                    "location": location,
                    "description": description,
                    "status": status,
                    "danger_level": danger_level
                }
                response = client.post(
                    f"{self.base_url}/missions",
                    headers=self._get_headers(access_token),
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                if data:
                    print(f"✅ Missão criada: {name}")
                    return data[0] if isinstance(data, list) else data
                return None
        except Exception as e:
            print(f"❌ Erro ao criar missão: {e}")
            return None
    
    def update_mission(self, mission_id: int, name: str = None, location: str = None,
                      description: str = None, status: str = None,
                      danger_level: int = None, access_token: str = None) -> Optional[Dict[str, Any]]:
        """Atualiza uma missão existente"""
        try:
            updates = {}
            if name is not None:
                updates["name"] = name
            if location is not None:
                updates["location"] = location
            if description is not None:
                updates["description"] = description
            if status is not None:
                updates["status"] = status
            if danger_level is not None:
                updates["danger_level"] = danger_level
            
            if not updates:
                return None
            
            with httpx.Client() as client:
                response = client.patch(
                    f"{self.base_url}/missions?id=eq.{mission_id}",
                    headers=self._get_headers(access_token),
                    json=updates
                )
                response.raise_for_status()
                data = response.json()
                if data:
                    print(f"✅ Missão atualizada: ID {mission_id}")
                    return data[0] if isinstance(data, list) else data
                return None
        except Exception as e:
            print(f"❌ Erro ao atualizar missão: {e}")
            return None
    
    def delete_mission(self, mission_id: int, access_token: str = None) -> bool:
        """Deleta uma missão"""
        try:
            with httpx.Client() as client:
                response = client.delete(
                    f"{self.base_url}/missions?id=eq.{mission_id}",
                    headers=self._get_headers(access_token)
                )
                response.raise_for_status()
                print(f"✅ Missão deletada: ID {mission_id}")
                return True
        except Exception as e:
            print(f"❌ Erro ao deletar missão: {e}")
            return False


# Nota: db será inicializado no supabase_client.py
db = None

