"""
S-Hear Intelligent Dashboard
Main entry point for the application
"""
import flet as ft
from src.ui.layout import MainLayout


def main(page: ft.Page):
    """Main application entry point"""
    
    # Page configuration
    page.title = "S-Hear Intelligent Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    
    # Custom theme colors
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#00D9FF",  # Electric Blue
            secondary="#8B5CF6",  # Purple
            background="#0F172A",  # Dark Slate
            surface="#1E293B",  # Slate Grey
            error="#EF4444",  # Red
            on_primary="#FFFFFF",
            on_secondary="#FFFFFF",
            on_background="#F1F5F9",
            on_surface="#F1F5F9",
        ),
        font_family="Segoe UI"
    )
    
    # Window settings
    page.window.width = 1400
    page.window.height = 900
    page.window.min_width = 1000
    page.window.min_height = 700
    
    # Create main layout
    main_layout = MainLayout(page)
    
    # Add to page
    page.add(main_layout.build())
    
    # Welcome message
    page.snack_bar = ft.SnackBar(
        content=ft.Text("🎧 Welcome to S-Hear Dashboard!"),
        bgcolor="#00D9FF"
    )
    page.snack_bar.open = True
    page.update()


if __name__ == "__main__":
    # Run the app
    ft.app(target=main)
