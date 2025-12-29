"""
Model Download Dialog
UI for downloading model from Google Drive
"""
import flet as ft
import threading
from src.utils.model_downloader import download_convnext_model, get_model_info


class ModelDownloadDialog:
    """Dialog for downloading model"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = None
        self.progress_bar = None
        self.progress_text = None
        self.download_button = None
        self.cancel_button = None
        self.is_downloading = False
        
    def show(self, on_complete=None):
        """
        Show download dialog
        
        Args:
            on_complete: Callback function when download completes
        """
        self.on_complete = on_complete
        
        # Progress bar
        self.progress_bar = ft.ProgressBar(
            width=400,
            color="#00D9FF",
            value=0
        )
        
        # Progress text
        self.progress_text = ft.Text(
            "Sẵn sàng tải xuống...",
            size=14,
            color="#94A3B8"
        )
        
        # Download button
        self.download_button = ft.ElevatedButton(
            "📥 Tải Xuống Model",
            icon=ft.Icons.DOWNLOAD,
            on_click=self.start_download,
            style=ft.ButtonStyle(
                bgcolor="#10B981",
                color="white"
            )
        )
        
        # Cancel button
        self.cancel_button = ft.ElevatedButton(
            "Hủy",
            on_click=self.close_dialog,
            style=ft.ButtonStyle(
                bgcolor="#64748B",
                color="white"
            )
        )
        
        # Dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Model Chưa Được Tải Xuống"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Ứng dụng cần file model ConvNeXt-Tiny để hoạt động.",
                        size=14
                    ),
                    ft.Text(
                        "Kích thước: ~115 MB",
                        size=12,
                        color="#94A3B8",
                        italic=True
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Nguồn: Google Drive",
                        size=12,
                        color="#94A3B8"
                    ),
                    ft.Container(height=20),
                    self.progress_text,
                    self.progress_bar,
                ], spacing=5, tight=True),
                width=450,
                padding=10
            ),
            actions=[
                self.download_button,
                self.cancel_button,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def start_download(self, e):
        """Start downloading model"""
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_button.disabled = True
        self.cancel_button.disabled = True
        self.progress_text.value = "Đang tải xuống..."
        self.page.update()
        
        # Download in background thread
        def download():
            def update_progress(current, total):
                """Update progress bar"""
                progress = current / total
                mb_current = current / (1024 * 1024)
                mb_total = total / (1024 * 1024)
                
                self.progress_bar.value = progress
                self.progress_text.value = f"Đang tải: {mb_current:.1f} MB / {mb_total:.1f} MB ({progress*100:.0f}%)"
                self.page.update()
            
            # Download model
            success = download_convnext_model(
                model_dir="models",
                progress_callback=update_progress
            )
            
            # Update UI on completion
            if success:
                self.progress_bar.value = 1.0
                self.progress_text.value = "✅ Tải xuống hoàn tất!"
                self.progress_text.color = "#10B981"
                
                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ Model đã được tải xuống thành công!"),
                    bgcolor="#10B981"
                )
                self.page.snack_bar.open = True
                
                # Close dialog after delay
                import time
                time.sleep(1)
                self.close_dialog(None)
                
                # Call completion callback
                if self.on_complete:
                    self.on_complete(success=True)
            else:
                self.progress_bar.value = 0
                self.progress_text.value = "❌ Tải xuống thất bại!"
                self.progress_text.color = "#EF4444"
                self.download_button.disabled = False
                self.cancel_button.disabled = False
                
                # Show error message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❌ Lỗi tải xuống model. Vui lòng thử lại!"),
                    bgcolor="#EF4444"
                )
                self.page.snack_bar.open = True
            
            self.is_downloading = False
            self.page.update()
        
        # Start download thread
        threading.Thread(target=download, daemon=True).start()
    
    def close_dialog(self, e):
        """Close the dialog"""
        if self.is_downloading:
            return  # Don't close while downloading
        
        self.dialog.open = False
        self.page.update()
        
        # Call completion callback with cancel
        if self.on_complete:
            self.on_complete(success=False)
