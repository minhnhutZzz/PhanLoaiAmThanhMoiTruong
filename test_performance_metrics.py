"""
Demo Script for Testing Performance Metrics
This script demonstrates how to use the performance tracking system
"""
import time
import numpy as np
from src.utils.performance_metrics import performance_metrics


def simulate_preprocessing():
    """Simulate audio preprocessing"""
    time.sleep(0.045)  # Simulate 45ms preprocessing
    return np.random.rand(1, 1, 128, 431).astype(np.float32)


def simulate_inference(data):
    """Simulate model inference"""
    time.sleep(0.120)  # Simulate 120ms inference
    return np.random.rand(50)  # Mock predictions


def simulate_postprocessing(predictions):
    """Simulate result postprocessing"""
    time.sleep(0.002)  # Simulate 2ms postprocessing
    top_idx = np.argmax(predictions)
    return {
        'class': top_idx,
        'confidence': predictions[top_idx] * 100
    }


def test_single_inference():
    """Test single inference with timing"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Single Inference Timing")
    print("="*60)
    
    # Start measurement
    performance_metrics.start_measurement()
    
    # Phase 1: Preprocessing
    performance_metrics.mark_phase_start('preprocessing')
    data = simulate_preprocessing()
    performance_metrics.mark_phase_end('preprocessing')
    
    # Phase 2: Inference
    performance_metrics.mark_phase_start('inference')
    predictions = simulate_inference(data)
    performance_metrics.mark_phase_end('inference')
    
    # Phase 3: Postprocessing
    performance_metrics.mark_phase_start('postprocessing')
    result = simulate_postprocessing(predictions)
    performance_metrics.mark_phase_end('postprocessing')
    
    # End measurement
    performance_metrics.end_measurement()
    
    # Get metrics
    metrics = performance_metrics.get_current_metrics()
    
    print("\n📊 Timing Results:")
    print(f"  Pre-processing Time:  {metrics['preprocessing_time']:>8.2f} ms")
    print(f"  Inference Latency:    {metrics['inference_latency']:>8.2f} ms")
    print(f"  Post-processing Time: {metrics['postprocessing_time']:>8.2f} ms")
    print(f"  ─────────────────────────────────────")
    print(f"  Total Latency:        {metrics['total_latency']:>8.2f} ms")
    print(f"  Real-time FPS:        {metrics['real_time_fps']:>8.2f} FPS")
    
    print("\n✅ Test 1 completed!")


def test_multiple_inferences():
    """Test multiple inferences to see FPS calculation"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Multiple Inferences (FPS Tracking)")
    print("="*60)
    
    num_runs = 10
    print(f"\nRunning {num_runs} consecutive inferences...\n")
    
    for i in range(num_runs):
        # Start measurement
        performance_metrics.start_measurement()
        
        # Preprocessing
        performance_metrics.mark_phase_start('preprocessing')
        data = simulate_preprocessing()
        performance_metrics.mark_phase_end('preprocessing')
        
        # Inference
        performance_metrics.mark_phase_start('inference')
        predictions = simulate_inference(data)
        performance_metrics.mark_phase_end('inference')
        
        # Postprocessing
        performance_metrics.mark_phase_start('postprocessing')
        result = simulate_postprocessing(predictions)
        performance_metrics.mark_phase_end('postprocessing')
        
        # End measurement
        performance_metrics.end_measurement()
        
        metrics = performance_metrics.get_current_metrics()
        
        print(f"  Run {i+1:2d}: Inference={metrics['inference_latency']:6.2f}ms, "
              f"Total={metrics['total_latency']:6.2f}ms, "
              f"FPS={metrics['real_time_fps']:5.2f}")
    
    print("\n📊 Final Metrics:")
    final_metrics = performance_metrics.get_current_metrics()
    print(f"  Average FPS (last {num_runs} runs): {final_metrics['real_time_fps']:.2f}")
    
    print("\n✅ Test 2 completed!")


def test_model_metadata():
    """Test model metadata retrieval"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Model Metadata")
    print("="*60)
    
    metadata = performance_metrics.get_model_metadata()
    
    print("\n🤖 Model Information:")
    for key, value in metadata.items():
        print(f"  {key.replace('_', ' ').title():20s}: {value}")
    
    print("\n✅ Test 3 completed!")


def test_reset():
    """Test metrics reset"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Reset Metrics")
    print("="*60)
    
    print("\n📊 Before reset:")
    metrics_before = performance_metrics.get_current_metrics()
    for key, value in metrics_before.items():
        print(f"  {key}: {value:.2f}")
    
    print("\n🔄 Resetting metrics...")
    performance_metrics.reset()
    
    print("\n📊 After reset:")
    metrics_after = performance_metrics.get_current_metrics()
    for key, value in metrics_after.items():
        print(f"  {key}: {value:.2f}")
    
    print("\n✅ Test 4 completed!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 PERFORMANCE METRICS DEMO")
    print("="*60)
    print("\nThis script demonstrates the performance tracking system")
    print("used in the Technical Stats Dashboard.\n")
    
    try:
        # Run tests
        test_single_inference()
        time.sleep(1)
        
        test_multiple_inferences()
        time.sleep(1)
        
        test_model_metadata()
        time.sleep(1)
        
        test_reset()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n💡 Tip: Run the main app (python main.py) to see these")
        print("   metrics in the beautiful UI dashboard!")
        print("\n🎯 Navigate to 'Tech Stats' tab after running an inference")
        print("   from 'File Analysis' or 'Live Monitor'.\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
