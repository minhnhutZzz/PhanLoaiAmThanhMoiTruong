"""
Performance Metrics Tracker
Measures and tracks timing metrics for model inference
"""
import time
from typing import Dict, Optional
from collections import deque


class PerformanceMetrics:
    """Track timing metrics for audio processing and inference"""
    
    def __init__(self, history_size: int = 100):
        """
        Initialize performance tracker
        
        Args:
            history_size: Number of recent measurements to keep for FPS calculation
        """
        self.history_size = history_size
        
        # Current metrics (latest measurement)
        self.preprocessing_time: float = 0.0
        self.inference_time: float = 0.0
        self.postprocessing_time: float = 0.0
        self.total_time: float = 0.0
        
        # History for FPS calculation
        self.inference_history = deque(maxlen=history_size)
        
        # Model metadata
        self.model_metadata = {
            'backbone': 'ConvNeXt-Tiny',
            'parameters': '28.6M',
            'input_resolution': '128x431',
            'model_format': '.pth',
            'optimizer': 'AdamW (Weight Decay: 1e-4)',
            'dataset': 'ESC-50',
            'num_classes': 50,
        }
        
        # Timing context
        self._start_time: Optional[float] = None
        self._phase_times: Dict[str, float] = {}
    
    def start_measurement(self):
        """Start a new measurement cycle"""
        self._start_time = time.perf_counter()
        self._phase_times = {
            'preprocessing': 0.0,
            'inference': 0.0,
            'postprocessing': 0.0
        }
    
    def mark_phase_start(self, phase: str):
        """Mark the start of a processing phase"""
        self._phase_times[f'{phase}_start'] = time.perf_counter()
    
    def mark_phase_end(self, phase: str):
        """Mark the end of a processing phase and calculate duration"""
        end_time = time.perf_counter()
        start_key = f'{phase}_start'
        
        if start_key in self._phase_times:
            duration = (end_time - self._phase_times[start_key]) * 1000  # Convert to ms
            self._phase_times[phase] = duration
            
            # Update metrics
            if phase == 'preprocessing':
                self.preprocessing_time = duration
            elif phase == 'inference':
                self.inference_time = duration
                self.inference_history.append(duration)
            elif phase == 'postprocessing':
                self.postprocessing_time = duration
    
    def end_measurement(self):
        """End measurement and calculate total time"""
        if self._start_time is not None:
            self.total_time = (time.perf_counter() - self._start_time) * 1000  # ms
    
    def get_fps(self) -> float:
        """
        Calculate real-time FPS based on recent inference times
        
        Returns:
            Frames per second (inference throughput)
        """
        if not self.inference_history or self.inference_history[-1] == 0:
            return 0.0
        
        # Use average of recent inferences
        avg_inference_time_ms = sum(self.inference_history) / len(self.inference_history)
        
        if avg_inference_time_ms > 0:
            return 1000.0 / avg_inference_time_ms
        return 0.0
    
    def get_current_metrics(self) -> Dict[str, float]:
        """
        Get current timing metrics
        
        Returns:
            Dictionary with all timing metrics in milliseconds
        """
        return {
            'preprocessing_time': self.preprocessing_time,
            'inference_latency': self.inference_time,
            'postprocessing_time': self.postprocessing_time,
            'total_latency': self.total_time,
            'real_time_fps': self.get_fps()
        }
    
    def get_model_metadata(self) -> Dict[str, str]:
        """
        Get model metadata
        
        Returns:
            Dictionary with model information
        """
        return self.model_metadata.copy()
    
    def update_model_format(self, format_type: str):
        """Update model format (.pth or .onnx)"""
        self.model_metadata['model_format'] = format_type
    
    def reset(self):
        """Reset all metrics"""
        self.preprocessing_time = 0.0
        self.inference_time = 0.0
        self.postprocessing_time = 0.0
        self.total_time = 0.0
        self.inference_history.clear()
        self._start_time = None
        self._phase_times = {}


# Global instance
performance_metrics = PerformanceMetrics()
