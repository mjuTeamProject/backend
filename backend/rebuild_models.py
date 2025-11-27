"""
Manually rebuild models from extracted h5 weights
"""
import os
import h5py
import numpy as np
import tensorflow as tf
from tensorflow import keras

def rebuild_sky_model(h5_path, output_path):
    """
    Rebuild sky model based on inspection:
    - Input: 20 features (one-hot encoded sky stems)
    - Architecture: Dense(128) -> 7x[Dense(128) + Dropout] -> Dense(1)
    """
    print(f"\nRebuilding Sky Model...")
    
    # Create model architecture
    model = keras.Sequential([
        keras.layers.Input(shape=(20,)),
        keras.layers.Dense(128, activation='relu', name='dense1'),
        keras.layers.Dropout(0.2, name='dropout_14'),
        keras.layers.Dense(128, activation='relu', name='dense_14'),
        keras.layers.Dropout(0.2, name='dropout_15'),
        keras.layers.Dense(128, activation='relu', name='dense_15'),
        keras.layers.Dropout(0.2, name='dropout_16'),
        keras.layers.Dense(128, activation='relu', name='dense_16'),
        keras.layers.Dropout(0.2, name='dropout_17'),
        keras.layers.Dense(128, activation='relu', name='dense_17'),
        keras.layers.Dropout(0.2, name='dropout_18'),
        keras.layers.Dense(128, activation='relu', name='dense_18'),
        keras.layers.Dropout(0.2, name='dropout_19'),
        keras.layers.Dense(128, activation='relu', name='dense_19'),
        keras.layers.Dropout(0.2, name='dropout_20'),
        keras.layers.Dense(128, activation='relu', name='dense_20'),
        keras.layers.Dense(1, activation='sigmoid', name='output')
    ])
    
    # Load weights manually
    with h5py.File(h5_path, 'r') as f:
        weight_names = [
            'dense1', 'dense_14', 'dense_15', 'dense_16',
            'dense_17', 'dense_18', 'dense_19', 'dense_20', 'output'
        ]
        
        for layer_name in weight_names:
            layer = model.get_layer(layer_name)
            kernel = f[f'model_weights/{layer_name}/{layer_name}/kernel'][:]
            bias = f[f'model_weights/{layer_name}/{layer_name}/bias'][:]
            layer.set_weights([kernel, bias])
            print(f"  Loaded {layer_name}: kernel {kernel.shape}, bias {bias.shape}")
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    # Save in TensorFlow 2.x format
    model.save(output_path, save_format='h5')
    print(f"✓ Saved to: {output_path}")
    
    # Test prediction
    test_input = np.random.rand(1, 20)
    prediction = model.predict(test_input, verbose=0)
    print(f"  Test prediction: {prediction[0][0]:.4f}")
    
    return model

def rebuild_earth_model(h5_path, output_path):
    """
    Rebuild earth model based on inspection:
    - Input: 24 features (one-hot encoded earth branches)
    - Architecture: Dense(128) -> 7x[Dense(128) + Dropout] -> Dense(1)
    """
    print(f"\nRebuilding Earth Model...")
    
    # Create model architecture
    model = keras.Sequential([
        keras.layers.Input(shape=(24,)),
        keras.layers.Dense(128, activation='relu', name='dense1'),
        keras.layers.Dropout(0.2, name='dropout_21'),
        keras.layers.Dense(128, activation='relu', name='dense_21'),
        keras.layers.Dropout(0.2, name='dropout_22'),
        keras.layers.Dense(128, activation='relu', name='dense_22'),
        keras.layers.Dropout(0.2, name='dropout_23'),
        keras.layers.Dense(128, activation='relu', name='dense_23'),
        keras.layers.Dropout(0.2, name='dropout_24'),
        keras.layers.Dense(128, activation='relu', name='dense_24'),
        keras.layers.Dropout(0.2, name='dropout_25'),
        keras.layers.Dense(128, activation='relu', name='dense_25'),
        keras.layers.Dropout(0.2, name='dropout_26'),
        keras.layers.Dense(128, activation='relu', name='dense_26'),
        keras.layers.Dropout(0.2, name='dropout_27'),
        keras.layers.Dense(128, activation='relu', name='dense_27'),
        keras.layers.Dense(1, activation='sigmoid', name='output')
    ])
    
    # Load weights manually
    with h5py.File(h5_path, 'r') as f:
        weight_names = [
            'dense1', 'dense_21', 'dense_22', 'dense_23',
            'dense_24', 'dense_25', 'dense_26', 'dense_27', 'output'
        ]
        
        for layer_name in weight_names:
            layer = model.get_layer(layer_name)
            kernel = f[f'model_weights/{layer_name}/{layer_name}/kernel'][:]
            bias = f[f'model_weights/{layer_name}/{layer_name}/bias'][:]
            layer.set_weights([kernel, bias])
            print(f"  Loaded {layer_name}: kernel {kernel.shape}, bias {bias.shape}")
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    # Save in TensorFlow 2.x format
    model.save(output_path, save_format='h5')
    print(f"✓ Saved to: {output_path}")
    
    # Test prediction
    test_input = np.random.rand(1, 24)
    prediction = model.predict(test_input, verbose=0)
    print(f"  Test prediction: {prediction[0][0]:.4f}")
    
    return model

def main():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    
    # Rebuild sky model
    sky_input = os.path.join(models_dir, 'sky3000.h5')
    sky_output = os.path.join(models_dir, 'sky3000_v2.h5')
    
    if os.path.exists(sky_input):
        sky_model = rebuild_sky_model(sky_input, sky_output)
    else:
        print(f"⚠ Sky model not found: {sky_input}")
    
    # Rebuild earth model
    earth_input = os.path.join(models_dir, 'earth3000.h5')
    earth_output = os.path.join(models_dir, 'earth3000_v2.h5')
    
    if os.path.exists(earth_input):
        earth_model = rebuild_earth_model(earth_input, earth_output)
    else:
        print(f"⚠ Earth model not found: {earth_input}")
    
    print("\n" + "="*60)
    print("✓ Model conversion complete!")
    print("="*60)
    print(f"\nNew model files:")
    print(f"  - {sky_output}")
    print(f"  - {earth_output}")
    print(f"\nUpdate your .env file:")
    print(f"  SKY_MODEL_PATH=./models/sky3000_v2.h5")
    print(f"  EARTH_MODEL_PATH=./models/earth3000_v2.h5")

if __name__ == '__main__':
    main()
