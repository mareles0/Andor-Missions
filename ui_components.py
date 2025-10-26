import flet as ft
from config import COLORS


def show_snack(page, snackbar):
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()


def create_title(text: str) -> ft.Text:
    
    return ft.Text(
        text,
        size=32,
        weight=ft.FontWeight.BOLD,
        color=COLORS["accent"],
        text_align=ft.TextAlign.CENTER,
    )


def create_subtitle(text: str) -> ft.Text:
    
    return ft.Text(
        text,
        size=20,
        weight=ft.FontWeight.W_500,
        color=COLORS["text"],
    )


def create_input(label: str, password: bool = False, multiline: bool = False) -> ft.TextField:
    
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,
        multiline=multiline,
        min_lines=3 if multiline else 1,
        max_lines=5 if multiline else 1,
        border_color=COLORS["secondary"],
        focused_border_color=COLORS["accent"],
        color=COLORS["text"],
        label_style=ft.TextStyle(color=COLORS["text"]),
    )


def create_button(text: str, on_click, icon: str = None, 
                 color: str = None, expand: bool = False) -> ft.ElevatedButton:
    
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        bgcolor=color or COLORS["accent"],
        color=COLORS["text"],
        expand=expand,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )


def create_card(content, on_click=None) -> ft.Container:
    
    return ft.Container(
        content=content,
        bgcolor=COLORS["secondary"],
        border_radius=12,
        padding=15,
        on_click=on_click,
        ink=True if on_click else False,
    )


def create_mission_card(mission: dict, on_click=None, show_full_info: bool = False) -> ft.Container:
    
    
    
    status_colors = {
        "pending": COLORS["warning"],
        "active": COLORS["accent"],
        "completed": COLORS["success"],
        "failed": "#f44336",
        "critical": "#000000",  # Preto para status crítico
    }
    
    status_text = {
        "pending": "Pendente",
        "active": "Ativa",
        "completed": "Concluída",
        "failed": "Falhou",
        "critical": "Crítica",
    }
    
    status = mission.get("status", "pending")
    
    # Cor do texto do status (branco para fundo escuro)
    status_text_color = "#FFFFFF" if status == "critical" else COLORS["background"]
    
    danger_stars = "⚠️ " * mission.get("danger_level", 1)
    
    content_items = [
        ft.Row([
            ft.Text(
                mission.get("name", "Sem nome"),
                size=18,
                weight=ft.FontWeight.BOLD,
                color=COLORS["text"],
                expand=True,
            ),
            ft.Container(
                content=ft.Text(
                    status_text.get(status, status),
                    size=12,
                    color=status_text_color,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=status_colors.get(status, COLORS["secondary"]),
                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                border_radius=8,
            ),
        ]),
        ft.Text(
            f"📍 {mission.get('location', 'Desconhecido')}",
            size=14,
            color=COLORS["text"],
            opacity=0.8,
        ),
    ]
    
    if show_full_info:
        content_items.extend([
            ft.Text(
                f"Nível de perigo: {danger_stars}",
                size=14,
                color=COLORS["warning"],
            ),
            ft.Text(
                mission.get("description", "Sem descrição"),
                size=13,
                color=COLORS["text"],
                opacity=0.9,
                selectable=True,
            ),
        ])
    
    return create_card(
        content=ft.Column(
            content_items,
            spacing=8,
        ),
        on_click=on_click,
    )


def create_alert(message: str, is_error: bool = False) -> ft.SnackBar:
    
    return ft.SnackBar(
        content=ft.Text(message, color=COLORS["text"]),
        bgcolor=COLORS["accent"] if is_error else COLORS["success"],
    )


def create_dialog(title: str, content, actions: list) -> ft.AlertDialog:
    
    return ft.AlertDialog(
        title=ft.Text(title, color=COLORS["text"]),
        content=content,
        actions=actions,
        bgcolor=COLORS["secondary"],
    )

