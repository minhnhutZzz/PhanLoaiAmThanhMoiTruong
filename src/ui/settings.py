"""
Settings View - Application settings and preferences
"""
import flet as ft
from src.utils.state import app_state


def SettingsView(page: ft.Page):
    """Settings view for app configuration"""
    
    # Threshold slider
    current_threshold = app_state.get_setting('confidence_threshold')
    
    threshold_text = ft.Text(
        f"{current_threshold:.0f}%",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#00D9FF"
    )
    
    def on_threshold_change(e):
        """Handle threshold slider change"""
        value = e.control.value
        app_state.update_setting('confidence_threshold', value)
        threshold_text.value = f"{value:.0f}%"
        page.update()
    
    threshold_slider = ft.Slider(
        min=0,
        max=100,
        value=current_threshold,
        divisions=20,
        label="{value}%",
        on_change=on_threshold_change,
        active_color="#00D9FF"
    )
    
    def on_visual_alerts_change(e):
        """Handle visual alerts switch change"""
        value = e.control.value
        app_state.update_setting('enable_visual_alerts', value)
        
        # Show confirmation
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"Emergency alerts {'enabled' if value else 'disabled'}"
            ),
            bgcolor="#10B981" if value else "#94A3B8"
        )
        page.snack_bar.open = True
        page.update()
    
    # Visual alerts switch
    visual_alerts_switch = ft.Switch(
        value=app_state.get_setting('enable_visual_alerts'),
        on_change=on_visual_alerts_change,
        active_color="#10B981"
    )
    
    # Layout
    return ft.Container(
        content=ft.Column([
            ft.Text(
                "⚙️ Settings",
                size=28,
                weight=ft.FontWeight.BOLD,
                color="#00D9FF"
            ),
            ft.Divider(color="#334155"),
            
            # Detection Settings
            ft.Container(
                content=ft.Column([
                    ft.Text("Detection Settings", size=20, weight=ft.FontWeight.BOLD),
                    
                    ft.Container(height=10),
                    
                    # Threshold
                    ft.Row([
                        ft.Icon(ft.Icons.TUNE, color="#00D9FF"),
                        ft.Text("Confidence Threshold", size=16),
                        threshold_text,
                    ], spacing=10),
                    ft.Text(
                        "Ngưỡng kích hoạt cảnh báo khẩn cấp (>= ngưỡng này sẽ có emergency alert)",
                        size=12,
                        color="#94A3B8",
                        italic=True
                    ),
                    threshold_slider,
                    
                ], spacing=10),
                padding=20,
                border=ft.border.all(1, "#334155"),
                border_radius=10,
                bgcolor="#1E293B"
            ),
            
            ft.Container(height=20),
            
            # Alert Settings
            ft.Container(
                content=ft.Column([
                    ft.Text("Alert Settings", size=20, weight=ft.FontWeight.BOLD),
                    
                    ft.Container(height=10),
                    
                    # Visual alerts (Emergency Alert)
                    ft.Row([
                        ft.Icon(ft.Icons.WARNING, color="#EF4444"),
                        ft.Column([
                            ft.Text("Emergency Alert", size=16),
                            ft.Text(
                                "Hiệu ứng nháy đỏ toàn màn hình cho âm thanh nguy hiểm (siren, fire...)",
                                size=12,
                                color="#94A3B8",
                                italic=True
                            ),
                        ], spacing=2, expand=True),
                        visual_alerts_switch,
                    ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                ], spacing=15),
                padding=20,
                border=ft.border.all(1, "#334155"),
                border_radius=10,
                bgcolor="#1E293B"
            ),
            
            ft.Container(height=20),
            
            # Model Info
            ft.Container(
                content=ft.Column([
                    ft.Text("Model Information", size=20, weight=ft.FontWeight.BOLD),
                    
                    ft.Container(height=10),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.PSYCHOLOGY, color="#8B5CF6"),
                        ft.Text("Model:", size=14, color="#94A3B8"),
                        ft.Text(app_state.model_info['name'], size=14, weight=ft.FontWeight.BOLD),
                    ], spacing=10),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.DATASET, color="#8B5CF6"),
                        ft.Text("Dataset:", size=14, color="#94A3B8"),
                        ft.Text(app_state.model_info['dataset'], size=14, weight=ft.FontWeight.BOLD),
                    ], spacing=10),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.INFO, color="#8B5CF6"),
                        ft.Text("Version:", size=14, color="#94A3B8"),
                        ft.Text(app_state.model_info['version'], size=14, weight=ft.FontWeight.BOLD),
                    ], spacing=10),
                    
                    ft.Row([
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE if app_state.model_info['loaded'] else ft.Icons.WARNING,
                            color="#10B981" if app_state.model_info['loaded'] else "#F59E0B"
                        ),
                        ft.Text("Status:", size=14, color="#94A3B8"),
                        ft.Text(
                            "Loaded" if app_state.model_info['loaded'] else "Mock Mode",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#10B981" if app_state.model_info['loaded'] else "#F59E0B"
                        ),
                    ], spacing=10),
                    
                ], spacing=12),
                padding=20,
                border=ft.border.all(1, "#334155"),
                border_radius=10,
                bgcolor="#1E293B"
            ),
            
            ft.Container(height=20),
            
            # About
            ft.Container(
                content=ft.Column([
                    ft.Text("About", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Phân Loại Âm Thanh Môi Trường v1.0",
                        size=14,
                        color="#94A3B8"
                    ),
                    ft.Text(
                        "Hệ thống nhận diện âm thanh môi trường sử dụng Deep Learning",
                        size=12,
                        color="#94A3B8",
                        italic=True
                    ),
                    ft.Text(
                        "Built with Flet, PyTorch, and ConvNeXt-Tiny",
                        size=12,
                        color="#94A3B8"
                    ),
                    ft.Text(
                        "Dataset: ESC-50 (50 environmental sounds)",
                        size=12,
                        color="#94A3B8"
                    ),
                ], spacing=8),
                padding=20,
                border=ft.border.all(1, "#334155"),
                border_radius=10,
                bgcolor="#1E293B"
            ),
            
        ], scroll=ft.ScrollMode.AUTO, spacing=0),
        padding=20,
        expand=True
    )
