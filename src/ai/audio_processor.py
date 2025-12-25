"""
Audio Processing Module - EXACT MATCH với code Kaggle
"""
import torch
import torchaudio
import torchaudio.transforms as T
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image


# Constants - match Kaggle exactly
SR = 44100
N_MELS = 128
FIXED_WIDTH = 431


def load_and_preprocess_audio(file_path, device='cpu'):
    """
    Load and preprocess audio EXACTLY like Kaggle code
    
    Args:
        file_path: Path to audio file
        device: torch device ('cpu' or 'cuda')
    
    Returns:
        preprocessed: Tensor ready for model (1, 1, 128, 431)
        spec_for_display: Mel-spectrogram for visualization (before normalization)
    """
    # a. Load audio (trying to use torchaudio.load directly, fallback to soundfile)
    try:
        waveform, sr = torchaudio.load(file_path)
    except Exception as e:
        # Fallback to soundfile if torchaudio.load fails
        import soundfile as sf
        audio_data, sr = sf.read(file_path, dtype='float32')
        waveform = torch.from_numpy(audio_data).float()
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        else:
            waveform = waveform.t()
    
    # b. Convert to mono (EXACTLY like Kaggle)
    if waveform.shape[0] > 1:
        waveform = waveform.mean(0, keepdim=True)
    
    # c. Resample to 44100 (EXACTLY like Kaggle)
    if sr != SR:
        waveform = T.Resample(sr, SR)(waveform)
    
    # d. Create Mel-Spectrogram (EXACTLY like Kaggle)
    mel_spec = T.MelSpectrogram(
        sample_rate=SR, 
        n_fft=2048, 
        hop_length=512, 
        n_mels=N_MELS
    ).to(device)
    
    db_trans = T.AmplitudeToDB(top_db=80).to(device)
    
    # e. Generate spectrogram
    with torch.no_grad():
        spec = db_trans(mel_spec(waveform.to(device))).cpu().squeeze(0)
        
        # Keep a copy for display (before normalization)
        spec_for_display = spec.clone()
        
        # f. Z-score normalization (EXACTLY like Kaggle)
        spec = (spec - spec.mean()) / (spec.std() + 1e-6)
        
        # g. Fixed width 128x431 (EXACTLY like Kaggle)
        if spec.shape[1] < FIXED_WIDTH:
            spec = F.pad(spec, (0, FIXED_WIDTH - spec.shape[1]))
        else:
            spec = spec[:, :FIXED_WIDTH]
        
        # h. Add batch and channel dimensions and convert to numpy
        preprocessed = spec.unsqueeze(0).unsqueeze(0).numpy().astype(np.float32)  # (1, 1, 128, 431)
    
    return preprocessed, spec_for_display


def mel_spectrogram_to_image(spec_tensor):
    """
    Convert mel-spectrogram tensor to PIL Image for display
    
    Args:
        spec_tensor: Mel-spectrogram tensor (2D)
    
    Returns:
        PIL Image object
    """
    # Convert to numpy
    if isinstance(spec_tensor, torch.Tensor):
        spec_np = spec_tensor.numpy()
    else:
        spec_np = spec_tensor
    
    plt.figure(figsize=(10, 4))
    plt.imshow(spec_np, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Mel Frequency')
    plt.tight_layout()
    
    # Save to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return Image.open(buf)


def waveform_to_image(waveform_tensor, sr=44100):
    """
    Convert audio waveform to PIL Image for display
    
    Args:
        waveform_tensor: Waveform tensor
        sr: Sample rate
    
    Returns:
        PIL Image object
    """
    # Convert to numpy
    if isinstance(waveform_tensor, torch.Tensor):
        audio = waveform_tensor.squeeze().numpy()
    else:
        audio = waveform_tensor
    
    plt.figure(figsize=(10, 3))
    time = np.arange(len(audio)) / sr
    plt.plot(time, audio, color='#00D9FF', linewidth=0.5)
    plt.fill_between(time, audio, alpha=0.3, color='#00D9FF')
    plt.title('Waveform', color='white')
    plt.xlabel('Time (s)', color='white')
    plt.ylabel('Amplitude', color='white')
    plt.grid(True, alpha=0.2)
    
    # Dark background
    plt.gca().set_facecolor('#1E1E2E')
    plt.gcf().patch.set_facecolor('#1E1E2E')
    plt.tick_params(colors='white')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#1E1E2E')
    plt.close()
    buf.seek(0)
    
    return Image.open(buf)


# ============================================================
# BACKWARD COMPATIBILITY FUNCTIONS (for existing code)
# ============================================================

def load_audio(file_path, sr=44100, duration=5.0):
    """
    Backward compatibility wrapper
    Returns: numpy array, sample rate
    """
    try:
        waveform, sample_rate = torchaudio.load(file_path)
    except:
        import soundfile as sf
        audio_data, sample_rate = sf.read(file_path, dtype='float32')
        waveform = torch.from_numpy(audio_data).float()
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        else:
            waveform = waveform.t()
    
    if waveform.shape[0] > 1:
        waveform = waveform.mean(0, keepdim=True)
    
    return waveform.squeeze().numpy(), sample_rate


def generate_mel_spectrogram(audio, sr=44100, n_mels=128, n_fft=2048, hop_length=512):
    """
    Backward compatibility wrapper
    Returns: numpy array (mel-spectrogram in dB)
    """
    if isinstance(audio, np.ndarray):
        audio = torch.from_numpy(audio).unsqueeze(0)
    
    device = torch.device('cpu')
    mel_spec = T.MelSpectrogram(
        sample_rate=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    ).to(device)
    
    db_trans = T.AmplitudeToDB(top_db=80).to(device)
    
    with torch.no_grad():
        spec = db_trans(mel_spec(audio.to(device))).cpu().squeeze(0)
    
    return spec.numpy()


def preprocess_for_model(mel_spec, target_shape=(128, 431)):
    """
    Backward compatibility wrapper
    Returns: numpy array (1, 1, 128, 431)
    """
    if isinstance(mel_spec, np.ndarray):
        mel_spec = torch.from_numpy(mel_spec)
    
    # Z-score normalization
    spec = (mel_spec - mel_spec.mean()) / (mel_spec.std() + 1e-6)
    
    # Pad or crop
    target_width = target_shape[1]
    if spec.shape[1] < target_width:
        spec = F.pad(spec, (0, target_width - spec.shape[1]))
    else:
        spec = spec[:, :target_width]
    
    # Add dimensions
    spec = spec.unsqueeze(0).unsqueeze(0)
    
    return spec.numpy().astype(np.float32)
