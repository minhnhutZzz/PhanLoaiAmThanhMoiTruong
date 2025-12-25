"""
File Analysis View - Upload and analyze audio files
"""
import flet as ft
from pathlib import Path
import threading
from io import BytesIO
import base64

from src.ai.audio_processor import load_and_preprocess_audio, mel_spectrogram_to_image
from src.ai.model_handler import SoundClassifier
from src.utils.state import app_state


class FileAnalysisView:
    """File analysis view for uploading and analyzing audio files"""
    
    def __init__(self, page: ft.Page, classifier: SoundClassifier):
        self.page = page
        self.classifier = classifier
        
        # UI elements
        self.file_picker = None
        self.selected_file_text = None
        self.spectrogram_image = None
        self.result_container = None
        self.analyze_button = None
        self.progress_ring = None
        
        self.current_file_path = None
    
    def build(self):
        # File picker
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)
        
        # Selected file display
        self.selected_file_text = ft.Text(
            "No file selected",
            color="#94A3B8",
            size=14
        )
        
        # Upload button
        upload_button = ft.ElevatedButton(
            "📁 Select Audio File",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["wav", "mp3", "ogg", "flac"],
                dialog_title="Select Audio File"
            ),
            style=ft.ButtonStyle(
                bgcolor="#00D9FF",
                color="white"
            )
        )
        
        # Analyze button
        self.progress_ring = ft.ProgressRing(visible=False, color="#00D9FF")
        self.analyze_button = ft.ElevatedButton(
            "🔍 Analyze",
            icon=ft.Icons.ANALYTICS,
            disabled=True,
            on_click=self.analyze_file,
            style=ft.ButtonStyle(
                bgcolor="#10B981",
                color="white"
            )
        )
        
        # Spectrogram display
        self.spectrogram_image = ft.Image(
            visible=False,
            width=800,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Result container
        self.result_container = ft.Container(
            visible=False,
            padding=20,
            border=ft.border.all(2, "#00D9FF"),
            border_radius=10,
            bgcolor="#1E293B"
        )
        
        # Layout
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "📁 File Analysis",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#00D9FF"
                ),
                ft.Divider(color="#334155"),
                
                # Upload section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Upload Audio File", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([upload_button, self.selected_file_text], spacing=15),
                        ft.Row([self.analyze_button, self.progress_ring], spacing=10),
                    ], spacing=15),
                    padding=20,
                    border=ft.border.all(1, "#334155"),
                    border_radius=10,
                    bgcolor="#1E293B"
                ),
                
                ft.Container(height=20),
                
                # Spectrogram section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Mel-Spectrogram", size=18, weight=ft.FontWeight.BOLD),
                        self.spectrogram_image,
                    ], spacing=15),
                    padding=20,
                    border=ft.border.all(1, "#334155"),
                    border_radius=10,
                    bgcolor="#1E293B"
                ),
                
                ft.Container(height=20),
                
                # Results section
                self.result_container,
                
            ], scroll=ft.ScrollMode.AUTO, spacing=0),
            padding=20,
            expand=True
        )
    
    def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Handle file selection"""
        if e.files:
            file = e.files[0]
            self.current_file_path = file.path
            self.selected_file_text.value = f"Selected: {file.name}"
            self.analyze_button.disabled = False
            self.page.update()
    
    def analyze_file(self, e):
        """Analyze the selected audio file"""
        if not self.current_file_path:
            return
        
        # Show progress
        self.analyze_button.disabled = True
        self.progress_ring.visible = True
        self.page.update()
        
        # Run analysis in thread
        threading.Thread(target=self._run_analysis, daemon=True).start()
    
    def _run_analysis(self):
        """Run analysis in background thread"""
        try:            
            # Load and preprocess audio (EXACTLY like Kaggle)
            import torch
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            preprocessed, spec_for_display = load_and_preprocess_audio(
                self.current_file_path,
                device=device
            )
            
            if preprocessed is None:
                self._show_error("Failed to load audio file")
                return
            
            # Convert spectrogram to image for display
            spec_img = mel_spectrogram_to_image(spec_for_display)
            
            # Update spectrogram display
            self.spectrogram_image.src_base64 = self._image_to_base64(spec_img)
            self.spectrogram_image.visible = True
            
            # Run prediction
            result = self.classifier.predict(preprocessed)
            
            # Get top-5 predictions
            top_predictions = self.classifier.get_top_k_predictions(preprocessed, k=5)
            
            # Add to history
            app_state.add_to_history(
                result['label'],
                result['confidence'],
                source="file"
            )
            
            # Update UI with results
            self._display_results(result, top_predictions)
            
        except Exception as ex:
            self._show_error(f"Analysis error: {str(ex)}")
        
        finally:
            # Hide progress
            self.progress_ring.visible = False
            self.analyze_button.disabled = False
            self.page.update()
    
    def _display_results(self, main_result, top_predictions):
        """Display analysis results"""
        # Main prediction
        main_card = ft.Container(
            content=ft.Row([
                ft.Text(main_result['icon'], size=60),
                ft.Column([
                    ft.Text(
                        main_result['label'].replace('_', ' ').title(),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#00D9FF"
                    ),
                    ft.Text(
                        f"Confidence: {main_result['confidence']:.2f}%",
                        size=16,
                        color="#10B981"
                    ),
                ], spacing=5)
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            border=ft.border.all(2, "#00D9FF"),
            border_radius=10,
            bgcolor="#0F172A"
        )
        
        # Top-5 predictions
        top5_bars = []
        for pred in top_predictions:
            bar = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(pred['icon'], size=20),
                        ft.Text(
                            pred['label'].replace('_', ' ').title(),
                            size=14,
                            color="white"
                        ),
                        ft.Text(
                            f"{pred['confidence']:.1f}%",
                            size=14,
                            color="#94A3B8"
                        ),
                    ], spacing=10),
                    ft.ProgressBar(
                        value=pred['confidence'] / 100,
                        color="#00D9FF",
                        bgcolor="#334155"
                    )
                ], spacing=5),
                padding=10
            )
            top5_bars.append(bar)
        
        # Update result container
        self.result_container.content = ft.Column([
            ft.Text("Analysis Results", size=18, weight=ft.FontWeight.BOLD),
            main_card,
            ft.Container(height=10),
            ft.Text("Top 5 Predictions", size=16, weight=ft.FontWeight.BOLD),
            ft.Column(top5_bars, spacing=10)
        ], spacing=15)
        
        self.result_container.visible = True
        self.page.update()
    
    def _show_error(self, message: str):
        """Show error message"""
        self.result_container.content = ft.Text(
            f"❌ {message}",
            color="#EF4444",
            size=16
        )
        self.result_container.visible = True
        self.page.update()
    
    def _image_to_base64(self, img):
        """Convert PIL Image to base64 string"""
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
