"""
Test different audio processing parameters to find the right configuration
"""
import librosa
import numpy as np
import onnxruntime as ort
from scipy.ndimage import zoom

def test_audio_parameters(audio_path, model_path="models/model.onnx"):
    """Test different combinations of audio parameters"""
    
    # Load model
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    # ESC-50 classes
    classes = [
        "dog", "rooster", "pig", "cow", "frog",
        "cat", "hen", "insects", "sheep", "crow",
        "rain", "sea_waves", "crackling_fire", "crickets", "chirping_birds",
        "water_drops", "wind", "pouring_water", "toilet_flush", "thunderstorm",
        "crying_baby", "sneezing", "clapping", "breathing", "coughing",
        "footsteps", "laughing", "brushing_teeth", "snoring", "drinking_sipping",
        "door_wood_knock", "mouse_click", "keyboard_typing", "door_wood_creaks", "can_opening",
        "washing_machine", "vacuum_cleaner", "clock_alarm", "clock_tick", "glass_breaking",
        "helicopter", "chainsaw", "siren", "car_horn", "engine",
        "train", "church_bells", "airplane", "fireworks", "hand_saw"
    ]
    
    print("="*80)
    print("Testing Different Audio Processing Parameters")
    print("="*80)
    
    # Test configurations
    configs = [
        # (duration, sr, n_fft, hop_length, description)
        (5.0, 22050, 2048, 512, "Current settings"),
        (10.0, 22050, 2048, 512, "Longer duration (10s)"),
        (5.0, 22050, 1024, 256, "Smaller FFT window"),
        (5.0, 22050, 2048, 256, "Smaller hop (more frames)"),
        (5.0, 16000, 2048, 512, "Lower sample rate"),
        (5.0, 44100, 2048, 512, "Higher sample rate"),
    ]
    
    best_dog_prob = 0
    best_config = None
    
    for duration, sr, n_fft, hop_length, desc in configs:
        try:
            # Load audio
            audio, _ = librosa.load(audio_path, sr=sr, duration=duration)
            
            # Generate mel-spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=audio,
                sr=sr,
                n_mels=128,
                n_fft=n_fft,
                hop_length=hop_length
            )
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Resize to 128x431
            target_shape = (128, 431)
            zoom_factors = (target_shape[0] / mel_spec_db.shape[0], 
                          target_shape[1] / mel_spec_db.shape[1])
            resized = zoom(mel_spec_db, zoom_factors, order=1)
            
            # Normalize
            normalized = (resized - resized.min()) / (resized.max() - resized.min() + 1e-8)
            preprocessed = normalized[np.newaxis, np.newaxis, :, :].astype(np.float32)
            
            # Predict
            outputs = session.run([output_name], {input_name: preprocessed})
            logits = outputs[0][0]
            exp_logits = np.exp(logits - np.max(logits))
            probabilities = exp_logits / np.sum(exp_logits)
            
            # Get results
            top_idx = np.argmax(probabilities)
            top_label = classes[top_idx]
            top_prob = probabilities[top_idx] * 100
            
            dog_idx = classes.index('dog')
            dog_prob = probabilities[dog_idx] * 100
            
            print(f"\n{desc}:")
            print(f"  Duration: {duration}s, SR: {sr}, FFT: {n_fft}, Hop: {hop_length}")
            print(f"  Mel-spec shape: {mel_spec_db.shape}")
            print(f"  Top: {top_label} ({top_prob:.2f}%)")
            print(f"  Dog: {dog_prob:.2f}% (rank {np.where(np.argsort(probabilities)[::-1] == dog_idx)[0][0] + 1}/50)")
            
            if dog_prob > best_dog_prob:
                best_dog_prob = dog_prob
                best_config = (duration, sr, n_fft, hop_length, desc, mel_spec_db.shape)
                
        except Exception as e:
            print(f"\n{desc}: ERROR - {e}")
    
    print("\n" + "="*80)
    print("BEST CONFIGURATION FOR DOG:")
    print("="*80)
    if best_config:
        duration, sr, n_fft, hop_length, desc, shape = best_config
        print(f"Config: {desc}")
        print(f"Duration: {duration}s")
        print(f"Sample Rate: {sr}")
        print(f"N_FFT: {n_fft}")
        print(f"Hop Length: {hop_length}")
        print(f"Mel-spec shape: {shape}")
        print(f"Dog probability: {best_dog_prob:.2f}%")
    
    return best_config


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = r"C:\Users\Minh Nhut\Pictures\amthanh\chosua.mp3"
    
    print(f"Testing with: {audio_file}\n")
    best = test_audio_parameters(audio_file)
