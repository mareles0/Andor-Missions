import os
import psycopg2
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Conectar ao banco DigitalOcean
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    sslmode='require'
)

cursor = conn.cursor()

print("🚀 Adicionando missão de Ghorman...")

# Inserir a missão de Ghorman
ghorman_mission = {
    "name": "Massacre de Ghorman",
    "location": "Ghorman, Palmo Plaza",
    "description": """Ghorman é um mundo orgulhoso do Setor Sern, conhecido pela produção de seda e twill ghorman, com uma população que valoriza profundamente sua língua e cultura. Em 2 BBY, o Império planejou extrair kalkite do planeta através de mineração invasiva para o Projeto Stardust, a Estrela da Morte. O ISB, liderado pela Supervisora Dedra Meero, manipulou a Frente Ghorman para radicalizar a população. Em um dia fatídico, milhares de ghormans pacíficos se reuniram na Palmo Plaza cantando o hino nacional "Gambol dum Ghor" (Nós Somos os Ghor). O Império cercou a multidão, encenou um tiroteio falso e abriu fogo indiscriminadamente. Tropas imperiais e droides KX-series massacraram aproximadamente 80.000 civis desarmados nas ruas. Este horror levou Mon Mothma a denunciar publicamente o Imperador Palpatine, criando a Aliança Rebelde. É a missão mais crucial e perigosa, pois expôs a verdadeira face do Império para toda a galáxia. O grito "A galáxia está assistindo!" ecoou por todos os sistemas estelares.""",
    "status": "critical",
    "danger_level": 5
}

# Verificar se a missão já existe
cursor.execute("SELECT id FROM missions WHERE name = %s", (ghorman_mission["name"],))
existing = cursor.fetchone()

if existing:
    # Atualizar se já existe
    cursor.execute("""
        UPDATE missions 
        SET location = %s, description = %s, status = %s, danger_level = %s, updated_at = CURRENT_TIMESTAMP
        WHERE name = %s
    """, (
        ghorman_mission["location"],
        ghorman_mission["description"],
        ghorman_mission["status"],
        ghorman_mission["danger_level"],
        ghorman_mission["name"]
    ))
    print(f"✅ Atualizado: {ghorman_mission['name']}")
else:
    # Inserir se não existe
    cursor.execute("""
        INSERT INTO missions (name, location, description, status, danger_level)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        ghorman_mission["name"],
        ghorman_mission["location"],
        ghorman_mission["description"],
        ghorman_mission["status"],
        ghorman_mission["danger_level"]
    ))
    print(f"✅ Inserido: {ghorman_mission['name']}")

conn.commit()

# Verificar resultado
print("\n📊 Verificando missão...")
cursor.execute("SELECT name, location, LEFT(description, 100) FROM missions WHERE name = %s", (ghorman_mission["name"],))
result = cursor.fetchone()
if result:
    print(f"\n   Nome: {result[0]}")
    print(f"   Local: {result[1]}")
    print(f"   Descrição: {result[2]}...")

cursor.close()
conn.close()

print("\n🎉 Missão de Ghorman adicionada com sucesso!")
print("🔄 Reinicie o aplicativo para ver a nova missão.")
