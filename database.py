
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2 import pool
    USE_POSTGRES = True
except ImportError:
    USE_POSTGRES = False
    
import bcrypt
from typing import Optional, List, Dict, Any
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_SSLMODE


class DatabaseConnection:
    
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        
        if cls._connection_pool is None:
            try:
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    1, 20,
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    sslmode=DB_SSLMODE
                )
                print("✅ Pool de conexões inicializado com sucesso!")
                print(f"🌐 Conectado ao PostgreSQL: {DB_HOST}")
            except Exception as e:
                print(f"❌ Erro ao inicializar pool: {e}")
                raise
    
    @classmethod
    def get_connection(cls):
        
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, connection):
        
        if cls._connection_pool:
            cls._connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        
        if cls._connection_pool:
            cls._connection_pool.closeall()


class PostgresDB:
    
    
    def __init__(self):
        DatabaseConnection.initialize_pool()
    
    def _get_cursor(self):
        
        conn = DatabaseConnection.get_connection()
        return conn, conn.cursor(cursor_factory=RealDictCursor)
    
    def _close_cursor(self, conn, cursor):
        
        cursor.close()
        DatabaseConnection.return_connection(conn)
    
    
    
    def register(self, email: str, password: str, is_admin: bool = False) -> Optional[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute(
                """
                INSERT INTO users (email, password_hash, is_admin)
                VALUES (%s, %s, %s)
                RETURNING id, email, is_admin, created_at
                """,
                (email, password_hash, is_admin)
            )
            
            conn.commit()
            user = dict(cursor.fetchone())
            print(f"✅ Usuário registrado: {email}")
            return user
            
        except psycopg2.IntegrityError:
            if conn:
                conn.rollback()
            print(f"❌ Email já existe: {email}")
            return None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao registrar: {e}")
            return None
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            
            cursor.execute(
                "SELECT id, email, password_hash, is_admin FROM users WHERE email = %s",
                (email,)
            )
            
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                user_dict = dict(user)
                user_dict.pop('password_hash')  
                print(f"✅ Login bem-sucedido: {email}")
                return user_dict
            
            print(f"❌ Credenciais inválidas para: {email}")
            return None
            
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return None
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    
    
    def get_missions(self) -> List[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            cursor.execute("SELECT * FROM missions ORDER BY created_at DESC")
            missions = [dict(row) for row in cursor.fetchall()]
            return missions
        except Exception as e:
            print(f"❌ Erro ao buscar missões: {e}")
            return []
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    def search_missions(self, search_term: str) -> List[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            cursor.execute(
                """
                SELECT * FROM missions 
                WHERE name ILIKE %s OR location ILIKE %s OR description ILIKE %s
                ORDER BY created_at DESC
                """,
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            )
            missions = [dict(row) for row in cursor.fetchall()]
            return missions
        except Exception as e:
            print(f"❌ Erro ao buscar missões: {e}")
            return []
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    def get_mission_by_id(self, mission_id: int) -> Optional[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            cursor.execute("SELECT * FROM missions WHERE id = %s", (mission_id,))
            mission = cursor.fetchone()
            return dict(mission) if mission else None
        except Exception as e:
            print(f"❌ Erro ao buscar missão: {e}")
            return None
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    def create_mission(self, name: str, location: str, description: str,
                      status: str = "pending", danger_level: int = 1) -> Optional[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            cursor.execute(
                """
                INSERT INTO missions (name, location, description, status, danger_level)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (name, location, description, status, danger_level)
            )
            conn.commit()
            mission = dict(cursor.fetchone())
            print(f"✅ Missão criada: {name}")
            return mission
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao criar missão: {e}")
            return None
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    def update_mission(self, mission_id: int, name: str = None, location: str = None,
                      description: str = None, status: str = None,
                      danger_level: int = None) -> Optional[Dict[str, Any]]:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            
            
            updates = []
            values = []
            
            if name is not None:
                updates.append("name = %s")
                values.append(name)
            if location is not None:
                updates.append("location = %s")
                values.append(location)
            if description is not None:
                updates.append("description = %s")
                values.append(description)
            if status is not None:
                updates.append("status = %s")
                values.append(status)
            if danger_level is not None:
                updates.append("danger_level = %s")
                values.append(danger_level)
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(mission_id)
            
            query = f"UPDATE missions SET {', '.join(updates)} WHERE id = %s RETURNING *"
            cursor.execute(query, values)
            
            conn.commit()
            mission = cursor.fetchone()
            if mission:
                print(f"✅ Missão atualizada: ID {mission_id}")
                return dict(mission)
            return None
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao atualizar missão: {e}")
            return None
        finally:
            if cursor:
                self._close_cursor(conn, cursor)
    
    def delete_mission(self, mission_id: int) -> bool:
        
        conn, cursor = None, None
        try:
            conn, cursor = self._get_cursor()
            cursor.execute("DELETE FROM missions WHERE id = %s", (mission_id,))
            conn.commit()
            print(f"✅ Missão deletada: ID {mission_id}")
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao deletar missão: {e}")
            return False
        finally:
            if cursor:
                self._close_cursor(conn, cursor)



db = PostgresDB()

