import flet as ft
from ui_components import *
from auth import session
from supabase_client import auth_manager


class LoginView(ft.View):
    
    
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success
        
        
        self.email_field = create_input("Email")
        self.password_field = create_input("Senha", password=True)
        
        super().__init__(
            route="/login",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=50),
                            create_title("ANDOR MISSIONS"),
                            ft.Text(
                                "Sistema de Missões Rebeldes",
                                size=16,
                                color=COLORS["text"],
                                opacity=0.7,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=30),
                            
                            # Card com layout simplificado
                            ft.Container(
                                content=ft.Column(
                                    [
                                        create_subtitle("Acessar Sistema"),
                                        ft.Container(height=10),
                                        self.email_field,
                                        self.password_field,
                                        ft.Container(height=10),
                                        create_button(
                                            "Entrar",
                                            self.handle_login,
                                            icon=ft.icons.LOGIN,
                                            expand=False,
                                        ),
                                        ft.Container(height=5),
                                        ft.Row(
                                            [
                                                ft.Text("Não tem conta?", color=COLORS["text"], opacity=0.7),
                                                ft.TextButton(
                                                    "Registrar",
                                                    on_click=lambda _: self.page.go("/register"),
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                    ],
                                    spacing=15,
                                ),
                                bgcolor=COLORS["secondary"],
                                padding=30,
                                border_radius=12,
                            ),
                            
                            ft.Container(height=20),
                            ft.Text(
                                '"As rebeliões são construídas na esperança."',
                                size=14,
                                color=COLORS["text"],
                                opacity=0.5,
                                italic=True,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=20,
                    expand=True,
                )
            ],
            bgcolor=COLORS["background"],
        )
    
    def handle_login(self, e):
        
        email = self.email_field.value
        password = self.password_field.value
        
        if not email or not password:
            show_snack(self.page, create_alert("Preencha todos os campos", is_error=True))
            return
        
      
        result = auth_manager.login(email, password)
        
        if result:
            
            session.login(result)
            
            show_snack(self.page, create_alert(f"Bem-vindo, {email}!"))
            
            
            self.on_login_success()
        else:
            show_snack(self.page, create_alert("Email ou senha incorretos", is_error=True))

