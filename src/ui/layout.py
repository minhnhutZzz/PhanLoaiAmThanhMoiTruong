"""
Main Application Layout
Manages sidebar navigation and content switching
"""
import flet as ft
from src.ui.dashboard import DashboardView
from src.ui.file_analysis import FileAnalysisView
from src.ui.live_monitor import LiveMonitorView
from src.ui.history import HistoryView
from src.ui.settings import SettingsView
from src.ai.model_handler import SoundClassifier
from src.utils.state import app_state
import psutil


class MainLayout:
    """Main application layout with sidebar and content area"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Initialize classifier
        self.classifier = SoundClassifier(model_path="models/best_convnext_tiny.pth", use_mock=False)
        app_state.set_model_loaded(not self.classifier.use_mock)
        
        # Current view
        self.current_view_index = 0
        
        # UI elements
        self.sidebar = None
        self.content_area = None
        self.status_bar = None
        
        # View instances
        self.file_analysis_view = FileAnalysisView(page, self.classifier)
        self.live_monitor_view = LiveMonitorView(page, self.classifier)
    
    def build(self):
        # Sidebar navigation
        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.UPLOAD_FILE_OUTLINED,
                    selected_icon=ft.Icons.UPLOAD_FILE,
                    label="File Analysis",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.MIC_OUTLINED,
                    selected_icon=ft.Icons.MIC,
                    label="Live Monitor",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.HISTORY_OUTLINED,
                    selected_icon=ft.Icons.HISTORY,
                    label="History",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=self.on_nav_change,
            bgcolor="#0F172A"
        )
        
        # Content area - start with dashboard
        self.content_area = ft.Container(
            content=DashboardView(self.page),
            expand=True,
            bgcolor="#0F172A"
        )
        
        # Status bar
        self.status_bar = self._create_status_bar()
        
        # Main layout
        return ft.Column([
            ft.Container(
                content=ft.Row([
                    self.sidebar,
                    ft.VerticalDivider(width=1, color="#334155"),
                    self.content_area,
                ], spacing=0, expand=True),
                expand=True
            ),
            self.status_bar,
        ], spacing=0, expand=True)
    
    def on_nav_change(self, e):
        """Handle navigation change"""
        self.current_view_index = e.control.selected_index
        
        # Switch content based on selection
        if self.current_view_index == 0:
            self.content_area.content = DashboardView(self.page)
        elif self.current_view_index == 1:
            self.content_area.content = self.file_analysis_view.build()
        elif self.current_view_index == 2:
            self.content_area.content = self.live_monitor_view.build()
        elif self.current_view_index == 3:
            self.content_area.content = HistoryView(self.page)
        elif self.current_view_index == 4:
            self.content_area.content = SettingsView(self.page)
        
        self.page.update()
    
    def _create_status_bar(self):
        """Create status bar at the bottom"""
        # Get system info
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Microphone status (placeholder)
        mic_status = "🎤 Ready"
        
        # Model version
        model_version = f"Model: {app_state.model_info['name']} {app_state.model_info['version']}"
        
        return ft.Container(
            content=ft.Row([
                ft.Text(mic_status, size=12, color="#10B981"),
                ft.VerticalDivider(width=1, color="#334155"),
                ft.Text(f"CPU: {cpu_percent:.1f}%", size=12, color="#00D9FF"),
                ft.VerticalDivider(width=1, color="#334155"),
                ft.Text(model_version, size=12, color="#8B5CF6"),
                ft.VerticalDivider(width=1, color="#334155"),
                ft.Text(
                    "Status: " + ("✅ Ready" if app_state.model_info['loaded'] else "⚠️ Mock Mode"),
                    size=12,
                    color="#10B981" if app_state.model_info['loaded'] else "#F59E0B"
                ),
            ], spacing=10),
            padding=10,
            bgcolor="#1E293B",
            border=ft.border.only(top=ft.BorderSide(1, "#334155"))
        )
