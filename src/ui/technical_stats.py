"""
Technical Stats Dashboard
Displays real-time performance metrics and model metadata
"""
import flet as ft
from src.utils.performance_metrics import performance_metrics


class TechnicalStatsView:
    """Technical specifications dashboard"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        # UI Components
        self.preprocessing_text = ft.Text("0.00 ms", size=18, weight=ft.FontWeight.BOLD, color="#00D9FF")
        self.inference_text = ft.Text("0.00 ms", size=18, weight=ft.FontWeight.BOLD, color="#10B981")
        self.postprocessing_text = ft.Text("0.00 ms", size=18, weight=ft.FontWeight.BOLD, color="#F59E0B")
        self.total_latency_text = ft.Text("0.00 ms", size=18, weight=ft.FontWeight.BOLD, color="#8B5CF6")
        self.fps_text = ft.Text("0.00 FPS", size=18, weight=ft.FontWeight.BOLD, color="#EC4899")
    
    def build(self):
        """Build the technical stats view"""
        
        # Get model metadata
        metadata = performance_metrics.get_model_metadata()
        
        # Title
        title = ft.Container(
            content=ft.Column([
                ft.Text(
                    "⚡ Technical Specifications Dashboard",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#00D9FF"
                ),
                ft.Text(
                    "Real-time Performance Metrics & Model Information",
                    size=14,
                    color="#94A3B8",
                    italic=True
                ),
            ], spacing=8),
            padding=20
        )
        
        # == SECTION 1: Timing Metrics ==
        timing_metrics_section = self._create_timing_metrics_section()
        
        # == SECTION 2: Model Metadata ==
        model_metadata_section = self._create_model_metadata_section(metadata)
        
        # Refresh button
        refresh_button = ft.Container(
            content=ft.ElevatedButton(
                "🔄 Refresh Metrics",
                icon=ft.Icons.REFRESH,
                on_click=self.refresh_metrics,
                style=ft.ButtonStyle(
                    bgcolor="#00D9FF",
                    color="white"
                )
            ),
            padding=20
        )
        
        # Main layout
        return ft.Container(
            content=ft.Column([
                title,
                ft.Divider(color="#334155"),
                timing_metrics_section,
                ft.Container(height=20),
                model_metadata_section,
                ft.Container(height=20),
                refresh_button,
            ], scroll=ft.ScrollMode.AUTO, spacing=0),
            padding=20,
            expand=True
        )
    
    def _create_timing_metrics_section(self):
        """Create timing metrics display section"""
        
        # Get current metrics
        metrics = performance_metrics.get_current_metrics()
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "⏱️ Timing Metrics",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#F1F5F9"
                ),
                ft.Container(height=10),
                
                # Metrics cards in grid
                ft.Row([
                    self._create_metric_card(
                        "Pre-processing Time",
                        self.preprocessing_text,
                        "🔄",
                        "#00D9FF",
                        "Time to convert audio to Mel-Spectrogram (128x431)"
                    ),
                    self._create_metric_card(
                        "Inference Latency",
                        self.inference_text,
                        "🚀",
                        "#10B981",
                        "Model computation time (forward pass)"
                    ),
                    self._create_metric_card(
                        "Post-processing Time",
                        self.postprocessing_text,
                        "⚙️",
                        "#F59E0B",
                        "Label processing and UI update time"
                    ),
                ], spacing=15, wrap=True),
                
                ft.Container(height=15),
                
                ft.Row([
                    self._create_metric_card(
                        "Total End-to-End Latency",
                        self.total_latency_text,
                        "⚡",
                        "#8B5CF6",
                        "Total time from audio input to result display"
                    ),
                    self._create_metric_card(
                        "Real-time FPS",
                        self.fps_text,
                        "📊",
                        "#EC4899",
                        "Inference throughput (frames per second)"
                    ),
                ], spacing=15, wrap=True),
            ], spacing=5),
            padding=20,
            border=ft.border.all(1, "#334155"),
            border_radius=10,
            bgcolor="#1E293B"
        )
    
    def _create_metric_card(self, title: str, value_text: ft.Text, icon: str, 
                           color: str, description: str):
        """Create a single metric card"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(icon, size=24),
                    ft.Container(width=10),
                    ft.Column([
                        ft.Text(title, size=12, color="#94A3B8", weight=ft.FontWeight.W_500),
                        value_text,
                    ], spacing=2),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=5),
                ft.Text(description, size=10, color="#64748B", italic=True),
            ], spacing=5),
            padding=15,
            border=ft.border.all(2, color),
            border_radius=8,
            bgcolor="#0F172A",
            width=280,
        )
    
    def _create_model_metadata_section(self, metadata: dict):
        """Create model metadata display section"""
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "🤖 Model Metadata",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#F1F5F9"
                ),
                ft.Container(height=15),
                
                # Metadata rows
                ft.Row([
                    self._create_info_row("Backbone", metadata['backbone'], "🧠"),
                    self._create_info_row("Parameters Count", metadata['parameters'], "📊"),
                ], spacing=20, wrap=True),
                
                ft.Container(height=10),
                
                ft.Row([
                    self._create_info_row("Input Resolution", metadata['input_resolution'], "📐"),
                    self._create_info_row("Model Format", metadata['model_format'], "💾"),
                ], spacing=20, wrap=True),
                
                ft.Container(height=10),
                
                ft.Row([
                    self._create_info_row("Optimizer", metadata['optimizer'], "⚙️"),
                    self._create_info_row("Dataset", metadata['dataset'], "📚"),
                ], spacing=20, wrap=True),
                
                ft.Container(height=10),
                
                self._create_info_row("Number of Classes", str(metadata['num_classes']), "🏷️"),
            ], spacing=5),
            padding=20,
            border=ft.border.all(1, "#334155"),
            border_radius=10,
            bgcolor="#1E293B"
        )
    
    def _create_info_row(self, label: str, value: str, icon: str):
        """Create an information row"""
        return ft.Container(
            content=ft.Row([
                ft.Text(icon, size=20),
                ft.Container(width=10),
                ft.Column([
                    ft.Text(label, size=12, color="#94A3B8"),
                    ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color="#F1F5F9"),
                ], spacing=2),
            ], alignment=ft.MainAxisAlignment.START),
            padding=12,
            border_radius=8,
            bgcolor="#0F172A",
            border=ft.border.all(1, "#334155"),
            width=300,
        )
    
    def refresh_metrics(self, e):
        """Refresh and update all metrics"""
        metrics = performance_metrics.get_current_metrics()
        
        # Update timing metrics
        self.preprocessing_text.value = f"{metrics['preprocessing_time']:.2f} ms"
        self.inference_text.value = f"{metrics['inference_latency']:.2f} ms"
        self.postprocessing_text.value = f"{metrics['postprocessing_time']:.2f} ms"
        self.total_latency_text.value = f"{metrics['total_latency']:.2f} ms"
        self.fps_text.value = f"{metrics['real_time_fps']:.2f} FPS"
        
        self.page.update()
        
        # Show confirmation snackbar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("✅ Metrics refreshed!"),
            bgcolor="#10B981"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def auto_update_metrics(self):
        """Automatically update metrics (call this after inference)"""
        metrics = performance_metrics.get_current_metrics()
        
        self.preprocessing_text.value = f"{metrics['preprocessing_time']:.2f} ms"
        self.inference_text.value = f"{metrics['inference_latency']:.2f} ms"
        self.postprocessing_text.value = f"{metrics['postprocessing_time']:.2f} ms"
        self.total_latency_text.value = f"{metrics['total_latency']:.2f} ms"
        self.fps_text.value = f"{metrics['real_time_fps']:.2f} FPS"
