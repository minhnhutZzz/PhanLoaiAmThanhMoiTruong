"""
Compare preprocessing between training code and current app
"""
import torch
import torchaudio
import torchaudio.transforms as T
import torch.nn.functional as F
import librosa
import numpy as np
import matplotlib.pyplot as plt

def preprocess_training_style(filepath):
    """
    Preprocess exactly like training code
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load audio with torchaudio (like training)
    waveform, sr = torchaudio.load(filepath)
    
    # Giảm số kênh về 1 kênh
    if waveform.shape[0] > 1:
        waveform = waveform.mean(0, keepdim=True)
    
    # Resample to 44100
    if sr != 44100:
        waveform = T.Resample(sr, 44100)(waveform)
    
    waveform = waveform.to(device)
    
    # Mel spectrogram
    mel = T.MelSpectrogram(sample_rate=44100, n_fft=2048, hop_length=512, n_mels=128).to(device)
    spec = mel(waveform)
    
    # AmplitudeToDB
    db = T.AmplitudeToDB(top_db=80).to(device)
    spec = db(spec)
    
    # Move to CPU
    spec = spec.squeeze(0).cpu()
    
    # Normalize (StandardScaler)
    spec = (spec - spec.mean()) / (spec.std() + 1e-6)
    
    # Pad/Crop to 431 frames
    target_frames = 431
    if spec.shape[1] < target_frames:
        pad = target_frames - spec.shape[1]
        spec = F.pad(spec, (0, pad), mode='constant')
    elif spec.shape[1] > target_frames:
        spec = spec[:, :target_frames]
    
    return spec.unsqueeze(0).unsqueeze(0).numpy()  # (1, 1, 128, 431)


def preprocess_current_app(filepath):
    """
    Preprocess using current app code
    """
    from src.ai.audio_processor import load_audio, generate_mel_spectrogram, preprocess_for_model
    
    audio, sr = load_audio(filepath)
    mel_spec = generate_mel_spectrogram(audio, sr)
    preprocessed = preprocess_for_model(mel_spec)
    
    return preprocessed


def compare_preprocessing(filepath):
    """
    Compare both methods
    """
    print("="*80)
    print(f"Comparing preprocessing for: {filepath}")
    print("="*80)
    
    # Training style
    print("\n1. Training Style Preprocessing:")
    train_spec = preprocess_training_style(filepath)
    print(f"   Shape: {train_spec.shape}")
    print(f"   Min: {train_spec.min():.4f}, Max: {train_spec.max():.4f}")
    print(f"   Mean: {train_spec.mean():.4f}, Std: {train_spec.std():.4f}")
    
    # Current app
    print("\n2. Current App Preprocessing:")
    app_spec = preprocess_current_app(filepath)
    print(f"   Shape: {app_spec.shape}")
    print(f"   Min: {app_spec.min():.4f}, Max: {app_spec.max():.4f}")
    print(f"   Mean: {app_spec.mean():.4f}, Std: {app_spec.std():.4f}")
    
    # Difference
    print("\n3. Difference:")
    diff = np.abs(train_spec - app_spec)
    print(f"   Mean absolute difference: {diff.mean():.6f}")
    print(f"   Max absolute difference: {diff.max():.6f}")
    
    # Visualize
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    axes[0].imshow(train_spec[0, 0], aspect='auto', origin='lower')
    axes[0].set_title('Training Style')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Mel Frequency')
    
    axes[1].imshow(app_spec[0, 0], aspect='auto', origin='lower')
    axes[1].set_title('Current App')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Mel Frequency')
    
    axes[2].imshow(diff[0, 0], aspect='auto', origin='lower', cmap='hot')
    axes[2].set_title('Absolute Difference')
    axes[2].set_xlabel('Time')
    axes[2].set_ylabel('Mel Frequency')
    
    plt.tight_layout()
    plt.savefig('preprocessing_comparison.png', dpi=150)
    print("\n✓ Saved comparison image: preprocessing_comparison.png")
    
    # Test with model
    print("\n4. Testing with PyTorch model:")
    from src.ai.model_handler import SoundClassifier
    
    classifier = SoundClassifier(model_path="models/best_convnext_tiny.pth")
    
    if not classifier.use_mock:
        result_train = classifier.predict(train_spec)
        result_app = classifier.predict(app_spec)
        
        print(f"\n   Training Style Result:")
        print(f"   - Label: {result_train['label']}")
        print(f"   - Confidence: {result_train['confidence']:.2f}%")
        
        print(f"\n   Current App Result:")
        print(f"   - Label: {result_app['label']}")
        print(f"   - Confidence: {result_app['confidence']:.2f}%")
        
        if result_train['label'] != result_app['label']:
            print(f"\n   ⚠️ WARNING: Different predictions!")
        else:
            print(f"\n   ✓ Same prediction!")
    
    return train_spec, app_spec


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        print("Usage: python compare_preprocessing.py <audio_file>")
        print("\nExample: python compare_preprocessing.py 1-30226-A-0.wav")
        sys.exit(1)
    
    train_spec, app_spec = compare_preprocessing(audio_file)
    
    print("\n" + "="*80)
    print("Comparison completed!")
    print("="*80)
