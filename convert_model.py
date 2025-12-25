"""
Convert PyTorch ConvNeXt model to ONNX format
"""
import torch
import torch.nn as nn
import torchvision.models as models
import os

def convert_to_onnx(pytorch_model_path, onnx_model_path):
    """
    Convert PyTorch model to ONNX format
    
    Args:
        pytorch_model_path: Path to .pth file
        onnx_model_path: Path to save .onnx file
    """
    print(f"Loading PyTorch model from: {pytorch_model_path}")
    
    # Create ConvNeXt-Tiny model
    model = models.convnext_tiny(weights=None)
    
    # Modify the first conv layer to accept 1 channel (grayscale) instead of 3 (RGB)
    # Original: Conv2d(3, 96, kernel_size=(4, 4), stride=(4, 4))
    # New: Conv2d(1, 96, kernel_size=(4, 4), stride=(4, 4))
    model.features[0][0] = nn.Conv2d(1, 96, kernel_size=(4, 4), stride=(4, 4))
    
    # Modify the classifier for 50 classes (ESC-50)
    num_classes = 50
    in_features = model.classifier[2].in_features
    model.classifier[2] = nn.Linear(in_features, num_classes)
    
    # Load weights
    checkpoint = torch.load(pytorch_model_path, map_location='cpu')
    
    # Handle different checkpoint formats
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
    
    # Map old keys to new keys if needed
    # ConvNeXt uses 'features' instead of 'stem' and 'stages'
    final_state_dict = {}
    for key, value in new_state_dict.items():
        # Map stem -> features.0
        if key.startswith('stem.'):
            new_key = key.replace('stem.', 'features.0.')
            final_state_dict[new_key] = value
        # Map stages -> features
        elif key.startswith('stages.'):
            # stages.0 -> features.1, stages.1 -> features.2, etc.
            parts = key.split('.')
            stage_num = int(parts[1])
            new_stage_num = stage_num + 1
            new_key = f"features.{new_stage_num}." + '.'.join(parts[2:])
            final_state_dict[new_key] = value
        # Map head -> classifier
        elif key.startswith('head.'):
            new_key = key.replace('head.', 'classifier.')
            # head.fc -> classifier.2
            new_key = new_key.replace('fc.', '2.')
            # head.norm -> classifier.0
            new_key = new_key.replace('norm.', '0.')
            final_state_dict[new_key] = value
        else:
            final_state_dict[key] = value
    
    model.load_state_dict(final_state_dict, strict=False)
    model.eval()
    
    print("Model loaded successfully!")
    
    # Create dummy input (batch_size=1, channels=1, height=128, width=431)
    dummy_input = torch.randn(1, 1, 128, 431)
    
    print(f"Converting to ONNX format...")
    
    # Export to ONNX
    torch.onnx.export(
        model,
        dummy_input,
        onnx_model_path,
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print(f"[OK] ONNX model saved to: {onnx_model_path}")
    
    # Verify the ONNX model
    import onnx
    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)
    print("[OK] ONNX model verified successfully!")
    
    # Test inference
    print("\nTesting ONNX inference...")
    import onnxruntime as ort
    import numpy as np
    
    session = ort.InferenceSession(onnx_model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    # Test with random input
    test_input = np.random.randn(1, 1, 128, 431).astype(np.float32)
    outputs = session.run([output_name], {input_name: test_input})
    
    print(f"[OK] Inference test passed!")
    print(f"  Output shape: {outputs[0].shape}")
    print(f"  Predicted class: {np.argmax(outputs[0])}")
    
    return True


if __name__ == "__main__":
    # Paths
    pytorch_model = "models/best_convnext_tiny.pth"
    onnx_model = "models/model.onnx"
    
    if not os.path.exists(pytorch_model):
        print(f"Error: PyTorch model not found at {pytorch_model}")
        print("Please make sure the file exists.")
        exit(1)
    
    try:
        convert_to_onnx(pytorch_model, onnx_model)
        print("\n" + "="*50)
        print("Conversion completed successfully!")
        print("You can now run the S-Hear Dashboard application.")
        print("="*50)
    except Exception as e:
        print(f"\nError during conversion: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PyTorch is installed: pip install torch torchvision")
        print("2. Make sure ONNX is installed: pip install onnx")
        print("3. Check if the .pth file is a valid PyTorch checkpoint")
        exit(1)
