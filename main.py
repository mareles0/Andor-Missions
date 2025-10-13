
import flet as ft
from config import COLORS
from auth import session
from views.login_view import LoginView
from views.register_view import RegisterView
from views.user_view import UserView
from views.admin_view import AdminView


def main(page: ft.Page):
    
    
    
    page.title = "Andor Missions"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLORS["background"]
    page.padding = 0
    # Configurações de janela removidas para web app
    # A aplicação se adapta automaticamente ao tamanho da tela
    
    
    def on_login_success():
        
        if session.is_admin:
            page.go("/admin")
        else:
            page.go("/user")
    
    def on_logout():
        
        page.go("/login")
    
    
    def route_change(e):
        
        page.views.clear()
        
        
        if page.route == "/login" or page.route == "/":
            page.views.append(LoginView(page, on_login_success))
        
        elif page.route == "/register":
            page.views.append(RegisterView(page))
        
        
        elif page.route == "/user":
            if not session.is_authenticated():
                page.go("/login")
                return
            user_view = UserView(page, on_logout)
            page.views.append(user_view)
            
            user_view.load_missions()
        
        elif page.route == "/admin":
            if not session.is_authenticated():
                page.go("/login")
                return
            if not session.is_admin:
                page.go("/user")
                return
            admin_view = AdminView(page, on_logout)
            page.views.append(admin_view)
            
            admin_view.load_missions()
        
        page.update()
    
    def view_pop(e):
        
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    
    page.go("/login")


if __name__ == "__main__":
    # Para web app: usa view=ft.AppView.WEB_BROWSER e port=8550
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)

