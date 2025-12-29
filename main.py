"""
Phân Loại Âm Thanh Môi Trường
Main entry point for the application
"""
import flet as ft
import os
from src.ui.layout import MainLayout
from src.ui.model_download_dialog import ModelDownloadDialog
from src.utils.model_downloader import check_model_exists


def main(page: ft.Page):
    """Main application entry point"""
    
    # Page configuration
    page.title = "Phân Loại Âm Thanh Môi Trường"
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
    
    # Check if model exists
    model_path = "models/best_convnext_tiny.pth"
    
    def init_app(success=True):
        """Initialize app after model check"""
        if not success:
            # User cancelled download
            page.window.close()
            return
            
        # Clear page
        page.clean()
        
        # Create main layout
        main_layout = MainLayout(page)
        
        # Add to page
        page.add(main_layout.build())
        page.update()
    
    # Check model and show download dialog if needed
    if not check_model_exists(model_path):
        print("[WARNING] Model not found!")
        print(f"[INFO] Expected path: {os.path.abspath(model_path)}")
        
        # Create download page instead of dialog
        from src.ui.model_download_page import ModelDownloadPage
        
        download_page = ModelDownloadPage(page)
        page.add(download_page.build(on_complete=lambda success: init_app(success)))
        page.update()
    else:
        print(f"[INFO] Model found: {model_path}")
        # Model exists, initialize app directly
        init_app()


if __name__ == "__main__":
    # Run the app
    ft.app(target=main)
