"""
Debug script to check model input/output and preprocessing
"""
import numpy as np
import librosa
import matplotlib.pyplot as plt
from src.ai.audio_processor import load_audio, generate_mel_spectrogram, preprocess_for_model
from src.ai.model_handler import SoundClassifier
import onnxruntime as ort

def debug_audio_file(audio_path):
    """Debug audio file processing"""
    print("="*60)
    print(f"Debugging: {audio_path}")
    print("="*60)
    
    # Load audio
    audio, sr = load_audio(audio_path)
    print(f"\n1. Audio loaded:")
    print(f"   - Sample rate: {sr}")
    print(f"   - Duration: {len(audio)/sr:.2f}s")
    print(f"   - Shape: {audio.shape}")
    print(f"   - Min: {audio.min():.4f}, Max: {audio.max():.4f}")
    print(f"   - Mean: {audio.mean():.4f}, Std: {audio.std():.4f}")
    
    # Generate mel-spectrogram
    mel_spec = generate_mel_spectrogram(audio, sr)
    print(f"\n2. Mel-Spectrogram:")
    print(f"   - Shape: {mel_spec.shape}")
    print(f"   - Min: {mel_spec.min():.2f} dB")
    print(f"   - Max: {mel_spec.max():.2f} dB")
    print(f"   - Mean: {mel_spec.mean():.2f} dB")
    
    # Preprocess for model
    preprocessed = preprocess_for_model(mel_spec)
    print(f"\n3. Preprocessed for model:")
    print(f"   - Shape: {preprocessed.shape}")
    print(f"   - Min: {preprocessed.min():.4f}")
    print(f"   - Max: {preprocessed.max():.4f}")
    print(f"   - Mean: {preprocessed.mean():.4f}")
    print(f"   - Std: {preprocessed.std():.4f}")
    
    # Run inference
    print(f"\n4. Running inference...")
    classifier = SoundClassifier(model_path="models/model.onnx")
    
    if not classifier.use_mock:
        # Get raw logits
        session = ort.InferenceSession("models/model.onnx")
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        
        outputs = session.run([output_name], {input_name: preprocessed})
        logits = outputs[0][0]
        
        print(f"   - Raw logits shape: {logits.shape}")
        print(f"   - Logits min: {logits.min():.4f}, max: {logits.max():.4f}")
        
        # Softmax
        exp_logits = np.exp(logits - np.max(logits))
        probabilities = exp_logits / np.sum(exp_logits)
        
        # Top 10 predictions
        top_10_idx = np.argsort(probabilities)[-10:][::-1]
        print(f"\n5. Top 10 Predictions:")
        for i, idx in enumerate(top_10_idx, 1):
            label = classifier.classes[idx]
            prob = probabilities[idx] * 100
            print(f"   {i}. {label:20s} - {prob:6.2f}%")
        
        # Check if 'dog' is in top predictions
        dog_idx = classifier.classes.index('dog')
        dog_prob = probabilities[dog_idx] * 100
        print(f"\n6. 'dog' prediction:")
        print(f"   - Probability: {dog_prob:.2f}%")
        print(f"   - Rank: {np.where(np.argsort(probabilities)[::-1] == dog_idx)[0][0] + 1}/50")
    
    print("\n" + "="*60)
    
    return preprocessed, mel_spec


def test_different_normalizations(audio_path):
    """Test different normalization methods"""
    print("\n" + "="*60)
    print("Testing Different Normalization Methods")
    print("="*60)
    
    audio, sr = load_audio(audio_path)
    mel_spec = generate_mel_spectrogram(audio, sr)
    
    classifier = SoundClassifier(model_path="models/model.onnx")
    if classifier.use_mock:
        print("Model not loaded, skipping normalization tests")
        return
    
    session = ort.InferenceSession("models/model.onnx")
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    methods = {
        "Current (min-max to [0,1])": lambda x: (x - x.min()) / (x.max() - x.min() + 1e-8),
        "StandardScaler (mean=0, std=1)": lambda x: (x - x.mean()) / (x.std() + 1e-8),
        "No normalization": lambda x: x,
        "Clip to [-1, 1]": lambda x: np.clip(x / 80, -1, 1),  # Assuming dB range ~[-80, 0]
    }
    
    for method_name, normalize_func in methods.items():
        # Resize
        from scipy.ndimage import zoom
        target_shape = (128, 431)
        zoom_factors = (target_shape[0] / mel_spec.shape[0], target_shape[1] / mel_spec.shape[1])
        resized = zoom(mel_spec, zoom_factors, order=1)
        
        # Normalize
        normalized = normalize_func(resized)
        preprocessed = normalized[np.newaxis, np.newaxis, :, :].astype(np.float32)
        
        # Predict
        outputs = session.run([output_name], {input_name: preprocessed})
        logits = outputs[0][0]
        exp_logits = np.exp(logits - np.max(logits))
        probabilities = exp_logits / np.sum(exp_logits)
        
        top_idx = np.argmax(probabilities)
        top_label = classifier.classes[top_idx]
        top_prob = probabilities[top_idx] * 100
        
        dog_idx = classifier.classes.index('dog')
        dog_prob = probabilities[dog_idx] * 100
        
        print(f"\n{method_name}:")
        print(f"  Top prediction: {top_label} ({top_prob:.2f}%)")
        print(f"  Dog probability: {dog_prob:.2f}%")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        print("Usage: python debug_model.py <audio_file>")
        print("\nPlease provide path to your dog barking audio file")
        print("Example: python debug_model.py dog_bark.wav")
        sys.exit(1)
    
    # Run debug
    preprocessed, mel_spec = debug_audio_file(audio_file)
    
    # Test different normalizations
    test_different_normalizations(audio_file)
    
    print("\n" + "="*60)
    print("Debug completed!")
    print("="*60)
