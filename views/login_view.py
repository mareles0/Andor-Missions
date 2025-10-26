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
        # criar o card (container interno) e manter referência para ajustes responsivos
        self._card_inner = ft.Container(
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
                                                icon=ft.Icons.LOGIN,
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
            # largura inicial; será ajustada no _update_card_width
            width=None,
            expand=True,
        )

        # container externo que centraliza o card
        card_wrapper = ft.Container(
            content=self._card_inner,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=10, right=10),
        )

        # montar a view
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
                            card_wrapper,
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

        # configurar resize handler para ajustar largura do card dinamicamente
        try:
            # armazena referência para restaurar caso necessário
            self._orig_on_resize = getattr(self.page, "on_resize", None)
            self.page.on_resize = lambda e: self._update_card_width()
        except Exception:
            pass

        # aplicar largura inicial correta
        self._update_card_width()
    
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

    def _update_card_width(self):
        """Ajusta a largura do card conforme a largura da janela.

        - Em telas pequenas (< 700) o card expande (mobile).
        - Em telas grandes, aplica largura fixa (desktop) para ficar centralizado.
        """
        try:
            # pegar largura atual da janela (várias versões do Flet expõem atributos diferentes)
            w = None
            if hasattr(self.page, "window_width") and self.page.window_width:
                w = self.page.window_width
            elif hasattr(self.page, "width") and self.page.width:
                w = self.page.width
            # fallback
            if not w:
                w = 1000

            # breakpoint responsivo
            if w < 700:
                # mobile: expandir para a largura disponível
                self._card_inner.width = None
                self._card_inner.expand = True
            else:
                # desktop: largura fixa e centralizada
                target = 760
                # garantir que não exceda a janela com alguma margem
                max_allowed = max(400, int(w - 120))
                self._card_inner.width = min(target, max_allowed)
                self._card_inner.expand = False

            # solicitar atualização visual
            try:
                self.page.update()
            except Exception:
                pass
        except Exception:
            # se algo falhar, não quebrar a view
            pass

