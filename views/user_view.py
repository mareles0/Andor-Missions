import flet as ft

from ui_components import *
from supabase_client import db
from auth import session


class UserView(ft.View):
    
    
    def __init__(self, page: ft.Page, on_logout):
        self.page = page
        self.on_logout = on_logout
        self.missions = []
        
        
        self.search_field = ft.TextField(
            label="Pesquisar missões",
            prefix_icon=ft.Icons.SEARCH,
            border_color=COLORS["secondary"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text"],
            on_submit=self.handle_search,
        )
        
        
        self.missions_list = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        super().__init__(
            route="/user",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                create_title("MISSÕES"),
                                                ft.Text(
                                                    f"Agente: {session.get_user_email()}",
                                                    size=14,
                                                    color=COLORS["text"],
                                                    opacity=0.7,
                                                ),
                                            ],
                                            expand=True,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.LOGOUT,
                                            icon_color=COLORS["accent"],
                                            tooltip="Sair",
                                            on_click=lambda _: self.handle_logout(),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.only(bottom=10),
                            ),
                            
                            
                            ft.Row(
                                [
                                    self.search_field,
                                    ft.IconButton(
                                        icon=ft.Icons.REFRESH,
                                        icon_color=COLORS["text"],
                                        tooltip="Atualizar",
                                        on_click=lambda _: self.load_missions(),
                                    ),
                                ],
                                spacing=10,
                            ),
                            
                            ft.Divider(color=COLORS["secondary"]),
                            
                            
                            self.missions_list,
                        ],
                        spacing=10,
                        expand=True,
                    ),
                    padding=20,
                    expand=True,
                )
            ],
            bgcolor=COLORS["background"],
        )
    
    def load_missions(self):
        token = session.access_token
        self.missions = db.get_missions(token)
        self.render_missions()
    
    def handle_search(self, e):
        token = session.access_token
        search_term = self.search_field.value
        
        if search_term:
            self.missions = db.search_missions(search_term, token)
        else:
            self.missions = db.get_missions(token)
        
        self.render_missions()
    
    def render_missions(self):
        
        self.missions_list.controls.clear()
        
        if not self.missions:
            self.missions_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.SEARCH_OFF, size=64, color=COLORS["text"], opacity=0.3),
                            ft.Text(
                                "Nenhuma missão encontrada",
                                size=18,
                                color=COLORS["text"],
                                opacity=0.5,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
        else:
            for mission in self.missions:
                card = create_mission_card(
                    mission,
                    on_click=lambda e, m=mission: self.show_mission_detail(m),
                    show_full_info=False,
                )
                self.missions_list.controls.append(card)
        
        if self.page:
            self.page.update()
    
    def show_mission_detail(self, mission):
        
        danger_stars = "⚠️ " * mission.get("danger_level", 1)
        
        status_text = {
            "pending": "Pendente",
            "active": "Ativa",
            "completed": "Concluída",
            "failed": "Falhou",
        }
        
        detail_dialog = create_dialog(
            title=mission.get("name", "Missão"),
            content=ft.Column(
                [
                    ft.Text(f"📍 Localização: {mission.get('location', 'Desconhecido')}", size=14, color=COLORS["text"]),
                    ft.Text(f"📊 Status: {status_text.get(mission.get('status', 'pending'), 'Desconhecido')}", size=14, color=COLORS["text"]),
                    ft.Text(f"⚠️ Nível de perigo: {danger_stars} ({mission.get('danger_level', 1)}/5)", size=14, color=COLORS["warning"]),
                    ft.Divider(),
                    ft.Text("Descrição:", size=16, weight=ft.FontWeight.BOLD, color=COLORS["accent"]),
                    ft.Container(
                        content=ft.Text(
                            mission.get("description", "Sem descrição"), 
                            size=13, 
                            color=COLORS["text"],
                            selectable=True,
                        ),
                        padding=10,
                        bgcolor=COLORS["background"],
                        border_radius=8,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                height=500,
            ),
            actions=[
                ft.TextButton(
                    "Fechar",
                    on_click=lambda _: self.page.close(detail_dialog),
                ),
            ],
        )
        
        self.page.open(detail_dialog)
    
    def handle_logout(self):
        
        session.logout()
        self.on_logout()

