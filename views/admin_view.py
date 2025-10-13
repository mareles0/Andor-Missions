
import flet as ft

from ui_components import *
from supabase_client import db
from auth import session


class AdminView(ft.View):
    
    
    def __init__(self, page: ft.Page, on_logout):
        self.page = page
        self.on_logout = on_logout
        self.missions = []
        self.selected_mission = None
        
        
        self.search_field = ft.TextField(
            label="Pesquisar missões",
            prefix_icon=ft.icons.SEARCH,
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
            route="/admin",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        create_title("ADMIN"),
                                                        ft.Icon(
                                                            ft.icons.ADMIN_PANEL_SETTINGS,
                                                            color=COLORS["accent"],
                                                            size=32,
                                                        ),
                                                    ],
                                                    spacing=10,
                                                ),
                                                ft.Text(
                                                    f"Comandante: {session.get_user_email()}",
                                                    size=14,
                                                    color=COLORS["text"],
                                                    opacity=0.7,
                                                ),
                                            ],
                                            expand=True,
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.LOGOUT,
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
                                        icon=ft.icons.REFRESH,
                                        icon_color=COLORS["text"],
                                        tooltip="Atualizar",
                                        on_click=lambda _: self.load_missions(),
                                    ),
                                    create_button(
                                        "Nova Missão",
                                        self.show_create_dialog,
                                        icon=ft.icons.ADD,
                                        color=COLORS["success"],
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
                            ft.Icon(ft.icons.INBOX, size=64, color=COLORS["text"], opacity=0.3),
                            ft.Text(
                                "Nenhuma missão registrada",
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
                mission_card = self.create_admin_mission_card(mission)
                self.missions_list.controls.append(mission_card)
        
        if self.page:
            self.page.update()
    
    def create_admin_mission_card(self, mission):
        
        card_content = create_mission_card(mission, show_full_info=True)
        
        
        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color=COLORS["warning"],
                    tooltip="Editar",
                    on_click=lambda e, m=mission: self.show_edit_dialog(m),
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=COLORS["accent"],
                    tooltip="Excluir",
                    on_click=lambda e, m=mission: self.show_delete_confirm(m),
                ),
                ft.IconButton(
                    icon=ft.icons.INFO,
                    icon_color=COLORS["text"],
                    tooltip="Detalhes",
                    on_click=lambda e, m=mission: self.show_mission_detail(m),
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        )
        
        card_content.content.controls.append(ft.Divider(color=COLORS["background"]))
        card_content.content.controls.append(actions)
        
        return card_content
    
    def show_create_dialog(self, e):
        
        name_field = create_input("Nome da Missão")
        location_field = create_input("Localização")
        description_field = create_input("Descrição", multiline=True)
        
        status_dropdown = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("pending", "Pendente"),
                ft.dropdown.Option("active", "Ativa"),
                ft.dropdown.Option("completed", "Concluída"),
                ft.dropdown.Option("failed", "Falhou"),
            ],
            value="pending",
            border_color=COLORS["secondary"],
            color=COLORS["text"],
        )
        
        danger_slider = ft.Slider(
            min=1,
            max=5,
            divisions=4,
            value=1,
            label="Nível {value}",
            active_color=COLORS["accent"],
        )
        
        def create_mission(e):
            if not name_field.value or not location_field.value:
                show_snack(self.page, create_alert("Preencha os campos obrigatórios", is_error=True))
                return
            
            result = db.create_mission(
                name=name_field.value,
                location=location_field.value,
                description=description_field.value or "",
                status=status_dropdown.value,
                danger_level=int(danger_slider.value),
                access_token=session.access_token
            )
            
            if result:
                show_snack(self.page, create_alert("Missão criada com sucesso!"))
                self.page.close(dialog)
                self.load_missions()
            else:
                show_snack(self.page, create_alert("Erro ao criar missão", is_error=True))
        
        dialog = create_dialog(
            title="Nova Missão",
            content=ft.Column(
                [
                    name_field,
                    location_field,
                    description_field,
                    status_dropdown,
                    ft.Text("Nível de Perigo:", size=14, color=COLORS["text"]),
                    danger_slider,
                ],
                spacing=15,
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.page.close(dialog)),
                create_button("Criar", create_mission, icon=ft.icons.ADD),
            ],
        )
        
        self.page.open(dialog)
    
    def show_edit_dialog(self, mission):
        
        name_field = create_input("Nome da Missão")
        name_field.value = mission.get("name", "")
        
        location_field = create_input("Localização")
        location_field.value = mission.get("location", "")
        
        description_field = create_input("Descrição", multiline=True)
        description_field.value = mission.get("description", "")
        
        status_dropdown = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("pending", "Pendente"),
                ft.dropdown.Option("active", "Ativa"),
                ft.dropdown.Option("completed", "Concluída"),
                ft.dropdown.Option("failed", "Falhou"),
            ],
            value=mission.get("status", "pending"),
            border_color=COLORS["secondary"],
            color=COLORS["text"],
        )
        
        danger_slider = ft.Slider(
            min=1,
            max=5,
            divisions=4,
            value=mission.get("danger_level", 1),
            label="Nível {value}",
            active_color=COLORS["accent"],
        )
        
        def update_mission(e):
            if not name_field.value or not location_field.value:
                show_snack(self.page, create_alert("Preencha os campos obrigatórios", is_error=True))
                return
            
            result = db.update_mission(
                mission_id=mission["id"],
                name=name_field.value,
                location=location_field.value,
                description=description_field.value,
                status=status_dropdown.value,
                danger_level=int(danger_slider.value),
                access_token=session.access_token
            )
            
            if result:
                show_snack(self.page, create_alert("Missão atualizada!"))
                self.page.close(dialog)
                self.load_missions()
            else:
                show_snack(self.page, create_alert("Erro ao atualizar missão", is_error=True))
        
        dialog = create_dialog(
            title="Editar Missão",
            content=ft.Column(
                [
                    name_field,
                    location_field,
                    description_field,
                    status_dropdown,
                    ft.Text("Nível de Perigo:", size=14, color=COLORS["text"]),
                    danger_slider,
                ],
                spacing=15,
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.page.close(dialog)),
                create_button("Salvar", update_mission, icon=ft.icons.SAVE),
            ],
        )
        
        self.page.open(dialog)
    
    def show_delete_confirm(self, mission):
        
        def delete_mission(e):
            if db.delete_mission(mission["id"], session.access_token):
                show_snack(self.page, create_alert("Missão excluída!"))
                self.page.close(dialog)
                self.load_missions()
            else:
                show_snack(self.page, create_alert("Erro ao excluir missão", is_error=True))
        
        dialog = create_dialog(
            title="Confirmar Exclusão",
            content=ft.Text(
                f"Deseja realmente excluir a missão '{mission.get('name', 'Sem nome')}'?",
                color=COLORS["text"],
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.page.close(dialog)),
                create_button("Excluir", delete_mission, icon=ft.icons.DELETE, color=COLORS["accent"]),
            ],
        )
        
        self.page.open(dialog)
    
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
                    ft.Text(f"🆔 ID: {mission.get('id', 'N/A')}", size=14, color=COLORS["text"]),
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
                    ft.Divider(),
                    ft.Text(f"📅 Criado em: {mission.get('created_at', 'N/A')}", size=12, opacity=0.7, color=COLORS["text"]),
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

