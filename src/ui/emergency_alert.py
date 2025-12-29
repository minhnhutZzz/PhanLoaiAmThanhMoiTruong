"""
Emergency Alert Overlay
Visual emergency effects for critical sound detection
"""
import flet as ft
import threading
import time


class EmergencyAlertOverlay:
    """Emergency alert with strobe flash and shake effects"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_active = False
        self.flash_thread = None
        self.overlay_container = None
        
        # Alert configuration
        self.flash_interval = 0.3  # seconds
        self.shake_offset = 0.02
        
    def show_alert(self, sound_label: str, confidence: float, icon: str):
        """
        Show emergency alert overlay
        
        Args:
            sound_label: Name of detected sound
            confidence: Confidence percentage
            icon: Emoji icon for the sound
        """
        if self.is_active:
            return  # Already showing alert
        
        self.is_active = True
        
        # Create overlay
        self._create_overlay(sound_label, confidence, icon)
        
        # Start strobe flash effect
        self._start_strobe_flash()
        
        # Add overlay to page
        self.page.overlay.append(self.overlay_container)
        self.page.update()
    
    def _create_overlay(self, sound_label: str, confidence: float, icon: str):
        """Create emergency overlay UI"""
        
        # Main warning icon with scale animation
        warning_icon = ft.Container(
            content=ft.Icon(
                ft.Icons.WARNING_AMBER_ROUNDED,
                size=120,
                color=ft.Colors.YELLOW_400
            ),
            animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Pulsing effect for icon
        def pulse_icon():
            while self.is_active:
                warning_icon.scale = 1.2
                self.page.update()
                time.sleep(0.5)
                if not self.is_active:
                    break
                warning_icon.scale = 1.0
                self.page.update()
                time.sleep(0.5)
        
        threading.Thread(target=pulse_icon, daemon=True).start()
        
        # Alert message
        alert_title = ft.Text(
            f"⚠️ CẢNH BÁO KHẨN CẤP ⚠️",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER
        )
        
        sound_name = ft.Text(
            f"{icon} {sound_label.upper().replace('_', ' ')}",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.YELLOW_400,
            text_align=ft.TextAlign.CENTER
        )
        
        confidence_text = ft.Text(
            f"Độ tin cậy: {confidence:.1f}%",
            size=20,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER
        )
        
        # Dismiss button
        dismiss_button = ft.ElevatedButton(
            "✓ TÔI ĐÃ HIỂU",
            icon=ft.Icons.CHECK_CIRCLE,
            on_click=self.dismiss_alert,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.WHITE,
                color=ft.Colors.RED_700,
                padding=20,
            ),
            height=60,
            width=250
        )
        
        # Content container with shake animation
        content_container = ft.Container(
            content=ft.Column([
                warning_icon,
                ft.Container(height=20),
                alert_title,
                ft.Container(height=15),
                sound_name,
                ft.Container(height=10),
                confidence_text,
                ft.Container(height=30),
                dismiss_button,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            border_radius=15,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.RED_900),
            border=ft.border.all(5, ft.Colors.YELLOW_400),
            animate_offset=ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Start shake animation
        def shake_animation():
            shake_positions = [
                (-self.shake_offset, 0),
                (self.shake_offset, 0),
                (-self.shake_offset, 0),
                (self.shake_offset, 0),
                (0, 0)
            ]
            
            while self.is_active:
                for offset in shake_positions:
                    if not self.is_active:
                        break
                    content_container.offset = offset
                    self.page.update()
                    time.sleep(0.05)
                time.sleep(0.5)  # Pause between shake cycles
        
        threading.Thread(target=shake_animation, daemon=True).start()
        
        # Full screen overlay
        self.overlay_container = ft.Container(
            content=ft.Stack([
                # Semi-transparent background
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
                ),
                # Centered alert
                ft.Container(
                    content=content_container,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]),
            width=self.page.window.width if self.page.window.width else 1400,
            height=self.page.window.height if self.page.window.height else 900,
            left=0,
            top=0,
        )
    
    def _start_strobe_flash(self):
        """Start strobe flash background effect"""
        def flash():
            original_bgcolor = self.page.bgcolor
            
            while self.is_active:
                # Flash red
                self.page.bgcolor = ft.Colors.RED_700
                self.page.update()
                time.sleep(self.flash_interval)
                
                if not self.is_active:
                    break
                
                # Back to dark
                self.page.bgcolor = ft.Colors.with_opacity(0.8, ft.Colors.BLACK)
                self.page.update()
                time.sleep(self.flash_interval)
            
            # Restore original background
            self.page.bgcolor = original_bgcolor
            self.page.update()
        
        self.flash_thread = threading.Thread(target=flash, daemon=True)
        self.flash_thread.start()
    
    def dismiss_alert(self, e):
        """Dismiss the emergency alert"""
        self.is_active = False
        
        # Wait a bit for threads to stop
        time.sleep(0.1)
        
        # Remove overlay
        if self.overlay_container in self.page.overlay:
            self.page.overlay.remove(self.overlay_container)
        
        self.page.update()
        
        # Show confirmation
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("✓ Cảnh báo đã được xác nhận"),
            bgcolor=ft.Colors.GREEN
        )
        self.page.snack_bar.open = True
        self.page.update()


# Helper function to check if sound is emergency
def is_emergency_sound(sound_label: str, confidence: float, threshold: float = None) -> bool:
    """
    Check if detected sound is emergency
    
    Args:
        sound_label: Detected sound label
        confidence: Confidence percentage
        threshold: Minimum confidence threshold for alert (uses app_state if None)
    
    Returns:
        True if emergency alert should be triggered
    """
    from src.utils.state import app_state
    
    # Use app_state threshold if not provided
    if threshold is None:
        threshold = app_state.get_setting('confidence_threshold')
    
    EMERGENCY_SOUNDS = ["siren", "car_horn", "crackling_fire", "crying_baby", "glass_breaking", "fireworks"]
    
    return sound_label.lower() in EMERGENCY_SOUNDS and confidence >= threshold

