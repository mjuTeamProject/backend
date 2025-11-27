"""
Convert legacy Keras 1.x models to TensorFlow 2.x compatible format.
This script attempts multiple conversion strategies.
"""
import os
import sys
import h5py
import numpy as np
import tensorflow as tf
from tensorflow import keras

def inspect_h5_file(filepath):
    """Inspect the structure of the h5 file"""
    print(f"\n{'='*60}")
    print(f"Inspecting: {filepath}")
    print(f"{'='*60}")
    
    with h5py.File(filepath, 'r') as f:
        def print_structure(name, obj):
            print(f"{name}: {type(obj)}")
            if isinstance(obj, h5py.Dataset):
                print(f"  Shape: {obj.shape}, Dtype: {obj.dtype}")
        
        f.visititems(print_structure)

def convert_with_tf1_compatibility(input_path, output_path):
    """Try loading with TF1 compatibility mode"""
    print(f"\n[Strategy 1] Loading with TF1 compatibility mode...")
    try:
        # Use tf.compat.v1 APIs
        import tensorflow.compat.v1 as tf_v1
        tf_v1.disable_v2_behavior()
        
        # Try loading
        model = keras.models.load_model(input_path, compile=False)
        print(f"✓ Loaded successfully with TF1 compatibility")
        
        # Re-enable V2 and save in new format
        tf_v1.enable_v2_behavior()
        model.save(output_path, save_format='h5')
        print(f"✓ Saved to: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def convert_by_rebuilding(input_path, output_path):
    """Rebuild model from scratch based on h5 weights"""
    print(f"\n[Strategy 2] Rebuilding model from h5 structure...")
    try:
        with h5py.File(input_path, 'r') as f:
            # Extract model config if exists
            if 'model_config' in f.attrs:
                import json
                config = json.loads(f.attrs['model_config'].decode('utf-8'))
                print(f"Model config found: {config.get('class_name', 'Unknown')}")
                
                # Manually rebuild Sequential model
                if config.get('class_name') == 'Sequential':
                    model = keras.Sequential()
                    
                    # Add layers based on config
                    for layer_config in config.get('config', {}).get('layers', []):
                        layer_class = layer_config.get('class_name')
                        layer_params = layer_config.get('config', {})
                        
                        # Fix batch_shape to input_shape for InputLayer
                        if layer_class == 'InputLayer' and 'batch_shape' in layer_params:
                            batch_shape = layer_params.pop('batch_shape')
                            if batch_shape:
                                layer_params['input_shape'] = batch_shape[1:]
                        
                        print(f"  Adding layer: {layer_class} - {layer_params.get('name', 'unnamed')}")
                        
                        # Create layer
                        if layer_class == 'Dense':
                            model.add(keras.layers.Dense(**{
                                k: v for k, v in layer_params.items() 
                                if k in ['units', 'activation', 'name']
                            }))
                        elif layer_class == 'Dropout':
                            model.add(keras.layers.Dropout(**{
                                k: v for k, v in layer_params.items() 
                                if k in ['rate', 'name']
                            }))
                        elif layer_class == 'InputLayer':
                            # Skip InputLayer as it's added automatically
                            pass
                    
                    # Build model
                    if len(model.layers) > 0:
                        # Try to load weights
                        try:
                            model.load_weights(input_path)
                            print(f"✓ Weights loaded successfully")
                        except Exception as we:
                            print(f"⚠ Could not load weights: {we}")
                        
                        # Save in new format
                        model.save(output_path, save_format='h5')
                        print(f"✓ Saved to: {output_path}")
                        return True
                
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def convert_weights_only(input_path, output_path):
    """Extract and save only weights as numpy arrays"""
    print(f"\n[Strategy 3] Extracting weights to numpy format...")
    try:
        with h5py.File(input_path, 'r') as f:
            weights = {}
            
            def extract_weights(name, obj):
                if isinstance(obj, h5py.Dataset):
                    weights[name] = obj[:]
            
            f.visititems(extract_weights)
            
            # Save as npz
            npz_path = output_path.replace('.h5', '_weights.npz')
            np.savez(npz_path, **weights)
            print(f"✓ Saved weights to: {npz_path}")
            print(f"  Total weight arrays: {len(weights)}")
            return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    
    model_files = [
        ('sky3000.h5', 'sky3000_converted.h5'),
        ('earth3000.h5', 'earth3000_converted.h5')
    ]
    
    for input_name, output_name in model_files:
        input_path = os.path.join(models_dir, input_name)
        output_path = os.path.join(models_dir, output_name)
        
        if not os.path.exists(input_path):
            print(f"⚠ File not found: {input_path}")
            continue
        
        # Inspect file structure
        inspect_h5_file(input_path)
        
        # Try conversion strategies in order
        strategies = [
            convert_by_rebuilding,
            convert_weights_only,
        ]
        
        success = False
        for strategy in strategies:
            if strategy(input_path, output_path):
                success = True
                break
        
        if not success:
            print(f"\n✗ All conversion strategies failed for {input_name}")
        else:
            print(f"\n✓ Successfully converted {input_name}")

if __name__ == '__main__':
    main()
