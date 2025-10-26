import flet as ft

from ui_components import *
from supabase_client import auth_manager


class RegisterView(ft.View):
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.email_field = create_input("Email")
        self.password_field = create_input("Senha", password=True)
        self.password_confirm_field = create_input("Confirmar Senha", password=True)
        # criar card interno e wrapper para responsividade semelhante ao login
        self._card_inner = ft.Container(
            content=ft.Column(
                [
                    self.email_field,
                    self.password_field,
                    self.password_confirm_field,
                    ft.Container(height=10),
                    create_button(
                        "Registrar",
                        self.handle_register,
                        icon=ft.Icons.PERSON_ADD,
                        expand=False,
                    ),
                ],
                spacing=15,
            ),
            bgcolor=COLORS["secondary"],
            padding=30,
            border_radius=12,
            width=None,
            expand=True,
        )

        card_wrapper = ft.Container(
            content=self._card_inner,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=10, right=10),
        )

        super().__init__(
            route="/register",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=30),

                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
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

                            card_wrapper,
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

        # configurar resize handler e ajustar largura inicial
        try:
            self._orig_on_resize = getattr(self.page, "on_resize", None)
            self.page.on_resize = lambda e: self._update_card_width()
        except Exception:
            pass

        self._update_card_width()
    
    def handle_register(self, e):
        email = self.email_field.value
        password = self.password_field.value
        password_confirm = self.password_confirm_field.value
        
        if not email or not password or not password_confirm:
            show_snack(self.page, create_alert("Preencha todos os campos", is_error=True))
            return
        
        if password != password_confirm:
            show_snack(self.page, create_alert("As senhas não coincidem", is_error=True))
            return
        
        if len(password) < 6:
            show_snack(self.page, create_alert("A senha deve ter pelo menos 6 caracteres", is_error=True))
            return
        
        # Registro via Supabase Auth (sempre como usuário normal)
        result = auth_manager.register(email, password, is_admin=False)
        
        if result:
            show_snack(self.page, create_alert("Registro realizado com sucesso! Faça login."))
            self.page.go("/login")
        else:
            show_snack(self.page, create_alert("Erro ao registrar. Tente outro email.", is_error=True))

    def _update_card_width(self):
        """Mesma lógica do login: ajusta largura conforme a janela."""
        try:
            w = None
            if hasattr(self.page, "window_width") and self.page.window_width:
                w = self.page.window_width
            elif hasattr(self.page, "width") and self.page.width:
                w = self.page.width
            if not w:
                w = 1000

            if w < 700:
                self._card_inner.width = None
                self._card_inner.expand = True
            else:
                target = 760
                max_allowed = max(400, int(w - 120))
                self._card_inner.width = min(target, max_allowed)
                self._card_inner.expand = False

            try:
                self.page.update()
            except Exception:
                pass
        except Exception:
            pass
