"""
Live Monitor View - Real-time audio monitoring and classification
"""
import flet as ft
import numpy as np
import sounddevice as sd
import threading
import queue
import time
from io import BytesIO
import base64

from src.ai.audio_processor import generate_mel_spectrogram, preprocess_for_model, waveform_to_image
from src.ai.model_handler import SoundClassifier
from src.utils.state import app_state


class LiveMonitorView:
    """Live audio monitoring with real-time classification"""
    
    def __init__(self, page: ft.Page, classifier: SoundClassifier):
        self.page = page
        self.classifier = classifier
        
        # Audio settings
        self.sample_rate = 44100  # Match training sample rate
        self.duration = 2.0  # Analyze every 2 seconds
        self.buffer_size = int(self.sample_rate * self.duration)
        
        # Recording state
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # UI elements
        self.start_button = None
        self.stop_button = None
        self.status_text = None
        self.waveform_image = None
        self.prediction_container = None
        self.alert_overlay = None
        
        # Prediction thread
        self.prediction_thread = None
        self.should_stop = False
    
    def build(self):
        # Control buttons
        self.start_button = ft.ElevatedButton(
            "🎙️ Start Monitoring",
            icon=ft.Icons.MIC,
            on_click=self.start_recording,
            style=ft.ButtonStyle(
                bgcolor="#10B981",
                color="white"
            )
        )
        
        self.stop_button = ft.ElevatedButton(
            "⏹️ Stop",
            icon=ft.Icons.STOP,
            on_click=self.stop_recording,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor="#EF4444",
                color="white"
            )
        )
        
        # Status
        self.status_text = ft.Text(
            "⚪ Not Recording",
            size=16,
            color="#94A3B8"
        )
        
        # Waveform display
        self.waveform_image = ft.Image(
            visible=False,
            width=800,
            height=250,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Prediction display
        self.prediction_container = ft.Container(
            visible=False,
            padding=20,
            border=ft.border.all(2, "#00D9FF"),
            border_radius=10,
            bgcolor="#1E293B"
        )
        
        # Alert overlay (for visual alerts)
        self.alert_overlay = ft.Container(
            visible=False,
            bgcolor="#EF4444",
            opacity=0.3,
            expand=True
        )
        
        # Layout
        return ft.Stack([
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🎙️ Live Monitor",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#00D9FF"
                    ),
                    ft.Divider(color="#334155"),
                    
                    # Controls
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Controls", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                self.start_button,
                                self.stop_button,
                                self.status_text
                            ], spacing=15),
                            ft.Text(
                                "⚠️ Make sure your microphone is connected and permissions are granted",
                                size=12,
                                color="#F59E0B",
                                italic=True
                            )
                        ], spacing=15),
                        padding=20,
                        border=ft.border.all(1, "#334155"),
                        border_radius=10,
                        bgcolor="#1E293B"
                    ),
                    
                    ft.Container(height=20),
                    
                    # Waveform
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Live Waveform", size=18, weight=ft.FontWeight.BOLD),
                            self.waveform_image,
                        ], spacing=15),
                        padding=20,
                        border=ft.border.all(1, "#334155"),
                        border_radius=10,
                        bgcolor="#1E293B"
                    ),
                    
                    ft.Container(height=20),
                    
                    # Current prediction
                    self.prediction_container,
                    
                ], scroll=ft.ScrollMode.AUTO, spacing=0),
                padding=20,
                expand=True
            ),
            self.alert_overlay
        ])
    
    def start_recording(self, e):
        """Start live audio monitoring"""
        try:
            self.is_recording = True
            self.should_stop = False
            
            # Update UI
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.status_text.value = "🔴 Recording..."
            self.status_text.color = "#EF4444"
            self.page.update()
            
            # Start audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.audio_callback,
                blocksize=1024
            )
            self.stream.start()
            
            # Start prediction thread
            self.prediction_thread = threading.Thread(target=self._prediction_loop, daemon=True)
            self.prediction_thread.start()
            
            # Show notification
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("🎙️ Live monitoring started"),
                bgcolor="#10B981"
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        except Exception as ex:
            self._show_error(f"Failed to start recording: {str(ex)}")
            self.stop_recording(None)
    
    def stop_recording(self, e):
        """Stop live audio monitoring"""
        self.is_recording = False
        self.should_stop = True
        
        # Stop stream
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Update UI
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.status_text.value = "⚪ Not Recording"
        self.status_text.color = "#94A3B8"
        self.page.update()
    
    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream"""
        if status:
            print(f"Audio status: {status}")
        
        # Add to queue
        self.audio_queue.put(indata.copy())
    
    def _prediction_loop(self):
        """Background thread for continuous prediction"""
        audio_buffer = []
        
        while not self.should_stop:
            try:
                # Collect audio chunks
                while len(audio_buffer) < self.buffer_size:
                    if self.should_stop:
                        return
                    
                    try:
                        chunk = self.audio_queue.get(timeout=0.1)
                        audio_buffer.extend(chunk.flatten())
                    except queue.Empty:
                        continue
                
                # Get buffer for analysis
                audio_data = np.array(audio_buffer[:self.buffer_size], dtype=np.float32)
                audio_buffer = audio_buffer[self.buffer_size:]
                
                # Update waveform
                self._update_waveform(audio_data)
                
                # Generate spectrogram
                mel_spec = generate_mel_spectrogram(audio_data, self.sample_rate)
                
                # Preprocess
                preprocessed = preprocess_for_model(mel_spec)
                
                # Predict
                result = self.classifier.predict(preprocessed)
                
                # Check threshold
                threshold = app_state.get_setting('confidence_threshold')
                if result['confidence'] >= threshold:
                    # Add to history
                    app_state.add_to_history(
                        result['label'],
                        result['confidence'],
                        source="live"
                    )
                    
                    # Update prediction display
                    self._update_prediction(result)
                    
                    # Show notification if enabled
                    if app_state.get_setting('enable_notifications'):
                        self._show_notification(result)
                    
                    # Visual alert for alert sounds
                    if result['is_alert'] and app_state.get_setting('enable_visual_alerts'):
                        self._trigger_visual_alert()
                
                # Small delay
                time.sleep(0.1)
                
            except Exception as ex:
                print(f"Prediction error: {ex}")
                time.sleep(0.5)
    
    def _update_waveform(self, audio_data):
        """Update waveform display"""
        try:
            # Generate waveform image
            waveform_img = waveform_to_image(audio_data, self.sample_rate)
            
            # Convert to base64
            self.waveform_image.src_base64 = self._image_to_base64(waveform_img)
            self.waveform_image.visible = True
            self.page.update()
            
        except Exception as ex:
            print(f"Waveform update error: {ex}")
    
    def _update_prediction(self, result):
        """Update prediction display"""
        try:
            self.prediction_container.content = ft.Row([
                ft.Text(result['icon'], size=50),
                ft.Column([
                    ft.Text(
                        result['label'].replace('_', ' ').title(),
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#00D9FF"
                    ),
                    ft.Text(
                        f"Confidence: {result['confidence']:.2f}%",
                        size=16,
                        color="#10B981"
                    ),
                    ft.Text(
                        f"Source: Live Monitor",
                        size=12,
                        color="#94A3B8",
                        italic=True
                    ),
                ], spacing=5)
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
            
            self.prediction_container.visible = True
            self.page.update()
            
        except Exception as ex:
            print(f"Prediction display error: {ex}")
    
    def _show_notification(self, result):
        """Show snackbar notification"""
        try:
            alert_emoji = "🚨" if result['is_alert'] else "🔊"
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"{alert_emoji} Detected: {result['label'].replace('_', ' ').title()} ({result['confidence']:.1f}%)"
                ),
                bgcolor="#EF4444" if result['is_alert'] else "#00D9FF"
            )
            self.page.snack_bar.open = True
            self.page.update()
        except:
            pass
    
    def _trigger_visual_alert(self):
        """Flash screen red for alert sounds"""
        try:
            self.alert_overlay.visible = True
            self.page.update()
            
            # Hide after 0.5 seconds
            threading.Timer(0.5, self._hide_alert).start()
        except:
            pass
    
    def _hide_alert(self):
        """Hide visual alert"""
        try:
            self.alert_overlay.visible = False
            self.page.update()
        except:
            pass
    
    def _show_error(self, message: str):
        """Show error message"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"❌ {message}"),
            bgcolor="#EF4444"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _image_to_base64(self, img):
        """Convert PIL Image to base64"""
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
