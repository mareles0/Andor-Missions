# Andor Missions 🚀

Sistema de gerenciamento de missões inspirado em Star Wars: Andor, desenvolvido com Flet e Supabase.

## 📱 Recursos

- ✅ Autenticação de usuários (login/registro)
- ✅ Dashboard de usuário para visualizar missões
- ✅ Dashboard administrativo para CRUD completo de missões
- ✅ Interface responsiva e moderna
- ✅ Tema escuro inspirado em Star Wars
- ✅ Sistema de busca de missões
- ✅ Níveis de perigo e status das missões

## 🛠️ Tecnologias

- **Frontend/Backend**: Python + Flet (Web App)
- **Banco de Dados**: Supabase (PostgreSQL + Auth)
- **HTTP Client**: httpx
- **Deploy**: Render.com

## 🚀 Como Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/mareles0/trabalho-lucas.git
cd trabalho-lucas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Adicione suas credenciais do Supabase

4. Execute o aplicativo:
```bash
python main.py
```

5. Acesse no navegador: `http://localhost:8550`

## 🌐 Deploy no Render

### Método 1: Blueprint (Automático)

1. Faça fork/clone deste repositório
2. Acesse [Render Dashboard](https://dashboard.render.com/)
3. Clique em "New" → "Blueprint"
4. Conecte seu repositório GitHub
5. O Render vai detectar o `render.yaml` automaticamente
6. Configure as variáveis de ambiente:
   - `SUPABASE_URL`: URL do seu projeto Supabase
   - `SUPABASE_ANON_KEY`: Chave anônima do Supabase
   - `SUPABASE_SERVICE_ROLE_KEY`: Chave de serviço do Supabase

### Método 2: Manual

1. Acesse [Render Dashboard](https://dashboard.render.com/)
2. Clique em "New" → "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `andor-missions`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free
5. Adicione as variáveis de ambiente (mesmas do método 1)
6. Clique em "Create Web Service"

## 📋 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anonima
SUPABASE_SERVICE_ROLE_KEY=sua-chave-service-role
```

⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` no Git! Ele já está no `.gitignore`.

## 🗄️ Estrutura do Banco de Dados

### Tabela: missions

```sql
CREATE TABLE missions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  location TEXT NOT NULL,
  description TEXT NOT NULL,
  danger_level TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Autenticação

Utiliza o Supabase Auth com:
- Campo `user_metadata.is_admin` para controle de permissões
- RLS (Row Level Security) ativado

## 👤 Usuários de Teste

- **Admin**:
  - Email: `admin@andor.com`
  - Senha: `admin123`

## 📁 Estrutura do Projeto

```
trabalho-lucas/
├── .env                    # Variáveis de ambiente (não commitado)
├── .gitignore             # Arquivos ignorados pelo Git
├── auth.py                # Sistema de autenticação
├── config.py              # Configurações da aplicação
├── database.py            # Operações de banco de dados
├── main.py                # Ponto de entrada da aplicação
├── requirements.txt       # Dependências Python
├── supabase_client.py     # Cliente Supabase singleton
├── ui_components.py       # Componentes de UI reutilizáveis
├── render.yaml            # Configuração do Render
└── views/                 # Telas da aplicação
    ├── login_view.py      # Tela de login
    ├── register_view.py   # Tela de registro
    ├── user_view.py       # Dashboard do usuário
    └── admin_view.py      # Dashboard administrativo
```

## 🎨 Paleta de Cores

Inspirada em Star Wars: Andor:
- Background: `#0A0E27` (Azul escuro espacial)
- Primary: `#1E88E5` (Azul Imperial)
- Secondary: `#424242` (Cinza metálico)
- Surface: `#1A1F3A` (Azul escuro cards)

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👨‍💻 Desenvolvedor

Desenvolvido com ❤️ para o trabalho acadêmico.
