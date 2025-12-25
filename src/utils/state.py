"""
Application State Management
Singleton pattern for shared state across UI components
"""
from datetime import datetime
from typing import List, Dict
import threading


class AppState:
    """
    Singleton class to manage application state
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # History log
        self.history: List[Dict] = []
        
        # Settings
        self.settings = {
            'confidence_threshold': 50.0,  # Minimum confidence to show notification
            'enable_notifications': True,
            'enable_visual_alerts': True,  # Flash screen for alert sounds
            'enable_sound_alerts': False,  # Play sound (future feature)
            'recording': False,  # Live monitor status
        }
        
        # Current prediction (for live monitor)
        self.current_prediction = None
        
        # Model info
        self.model_info = {
            'name': 'ConvNeXt-Tiny',
            'dataset': 'ESC-50',
            'version': 'v1.0',
            'loaded': False
        }
        
        self._initialized = True
    
    def add_to_history(self, label: str, confidence: float, source: str = "file"):
        """
        Add a prediction to history
        
        Args:
            label: Predicted sound label
            confidence: Confidence score (0-100)
            source: Source type ("file" or "live")
        """
        entry = {
            'timestamp': datetime.now(),
            'label': label,
            'confidence': confidence,
            'source': source
        }
        self.history.append(entry)
    
    def get_history(self, limit: int = None):
        """Get history entries (most recent first)"""
        history = sorted(self.history, key=lambda x: x['timestamp'], reverse=True)
        if limit:
            return history[:limit]
        return history
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
    
    def update_setting(self, key: str, value):
        """Update a setting"""
        if key in self.settings:
            self.settings[key] = value
    
    def get_setting(self, key: str):
        """Get a setting value"""
        return self.settings.get(key)
    
    def set_model_loaded(self, loaded: bool):
        """Update model loaded status"""
        self.model_info['loaded'] = loaded
    
    def get_stats(self):
        """Get statistics from history"""
        if not self.history:
            return {
                'total_detections': 0,
                'most_common': None,
                'avg_confidence': 0
            }
        
        total = len(self.history)
        
        # Most common sound
        label_counts = {}
        confidences = []
        
        for entry in self.history:
            label = entry['label']
            label_counts[label] = label_counts.get(label, 0) + 1
            confidences.append(entry['confidence'])
        
        most_common = max(label_counts, key=label_counts.get) if label_counts else None
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'total_detections': total,
            'most_common': most_common,
            'avg_confidence': avg_confidence
        }


# Global state instance
app_state = AppState()
