"""
Model Downloader
Download ConvNeXt-Tiny model from Google Drive
"""
import os
from pathlib import Path

try:
    import gdown
    GDOWN_AVAILABLE = True
except ImportError:
    GDOWN_AVAILABLE = False
    print("[WARNING] gdown not installed. Installing now...")
    import subprocess
    subprocess.check_call(["pip", "install", "gdown"])
    import gdown
    GDOWN_AVAILABLE = True


def check_model_exists(model_path: str) -> bool:
    """
    Check if model file exists
    
    Args:
        model_path: Path to model file
    
    Returns:
        bool: True if exists, False otherwise
    """
    if not os.path.exists(model_path):
        return False
    
    # Check file size (should be > 100MB)
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    if size_mb < 10:  # Less than 10MB is likely HTML error page
        print(f"[WARNING] Model file too small ({size_mb:.2f} MB), likely corrupted")
        return False
    
    return True


def download_convnext_model(model_dir: str = "models", progress_callback=None) -> bool:
    """
    Download ConvNeXt-Tiny model from Google Drive
    
    Args:
        model_dir: Directory to save model
        progress_callback: Optional callback function(current, total)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Google Drive file ID
    FILE_ID = "1Wa8e88uWznB1fwoqSNaZ2qiEgqbwIlWL"
    
    # Construct download URL
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    
    # Model filename
    MODEL_FILENAME = "best_convnext_tiny.pth"
    
    # Expected file size (approximately 115 MB)
    EXPECTED_SIZE = 115 * 1024 * 1024  # 115 MB in bytes
    
    # Create models directory if not exists
    os.makedirs(model_dir, exist_ok=True)
    
    # Destination path
    destination = os.path.join(model_dir, MODEL_FILENAME)
    
    # Check if already exists
    if check_model_exists(destination):
        print(f"[INFO] Model already exists: {destination}")
        return True
    
    print(f"[INFO] Downloading model from Google Drive...")
    print(f"[INFO] URL: {url}")
    print(f"[INFO] Destination: {destination}")
    
    # Start progress monitoring in background if callback provided
    import threading
    import time
    stop_monitoring = False
    
    def monitor_progress():
        """Monitor download progress by checking file size"""
        while not stop_monitoring:
            if os.path.exists(destination):
                current_size = os.path.getsize(destination)
                if progress_callback:
                    progress_callback(current_size, EXPECTED_SIZE)
            time.sleep(0.5)  # Update every 0.5 seconds
    
    # Start monitoring thread if callback provided
    if progress_callback:
        monitor_thread = threading.Thread(target=monitor_progress, daemon=True)
        monitor_thread.start()
    
    try:
        # Download using gdown (quiet=False to show progress in terminal)
        print("[INFO] Downloading... Check progress below:")
        gdown.download(url, destination, quiet=False, fuzzy=True)
        
        # Stop monitoring
        stop_monitoring = True
        if progress_callback:
            time.sleep(0.6)  # Wait for monitor thread to finish
        
        # Verify download
        if check_model_exists(destination):
            # Final progress update
            final_size = os.path.getsize(destination)
            if progress_callback:
                progress_callback(final_size, final_size)
            
            print(f"[SUCCESS] Model downloaded successfully!")
            print(f"[INFO] File size: {final_size / (1024*1024):.2f} MB")
            return True
        else:
            print(f"[ERROR] Download failed - file too small or corrupted")
            if os.path.exists(destination):
                os.remove(destination)
            return False
            
    except Exception as e:
        stop_monitoring = True
        print(f"[ERROR] Download failed: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False


def get_model_info(model_path: str) -> dict:
    """
    Get model file information
    
    Args:
        model_path: Path to model file
    
    Returns:
        dict: Model information
    """
    if not os.path.exists(model_path):
        return {
            'exists': False,
            'size_mb': 0,
            'path': model_path
        }
    
    size_bytes = os.path.getsize(model_path)
    size_mb = size_bytes / (1024 * 1024)
    
    return {
        'exists': True,
        'size_mb': size_mb,
        'size_bytes': size_bytes,
        'path': model_path
    }
