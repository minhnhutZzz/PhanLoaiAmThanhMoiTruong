"""
Dashboard View - Welcome screen with statistics
"""
import flet as ft
from src.utils.state import app_state


def create_stat_card(title: str, value: str, icon: str, color: str):
    """Create a statistics card"""
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(icon, size=30),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=color, 
                       text_align=ft.TextAlign.CENTER, overflow=ft.TextOverflow.VISIBLE)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text(title, size=14, color="#94A3B8", text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        padding=20,
        border=ft.border.all(2, color),
        border_radius=10,
        bgcolor="#1E293B",
        width=240,
        height=120
    )


def DashboardView(page: ft.Page):
    """Main dashboard view"""
    stats = app_state.get_stats()
    
    # Welcome section
    welcome_text = ft.Container(
        content=ft.Column([
            ft.Text(
                "🎵 Phân Loại Âm Thanh Môi Trường",
                size=36,
                weight=ft.FontWeight.BOLD,
                color="#00D9FF"
            ),
            ft.Text(
                "Hệ thống nhận diện âm thanh sử dụng Deep Learning",
                size=16,
                color="#94A3B8",
                italic=True
            ),
        ], spacing=10),
        padding=20
    )
    
    # Stats cards
    stats_row = ft.Row([
        create_stat_card(
            "Total Detections",
            str(stats['total_detections']),
            "📊",
            "#00D9FF"
        ),
        create_stat_card(
            "Most Common",
            (stats['most_common'].replace('_', ' ').title() if stats['most_common'] else "N/A"),
            "🔊",
            "#10B981"
        ),
        create_stat_card(
            "Avg Confidence",
            f"{stats['avg_confidence']:.1f}%",
            "🎯",
            "#F59E0B"
        ),
    ], spacing=20, wrap=True)
    
    # Quick actions
    actions = ft.Container(
        content=ft.Column([
            ft.Text("Quick Actions", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(
                    "📁 Analyze File",
                    icon=ft.Icons.UPLOAD_FILE,
                    style=ft.ButtonStyle(
                        bgcolor="#00D9FF",
                        color="white"
                    )
                ),
                ft.ElevatedButton(
                    "🎙️ Live Monitor",
                    icon=ft.Icons.MIC,
                    style=ft.ButtonStyle(
                        bgcolor="#10B981",
                        color="white"
                    )
                ),
            ], spacing=10)
        ], spacing=15),
        padding=20,
        border=ft.border.all(1, "#334155"),
        border_radius=10,
        bgcolor="#1E293B"
    )
    
    # Model info
    model_status = "✅ Loaded" if app_state.model_info['loaded'] else "⚠️ Mock Mode"
    model_info = ft.Container(
        content=ft.Column([
            ft.Text("Model Information", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Model: {app_state.model_info['name']}", color="#94A3B8"),
            ft.Text(f"Dataset: {app_state.model_info['dataset']}", color="#94A3B8"),
            ft.Text(f"Status: {model_status}", color="#94A3B8"),
        ], spacing=8),
        padding=20,
        border=ft.border.all(1, "#334155"),
        border_radius=10,
        bgcolor="#1E293B"
    )
    
    # Main layout
    return ft.Container(
        content=ft.Column([
            welcome_text,
            ft.Divider(color="#334155"),
            stats_row,
            ft.Container(height=20),
            actions,
            ft.Container(height=20),
            model_info,
        ], scroll=ft.ScrollMode.AUTO, spacing=0),
        padding=20,
        expand=True
    )
