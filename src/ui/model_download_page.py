"""
Model Download Page
Full-page UI for downloading model from Google Drive
"""
import flet as ft
import threading
from src.utils.model_downloader import download_convnext_model


class ModelDownloadPage:
    """Full-page download interface"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.progress_ring = None
        self.progress_text = None
        self.download_button = None
        self.status_text = None
        self.is_downloading = False
        self.on_complete = None
        
    def build(self, on_complete=None):
        """Build the download page"""
        self.on_complete = on_complete
        
        # Progress bar (indeterminate mode while downloading)
        self.progress_ring = ft.ProgressRing(
            width=50,
            height=50,
            stroke_width=4,
            color="#00D9FF",
            visible=False
        )
        
        # Progress text
        self.progress_text = ft.Text(
            "Nhấn nút bên dưới để bắt đầu tải xuống",
            size=16,
            color="#94A3B8",
            text_align=ft.TextAlign.CENTER
        )
        
        # Terminal info
        terminal_info = ft.Text(
            "💡 Tiến độ tải xuống sẽ hiển thị trong terminal/console",
            size=12,
            color="#64748B",
            text_align=ft.TextAlign.CENTER,
            italic=True
        )
        
        # Status text
        self.status_text = ft.Text(
            "Model ConvNeXt-Tiny chưa được tải xuống",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#F1F5F9",
            text_align=ft.TextAlign.CENTER
        )
        
        # Download button
        self.download_button = ft.ElevatedButton(
            "📥 Tải Xuống Model (115 MB)",
            icon=ft.Icons.DOWNLOAD,
            on_click=self.start_download,
            style=ft.ButtonStyle(
                bgcolor="#10B981",
                color="white",
                padding=20
            ),
            height=60,
            width=300
        )
        
        # Main content
        content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CLOUD_DOWNLOAD, size=80, color="#00D9FF"),
                ft.Container(height=20),
                self.status_text,
                ft.Container(height=10),
                ft.Text(
                    "Ứng dụng cần file model để nhận diện âm thanh",
                    size=14,
                    color="#94A3B8",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Nguồn: Google Drive | Kích thước: ~115 MB",
                    size=12,
                    color="#64748B",
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=40),
                self.download_button,
                ft.Container(height=30),
                self.progress_ring,
                self.progress_text,
                ft.Container(height=10),
                terminal_info,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor="#0F172A"
        )
        
        return content
    
    def start_download(self, e):
        """Start downloading model"""
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_button.disabled = True
        self.download_button.text = "Đang tải xuống..."
        self.progress_ring.visible = True
        self.progress_text.value = "Đang tải xuống... Xem terminal để theo dõi tiến độ"
        self.progress_text.color = "#00D9FF"
        self.page.update()
        
        print("[INFO] Starting download...")
        print("[INFO] Progress will be shown in terminal...")
        
        # Download in background thread
        def download():
            # Download model (gdown will show progress in terminal)
            success = download_convnext_model(model_dir="models")
            
            # Update UI on completion
            if success:
                self.progress_ring.visible = False
                self.progress_text.value = "✅ Tải xuống hoàn tất!"
                self.progress_text.color = "#10B981"
                self.status_text.value = "Model đã sẵn sàng!"
                self.status_text.color = "#10B981"
                
                print("[SUCCESS] Download completed!")
                
                # Wait a bit then initialize app
                import time
                time.sleep(1)
                
                # Call completion callback
                if self.on_complete:
                    self.on_complete(success=True)
            else:
                self.progress_ring.visible = False
                self.progress_text.value = "❌ Tải xuống thất bại! Vui lòng thử lại."
                self.progress_text.color = "#EF4444"
                self.download_button.disabled = False
                self.download_button.text = "📥 Thử Lại"
                
                print("[ERROR] Download failed!")
            
            self.is_downloading = False
            self.page.update()
        
        # Start download thread
        threading.Thread(target=download, daemon=True).start()
