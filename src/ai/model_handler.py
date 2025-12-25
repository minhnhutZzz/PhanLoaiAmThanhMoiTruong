"""
Sound Classification Model Handler
Handles PyTorch model loading and inference (using .pth directly)
"""
import os
import numpy as np
import torch
import torch.nn as nn
from pathlib import Path


# ESC-50 Dataset Classes (50 environmental sounds)
# IMPORTANT: Must be sorted alphabetically to match training code!
# In training: categories = sorted(df_meta['category'].unique())
ESC50_CLASSES = [
    "airplane", "breathing", "brushing_teeth", "can_opening", "car_horn",
    "cat", "chainsaw", "chirping_birds", "church_bells", "clapping",
    "clock_alarm", "clock_tick", "coughing", "cow", "crackling_fire",
    "crickets", "crow", "crying_baby", "dog", "door_wood_creaks",
    "door_wood_knock", "drinking_sipping", "engine", "fireworks", "footsteps",
    "frog", "glass_breaking", "hand_saw", "helicopter", "hen",
    "insects", "keyboard_typing", "laughing", "mouse_click", "pig",
    "pouring_water", "rain", "rooster", "sea_waves", "sheep",
    "siren", "sneezing", "snoring", "thunderstorm", "toilet_flush",
    "train", "vacuum_cleaner", "washing_machine", "water_drops", "wind"
]

# Icons mapping for each sound class
SOUND_ICONS = {
    "dog": "🐕", "rooster": "🐓", "pig": "🐷", "cow": "🐄", "frog": "🐸",
    "cat": "🐈", "hen": "🐔", "insects": "🦗", "sheep": "🐑", "crow": "🦅",
    "rain": "🌧️", "sea_waves": "🌊", "crackling_fire": "🔥", "crickets": "🦗", "chirping_birds": "🐦",
    "water_drops": "💧", "wind": "💨", "pouring_water": "🚰", "toilet_flush": "🚽", "thunderstorm": "⛈️",
    "crying_baby": "👶", "sneezing": "🤧", "clapping": "👏", "breathing": "😮", "coughing": "😷",
    "footsteps": "👣", "laughing": "😂", "brushing_teeth": "🪥", "snoring": "😴", "drinking_sipping": "🥤",
    "door_wood_knock": "🚪", "mouse_click": "🖱️", "keyboard_typing": "⌨️", "door_wood_creaks": "🚪", "can_opening": "🥫",
    "washing_machine": "🧺", "vacuum_cleaner": "🧹", "clock_alarm": "⏰", "clock_tick": "🕐", "glass_breaking": "🔨",
    "helicopter": "🚁", "chainsaw": "🪚", "siren": "🚨", "car_horn": "🚗", "engine": "🏎️",
    "train": "🚂", "church_bells": "🔔", "airplane": "✈️", "fireworks": "🎆", "hand_saw": "🪚"
}

# Alert sounds (for visual notifications)
ALERT_SOUNDS = ["siren", "car_horn", "glass_breaking", "clock_alarm", "crying_baby", "fireworks"]


class SoundClassifier:
    """
    Sound Classification using PyTorch ConvNeXt model
    """
    
    def __init__(self, model_path="models/best_convnext_tiny.pth", use_mock=False):
        """
        Initialize the classifier
        
        Args:
            model_path: Path to PyTorch .pth file
            use_mock: If True, use mock predictions (for testing without model)
        """
        self.model_path = model_path
        self.use_mock = use_mock
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.classes = ESC50_CLASSES
        
        if not use_mock:
            self._load_model()
        else:
            print("[WARNING] Using MOCK predictor (no model loaded)")
    
    def _load_model(self):
        """Load PyTorch model"""
        try:
            import timm
            
            if not os.path.exists(self.model_path):
                print(f"[WARNING] Model file not found: {self.model_path}")
                print("[WARNING] Switching to MOCK mode")
                self.use_mock = True
                return
            
            # Create ConvNeXt-Tiny model structure
            self.model = timm.create_model('convnext_tiny', pretrained=False, num_classes=50, in_chans=1)
            
            # Load weights
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Handle different checkpoint formats and DataParallel
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    state_dict = checkpoint['model_state_dict']
                elif 'state_dict' in checkpoint:
                    state_dict = checkpoint['state_dict']
                else:
                    state_dict = checkpoint
            else:
                state_dict = checkpoint
            
            # Remove 'module.' prefix if present (from DataParallel)
            new_state_dict = {}
            for key, value in state_dict.items():
                if key.startswith('module.'):
                    new_key = key[7:]  # Remove 'module.' prefix
                    new_state_dict[new_key] = value
                else:
                    new_state_dict[key] = value
            
            # Load state dict
            self.model.load_state_dict(new_state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            print(f"[SUCCESS] PyTorch model loaded successfully: {self.model_path}")
            print(f"[INFO] Using device: {self.device}")
            
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            print("[WARNING] Switching to MOCK mode")
            self.use_mock = True
    
    def predict(self, preprocessed_input):
        """
        Run inference on preprocessed input
        
        Args:
            preprocessed_input: Preprocessed spectrogram (1, 1, 128, 431) as numpy array
        
        Returns:
            dict with 'label', 'confidence', 'icon', 'is_alert'
        """
        if self.use_mock:
            return self._mock_predict()
        
        try:
            # Convert to torch tensor if needed
            if isinstance(preprocessed_input, np.ndarray):
                input_tensor = torch.from_numpy(preprocessed_input).float().to(self.device)
            elif isinstance(preprocessed_input, torch.Tensor):
                input_tensor = preprocessed_input.float().to(self.device)
            else:
                raise TypeError(f"Expected np.ndarray or torch.Tensor, got {type(preprocessed_input)}")
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
            
            # Get probabilities
            probabilities = torch.softmax(outputs, dim=1)[0].cpu().numpy()
            
            # Get top prediction
            top_idx = np.argmax(probabilities)
            top_prob = probabilities[top_idx]
            top_label = self.classes[top_idx]
            
            return {
                'label': top_label,
                'confidence': float(top_prob * 100),
                'icon': SOUND_ICONS.get(top_label, "🔊"),
                'is_alert': top_label in ALERT_SOUNDS,
                'all_probs': probabilities
            }
            
        except Exception as e:
            print(f"[ERROR] Prediction error: {e}")
            return self._mock_predict()
    
    def _mock_predict(self):
        """Mock prediction for testing"""
        import random
        
        mock_classes = ["dog", "cat", "rain", "siren", "keyboard_typing", "laughing"]
        label = random.choice(mock_classes)
        confidence = random.uniform(65, 95)
        
        return {
            'label': label,
            'confidence': confidence,
            'icon': SOUND_ICONS.get(label, "🔊"),
            'is_alert': label in ALERT_SOUNDS,
            'all_probs': None
        }
    
    def get_top_k_predictions(self, preprocessed_input, k=5):
        """
        Get top-k predictions
        
        Args:
            preprocessed_input: Preprocessed spectrogram
            k: Number of top predictions
        
        Returns:
            List of dicts with label, confidence, icon
        """
        result = self.predict(preprocessed_input)
        
        if result['all_probs'] is None:
            # Mock mode
            return [result]
        
        # Get top-k
        probs = result['all_probs']
        top_k_idx = np.argsort(probs)[-k:][::-1]
        
        predictions = []
        for idx in top_k_idx:
            label = self.classes[idx]
            predictions.append({
                'label': label,
                'confidence': float(probs[idx] * 100),
                'icon': SOUND_ICONS.get(label, "🔊")
            })
        
        return predictions
