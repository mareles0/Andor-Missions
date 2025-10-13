"""
Script para atualizar as descrições das missões no banco DigitalOcean
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Novas descrições detalhadas
NEW_DESCRIPTIONS = {
    "Infiltração em Ferrix": """Ferrix é um planeta de salvamento industrial no sistema Morlana, controlado pela corporação Pre-Mor. Após o incidente onde Cassian Andor matou dois guardas corporativos, o Império ocupou permanentemente o planeta. Esta missão visa infiltrar-se nos distritos industriais de Ferrix para recuperar informações cruciais sobre o novo projeto imperial de manufatura de armas. A operação deve ser realizada durante o toque do sino de Rix Road, quando os trabalhadores trocam turnos, aproveitando a confusão nas ruas estreitas e nebulosas da cidade. O perigo é elevado devido à forte presença de stormtroopers e à vigilância constante dos colaboradores imperiais locais.""",
    
    "Resgate em Narkina 5": """Narkina 5 é uma lua aquática orbitando o gigante gasoso Narkina, lar do infame Complexo Prisional Imperial. Prisioneiros trabalham em turnos de 12 horas fabricando fixadores EP-N5 para a máquina de guerra imperial. Cassian Andor foi falsamente condenado a 6 anos de prisão nesta instalação em 5 BBY. Esta missão bem-sucedida libertou dezenas de prisioneiros após uma ousada fuga através da superfície rochosa da lua, passando por mesas e praias até alcançar um ponto de extração seguro. A operação expôs as brutais condições de trabalho forçado do Império e marcou uma importante vitória para a Rebelião nascente.""",
    
    "Sabotagem em Morlana One": """Morlana One é o mundo principal do sistema Morlani, servindo como sede da Corporação Preox-Morlana no setor de Comércio Livre. Após os incidentes envolvendo Cassian Andor, o Império assumiu controle permanente do sistema, transformando-o em um hub de vigilância e controle corporativo. Esta missão de sabotagem visa desativar o Centro de Comunicações Corporativas localizado nas instalações imperiais, impedindo coordenação entre patrulhas e atrasando reforços em operações futuras. A operação deve ser realizada à noite, quando a Zona de Lazer próxima está movimentada, fornecendo cobertura adicional. O risco moderado vem da presença de forças de segurança corporativa bem equipadas e sistemas de alarme sofisticados.""",
    
    "Reconhecimento em Aldhani": """Aldhani é um mundo sagrado conhecido pelo fenômeno celestial chamado "Olho de Aldhani", onde partículas de cristal meteóricas iluminam o céu. O Império construiu uma fortaleza-barragem neste planeta para armazenar a folha de pagamento trimestral de todo um setor. Esta missão de reconhecimento visa observar padrões de patrulha, rotações de guarda e movimentação de tropas imperiais ao redor da instalação. Os dados coletados serão cruciais para uma futura operação de maior escala. A equipe deve permanecer oculta nos vales e colinas ao redor da barragem, evitando peregrinos locais que visitam o planeta durante festivais. O perigo é relativamente baixo desde que a equipe mantenha distância e não seja detectada pelos sistemas de vigilância imperial.""",
    
    "Extração em Coruscant": """Coruscant, a capital galática e throneworld do Império, é um ecumenópolis de um trilhão de habitantes distribuídos em milhares de níveis verticais. Durante a era Imperial, o planeta tornou-se o centro do poder de Palpatine, com o antigo Templo Jedi transformado no Palácio Imperial. Esta perigosa missão de extração visa resgatar um informante de alto valor infiltrado no Bureau de Segurança Imperial antes que sua cobertura seja descoberta. A operação requer navegação pelos níveis superiores altamente vigiados da cidade-planeta, evitando checkpoints de stormtroopers e scanners de identificação onipresentes. O agente deve ser extraído através dos níveis inferiores de CoCo Town, uma área com resistência ativa, até um ponto de embarque secreto. Este é um dos trabalhos mais perigosos da Rebelião, operando no coração do poder imperial.""",
    
    "Sabotagem em Scarif": """Scarif é um planeta tropical paradisíaco transformado em fortaleza militar ultra-secreta do Império. Protegido por um escudo planetário massivo e pela temível nave capital Perseguidor Estelar classe Executor, Scarif abriga o Centro de Dados Imperial onde os planos da Estrela da Morte estão armazenados. Esta missão histórica, liderada por Jyn Erso e Cassian Andor em 0 BBY, resultou na transmissão bem-sucedida dos planos da superarma para a Aliança Rebelde. A operação custou a vida de toda a equipe Rogue One, mas forneceu à Rebelião a fraqueza fatal da Estrela da Morte - o reator térmico de exaustão. Este sacrifício heroico culminou na destruição da estação de batalha durante a Batalha de Yavin, marcando a primeira grande vitória rebelde contra o Império.""",
}

def update_descriptions():
    """Atualiza as descrições no banco DigitalOcean"""
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            sslmode="require"
        )
        
        cursor = conn.cursor()
        
        print("🔄 Atualizando descrições das missões...\n")
        
        # Atualizar cada missão
        for mission_name, description in NEW_DESCRIPTIONS.items():
            cursor.execute(
                "UPDATE missions SET description = %s WHERE name = %s",
                (description, mission_name)
            )
            print(f"✅ Atualizado: {mission_name}")
        
        # Commit das alterações
        conn.commit()
        
        print("\n🎉 Todas as descrições foram atualizadas com sucesso!")
        print("\n📊 Verificando atualização...")
        
        # Verificar
        cursor.execute("SELECT name, LEFT(description, 50) FROM missions ORDER BY id")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}...")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao atualizar descrições: {e}")

if __name__ == "__main__":
    update_descriptions()
