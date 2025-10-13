import os
from dotenv import load_dotenv
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import psycopg2
from psycopg2 import pool
import bcrypt
import jwt
from datetime import datetime, timedelta

load_dotenv()

# Tema Star Wars Andor
THEME = {
    "bg_dark": [15/255, 13/255, 26/255, 1],
    "bg_medium": [42/255, 37/255, 53/255, 1],
    "card_bg": [51/255, 45/255, 66/255, 1],
    "primary": [233/255, 69/255, 96/255, 1],
    "accent": [255/255, 107/255, 133/255, 1],
    "text_white": [1, 1, 1, 1],
    "text_gray": [184/255, 181/255, 194/255, 1],
    "success": [0, 200/255, 83/255, 1],
    "warning": [255/255, 167/255, 38/255, 1],
    "error": [244/255, 67/255, 54/255, 1],
    "critical": [211/255, 47/255, 47/255, 1]
}

# Pool de conexões
connection_pool = None

def init_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            sslmode='require'
        )

def get_conn():
    return connection_pool.getconn()

def return_conn(conn):
    connection_pool.putconn(conn)

def hash_pwd(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_pwd(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_token(user_id, email, is_admin):
    payload = {
        'user_id': user_id,
        'email': email,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, os.getenv('SECRET_KEY', 'andor-secret'), algorithm='HS256')


# TELA DE LOGIN
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        
        layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        layout.md_bg_color = THEME["bg_dark"]
        
        # Espaçador
        layout.add_widget(MDLabel(text='', size_hint_y=0.3))
        
        # Título
        title = MDLabel(
            text='[b]ANDOR[/b]\nMISSÕES REBELDES',
            markup=True,
            halign='center',
            font_style='H4',
            theme_text_color='Custom',
            text_color=THEME["primary"],
            size_hint_y=None,
            height=dp(100)
        )
        layout.add_widget(title)
        
        # Card de login
        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint=(None, None),
            size=(dp(320), dp(280)),
            pos_hint={'center_x': 0.5},
            md_bg_color=THEME["card_bg"],
            elevation=8
        )
        
        self.email_field = MDTextField(
            hint_text='Email',
            mode='rectangle',
            size_hint_x=1,
            icon_left='email'
        )
        card.add_widget(self.email_field)
        
        self.password_field = MDTextField(
            hint_text='Senha',
            mode='rectangle',
            password=True,
            size_hint_x=1,
            icon_left='lock'
        )
        card.add_widget(self.password_field)
        
        login_btn = MDRaisedButton(
            text='ENTRAR',
            size_hint_x=1,
            md_bg_color=THEME["primary"],
            on_release=self.do_login
        )
        card.add_widget(login_btn)
        
        self.error_label = MDLabel(
            text='',
            halign='center',
            theme_text_color='Custom',
            text_color=THEME["error"],
            size_hint_y=None,
            height=dp(30),
            font_size=sp(12)
        )
        card.add_widget(self.error_label)
        
        layout.add_widget(card)
        
        register_btn = MDFlatButton(
            text='Criar nova conta',
            pos_hint={'center_x': 0.5},
            on_release=self.go_register
        )
        layout.add_widget(register_btn)
        
        layout.add_widget(MDLabel(text='', size_hint_y=0.3))
        
        self.add_widget(layout)
    
    def go_register(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'register'
    
    def do_login(self, *args):
        email = self.email_field.text.strip()
        password = self.password_field.text
        
        if not email or not password:
            self.error_label.text = 'Preencha todos os campos'
            return
        
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, is_admin FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            return_conn(conn)
            
            if user and verify_pwd(password, user[2]):
                token = create_token(user[0], user[1], user[3])
                dashboard = self.manager.get_screen('dashboard')
                dashboard.user_data = {
                    'id': user[0],
                    'email': user[1],
                    'is_admin': user[3],
                    'token': token
                }
                dashboard.load_missions()
                self.manager.transition = SlideTransition(direction='left')
                self.manager.current = 'dashboard'
                self.email_field.text = ''
                self.password_field.text = ''
                self.error_label.text = ''
            else:
                self.error_label.text = 'Email ou senha incorretos'
        except Exception as e:
            self.error_label.text = f'Erro: {str(e)}'


# TELA DE REGISTRO
class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register'
        
        layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        layout.md_bg_color = THEME["bg_dark"]
        
        layout.add_widget(MDLabel(text='', size_hint_y=0.2))
        
        title = MDLabel(
            text='[b]NOVA CONTA[/b]',
            markup=True,
            halign='center',
            font_style='H4',
            theme_text_color='Custom',
            text_color=THEME["primary"],
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(title)
        
        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint=(None, None),
            size=(dp(320), dp(350)),
            pos_hint={'center_x': 0.5},
            md_bg_color=THEME["card_bg"],
            elevation=8
        )
        
        self.email_field = MDTextField(
            hint_text='Email',
            mode='rectangle',
            icon_left='email'
        )
        card.add_widget(self.email_field)
        
        self.password_field = MDTextField(
            hint_text='Senha (mínimo 6 caracteres)',
            mode='rectangle',
            password=True,
            icon_left='lock'
        )
        card.add_widget(self.password_field)
        
        self.confirm_field = MDTextField(
            hint_text='Confirmar senha',
            mode='rectangle',
            password=True,
            icon_left='lock-check'
        )
        card.add_widget(self.confirm_field)
        
        register_btn = MDRaisedButton(
            text='CRIAR CONTA',
            size_hint_x=1,
            md_bg_color=THEME["success"],
            on_release=self.do_register
        )
        card.add_widget(register_btn)
        
        self.message_label = MDLabel(
            text='',
            halign='center',
            theme_text_color='Custom',
            text_color=THEME["error"],
            size_hint_y=None,
            height=dp(40),
            font_size=sp(12)
        )
        card.add_widget(self.message_label)
        
        layout.add_widget(card)
        
        back_btn = MDFlatButton(
            text='Voltar ao login',
            pos_hint={'center_x': 0.5},
            on_release=self.go_login
        )
        layout.add_widget(back_btn)
        
        layout.add_widget(MDLabel(text='', size_hint_y=0.2))
        
        self.add_widget(layout)
    
    def go_login(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'
    
    def do_register(self, *args):
        email = self.email_field.text.strip()
        password = self.password_field.text
        confirm = self.confirm_field.text
        
        if not email or not password or not confirm:
            self.message_label.text = 'Preencha todos os campos'
            self.message_label.text_color = THEME["error"]
            return
        
        if password != confirm:
            self.message_label.text = 'As senhas não coincidem'
            self.message_label.text_color = THEME["error"]
            return
        
        if len(password) < 6:
            self.message_label.text = 'Senha muito curta (mín. 6)'
            self.message_label.text_color = THEME["error"]
            return
        
        try:
            conn = get_conn()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                self.message_label.text = 'Email já cadastrado'
                self.message_label.text_color = THEME["error"]
                cursor.close()
                return_conn(conn)
                return
            
            password_hash = hash_pwd(password)
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, password_hash)
            )
            conn.commit()
            cursor.close()
            return_conn(conn)
            
            self.message_label.text = 'Conta criada com sucesso!'
            self.message_label.text_color = THEME["success"]
            
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.go_login(), 1.5)
        except Exception as e:
            self.message_label.text = f'Erro: {str(e)}'
            self.message_label.text_color = THEME["error"]


# CARD DE MISSÃO
class MissionCard(MDCard):
    def __init__(self, mission, callback, **kwargs):
        super().__init__(**kwargs)
        self.mission = mission
        self.callback = callback
        
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(340), dp(200))
        self.padding = dp(15)
        self.spacing = dp(10)
        self.md_bg_color = THEME["card_bg"]
        self.elevation = 4
        
        # Header: nome + status
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35))
        
        name = MDLabel(
            text=f'[b]{mission[1]}[/b]',
            markup=True,
            theme_text_color='Custom',
            text_color=THEME["text_white"],
            font_size=sp(16),
            size_hint_x=0.65
        )
        header.add_widget(name)
        
        # Status badge
        status_colors = {
            'pending': THEME["warning"],
            'active': THEME["accent"],
            'completed': THEME["success"],
            'critical': THEME["critical"]
        }
        status_names = {
            'pending': 'PENDENTE',
            'active': 'ATIVA',
            'completed': 'COMPLETA',
            'critical': 'CRÍTICA'
        }
        
        status_box = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(100), dp(28)),
            md_bg_color=status_colors.get(mission[4], THEME["text_gray"]),
            radius=[14, 14, 14, 14],
            padding=[dp(8), 0]
        )
        status_lbl = MDLabel(
            text=status_names.get(mission[4], mission[4].upper()),
            halign='center',
            theme_text_color='Custom',
            text_color=THEME["text_white"],
            font_size=sp(10),
            bold=True
        )
        status_box.add_widget(status_lbl)
        header.add_widget(status_box)
        
        self.add_widget(header)
        
        # Local
        location = MDLabel(
            text=f'Local: {mission[2]}',
            theme_text_color='Custom',
            text_color=THEME["accent"],
            font_size=sp(13),
            size_hint_y=None,
            height=dp(20)
        )
        self.add_widget(location)
        
        # Descrição preview
        desc_preview = mission[3][:150] + '...' if len(mission[3]) > 150 else mission[3]
        desc = Label(
            text=desc_preview,
            color=THEME["text_gray"],
            font_size=sp(12),
            size_hint_y=None,
            height=dp(60),
            text_size=(dp(310), None),
            halign='left',
            valign='top'
        )
        self.add_widget(desc)
        
        # Footer: perigo + botão
        footer = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35))
        
        danger = mission[5]
        danger_levels = {1: 'BAIXO', 2: 'MODERADO', 3: 'ALTO', 4: 'EXTREMO', 5: 'CRÍTICO'}
        danger_lbl = MDLabel(
            text=f'Perigo: {danger_levels.get(danger, "ALTO")} ({danger}/5)',
            theme_text_color='Custom',
            text_color=THEME["warning"] if danger >= 4 else THEME["text_gray"],
            font_size=sp(11),
            size_hint_x=0.6
        )
        footer.add_widget(danger_lbl)
        
        btn = MDRaisedButton(
            text='DETALHES',
            size_hint=(None, None),
            size=(dp(100), dp(32)),
            md_bg_color=THEME["primary"],
            font_size=sp(11),
            on_release=lambda x: self.callback(mission)
        )
        footer.add_widget(btn)
        
        self.add_widget(footer)


# DASHBOARD
class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.user_data = {}
        
        layout = MDBoxLayout(orientation='vertical')
        layout.md_bg_color = THEME["bg_dark"]
        
        # Header
        header = MDBoxLayout(
            orientation='horizontal',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(60),
            md_bg_color=THEME["bg_medium"]
        )
        
        logo = MDLabel(
            text='[b]ANDOR[/b]',
            markup=True,
            font_style='H6',
            theme_text_color='Custom',
            text_color=THEME["primary"],
            size_hint_x=None,
            width=dp(80)
        )
        header.add_widget(logo)
        
        self.user_label = MDLabel(
            text='',
            theme_text_color='Custom',
            text_color=THEME["text_gray"],
            font_size=sp(13)
        )
        header.add_widget(self.user_label)
        
        exit_btn = MDIconButton(
            icon='exit-to-app',
            theme_text_color='Custom',
            text_color=THEME["error"],
            on_release=self.logout
        )
        header.add_widget(exit_btn)
        
        layout.add_widget(header)
        
        # Área de missões
        scroll = MDScrollView()
        self.missions_box = MDBoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(15),
            size_hint_y=None
        )
        self.missions_box.bind(minimum_height=self.missions_box.setter('height'))
        scroll.add_widget(self.missions_box)
        
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def load_missions(self):
        self.missions_box.clear_widgets()
        
        title = MDLabel(
            text='[b]MISSÕES DISPONÍVEIS[/b]',
            markup=True,
            halign='center',
            font_style='H5',
            theme_text_color='Custom',
            text_color=THEME["primary"],
            size_hint_y=None,
            height=dp(40)
        )
        self.missions_box.add_widget(title)
        
        subtitle = MDLabel(
            text='A rebelião precisa de você',
            halign='center',
            theme_text_color='Custom',
            text_color=THEME["text_gray"],
            font_size=sp(13),
            size_hint_y=None,
            height=dp(25)
        )
        self.missions_box.add_widget(subtitle)
        
        try:
            conn = get_conn()
            cursor = conn.cursor()
            
            if self.user_data.get('is_admin'):
                cursor.execute("SELECT id, name, location, description, status, danger_level FROM missions ORDER BY danger_level DESC")
            else:
                cursor.execute("SELECT id, name, location, description, status, danger_level FROM missions WHERE status IN ('pending', 'active', 'critical') ORDER BY danger_level DESC")
            
            missions = cursor.fetchall()
            cursor.close()
            return_conn(conn)
            
            for mission in missions:
                card = MissionCard(mission, self.show_details)
                card_box = MDBoxLayout(size_hint_y=None, height=dp(200))
                card_box.add_widget(MDLabel(text=''))
                card_box.add_widget(card)
                card_box.add_widget(MDLabel(text=''))
                self.missions_box.add_widget(card_box)
        
        except Exception as e:
            error = MDLabel(
                text=f'Erro ao carregar: {str(e)}',
                halign='center',
                theme_text_color='Custom',
                text_color=THEME["error"]
            )
            self.missions_box.add_widget(error)
        
        if self.user_data:
            role = 'ADMIN' if self.user_data.get('is_admin') else 'REBELDE'
            self.user_label.text = f'{role} | {self.user_data.get("email", "")}'
    
    def show_details(self, mission):
        # Container do modal
        content = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Nome
        name_lbl = MDLabel(
            text=f'[b]{mission[1]}[/b]',
            markup=True,
            font_style='H5',
            theme_text_color='Custom',
            text_color=THEME["primary"],
            size_hint_y=None,
            height=dp(35)
        )
        content.add_widget(name_lbl)
        
        # Info
        status_names = {
            'pending': 'PENDENTE',
            'active': 'ATIVA',
            'completed': 'COMPLETA',
            'critical': 'CRÍTICA'
        }
        
        danger_levels = {1: 'BAIXO', 2: 'MODERADO', 3: 'ALTO', 4: 'EXTREMO', 5: 'CRÍTICO'}
        danger_text = danger_levels.get(mission[5], 'ALTO')
        info_text = f"Status: {status_names.get(mission[4], mission[4].upper())}\nLocal: {mission[2]}\nNível de Perigo: {danger_text} ({mission[5]}/5)"
        
        info_lbl = Label(
            text=info_text,
            color=THEME["text_white"],
            font_size=sp(13),
            size_hint_y=None,
            height=dp(70),
            text_size=(Window.width * 0.7, None),
            halign='left',
            valign='top'
        )
        content.add_widget(info_lbl)
        
        # Título descrição
        desc_title = MDLabel(
            text='[b]DESCRIÇÃO:[/b]',
            markup=True,
            theme_text_color='Custom',
            text_color=THEME["primary"],
            font_size=sp(14),
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(desc_title)
        
        # Descrição completa em scroll
        desc_scroll = ScrollView(size_hint=(1, None), height=dp(250), bar_width=dp(6))
        
        desc_text = Label(
            text=mission[3],
            color=THEME["text_white"],
            font_size=sp(13),
            size_hint_y=None,
            text_size=(Window.width * 0.7, None),
            padding=(dp(10), dp(10)),
            halign='left',
            valign='top'
        )
        desc_text.bind(texture_size=lambda *x: setattr(desc_text, 'height', desc_text.texture_size[1] + dp(20)))
        
        desc_scroll.add_widget(desc_text)
        content.add_widget(desc_scroll)
        
        # Dialog
        self.dialog = MDDialog(
            type='custom',
            content_cls=content,
            size_hint=(0.9, 0.85),
            buttons=[
                MDFlatButton(
                    text='FECHAR',
                    theme_text_color='Custom',
                    text_color=THEME["accent"],
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def logout(self, *args):
        self.user_data = {}
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


# APP
class AndorMissionsApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        
        Window.size = (400, 700)
        
        init_pool()
        
        sm = MDScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(RegisterScreen())
        sm.add_widget(DashboardScreen())
        
        return sm
    
    def on_stop(self):
        if connection_pool:
            connection_pool.closeall()


if __name__ == '__main__':
    AndorMissionsApp().run()
