import flet as ft

from ui_components import *
from database import db


class RegisterView(ft.View):
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.email_field = create_input("Email")
        self.password_field = create_input("Senha", password=True)
        self.password_confirm_field = create_input("Confirmar Senha", password=True)
        
        super().__init__(
            route="/register",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=30),
                            
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color=COLORS["text"],
                                on_click=lambda _: page.go("/login"),
                            ),
                            
                            create_title("NOVO AGENTE"),
                            ft.Text(
                                "Junte-se à Rebelião",
                                size=16,
                                color=COLORS["text"],
                                opacity=0.7,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=20),
                            
                            # Card de registro
                            ft.Container(
                                content=ft.Column(
                                    [
                                        self.email_field,
                                        self.password_field,
                                        self.password_confirm_field,
                                        ft.Container(height=10),
                                        create_button(
                                            "Registrar",
                                            self.handle_register,
                                            icon=ft.icons.PERSON_ADD,
                                            expand=False,
                                        ),
                                    ],
                                    spacing=15,
                                ),
                                bgcolor=COLORS["secondary"],
                                padding=30,
                                border_radius=12,
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
    
    def handle_register(self, e):
        email = self.email_field.value
        password = self.password_field.value
        password_confirm = self.password_confirm_field.value
        is_admin = False
        
        if not email or not password or not password_confirm:
            show_snack(self.page, create_alert("Preencha todos os campos", is_error=True))
            return
        
        if password != password_confirm:
            show_snack(self.page, create_alert("As senhas não coincidem", is_error=True))
            return
        
        if len(password) < 6:
            show_snack(self.page, create_alert("A senha deve ter pelo menos 6 caracteres", is_error=True))
            return
        
        result = db.register(email, password, is_admin)
        
        if result:
            show_snack(self.page, create_alert("Registro realizado com sucesso! Faça login."))
            self.page.go("/login")
        else:
            show_snack(self.page, create_alert("Erro ao registrar. Tente outro email.", is_error=True))
