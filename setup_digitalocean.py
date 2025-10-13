"""
Script para configurar as tabelas no DigitalOcean PostgreSQL
Execute APENAS UMA VEZ: python setup_digitalocean.py
"""
import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_SSLMODE

print("="*60)
print("⚙️  CONFIGURAÇÃO - DIGITALOCEAN POSTGRESQL")
print("="*60)

print(f"\n📋 Este script vai criar:")
print(f"   ✅ Tabela 'users' (usuários)")
print(f"   ✅ Tabela 'missions' (missões)")
print(f"   ✅ Índices de performance")
print(f"   ✅ Dados de exemplo")

resposta = input(f"\n❓ Deseja continuar? (s/n): ")

if resposta.lower() != 's':
    print("❌ Operação cancelada!")
    exit()

print(f"\n⏳ Conectando ao banco de dados...")

try:
    # Conectar
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=DB_SSLMODE
    )
    
    print("✅ Conectado!")
    
    cursor = conn.cursor()
    
    # Ler script SQL
    print(f"\n⏳ Executando script SQL...")
    
    with open('init_digitalocean.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    cursor.execute(sql_script)
    conn.commit()
    
    print("✅ Script executado com sucesso!")
    
    # Verificar tabelas criadas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    print(f"\n📁 Tabelas criadas:")
    for table in tables:
        print(f"   ✅ {table[0]}")
    
    # Contar missões
    cursor.execute("SELECT COUNT(*) FROM missions;")
    count = cursor.fetchone()[0]
    print(f"\n📊 Missões de exemplo: {count}")
    
    cursor.close()
    conn.close()
    
    print(f"\n" + "="*60)
    print("🎉 Configuração concluída com sucesso!")
    print("="*60)
    print(f"\n🚀 Próximos passos:")
    print(f"   1. Execute: python main.py")
    print(f"   2. Registre um usuário admin")
    print(f"   3. Use o aplicativo!")
    print(f"\n💡 O banco agora funciona para:")
    print(f"   ✅ Desktop (seu PC)")
    print(f"   ✅ APK (Android)")
    print(f"   ✅ IPA (iOS)")
    print(f"   ✅ Web")
    print(f"   ✅ Qualquer lugar com internet!")
    
except FileNotFoundError:
    print(f"\n❌ Arquivo 'init_digitalocean.sql' não encontrado!")
    print(f"   Certifique-se de que está na pasta do projeto.")
    
except psycopg2.Error as e:
    print(f"\n❌ Erro ao executar SQL:")
    print(f"   {e}")
    if conn:
        conn.rollback()
    
except Exception as e:
    print(f"\n❌ Erro inesperado:")
    print(f"   {e}")
    
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
