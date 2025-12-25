"""
Check if label order matches between training and app
"""
import pandas as pd
import os

# App's current labels
APP_LABELS = [
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
print("APP LABELS (current order):")
print("="*80)
for i, label in enumerate(APP_LABELS):
    print(f"{i:2d}. {label}")

print("\n" + "="*80)
print("TRAINING LABELS (should be sorted alphabetically):")
print("="*80)

# What it SHOULD be (sorted alphabetically like in Kaggle code)
CORRECT_LABELS = sorted(APP_LABELS)
for i, label in enumerate(CORRECT_LABELS):
    print(f"{i:2d}. {label}")

print("\n" + "="*80)
print("COMPARISON:")
print("="*80)

mismatches = []
for i in range(len(APP_LABELS)):
    if APP_LABELS[i] != CORRECT_LABELS[i]:
        print(f"❌ Index {i}: APP has '{APP_LABELS[i]}' but TRAINING has '{CORRECT_LABELS[i]}'")
        mismatches.append(i)

if not mismatches:
    print("✅ All labels match!")
else:
    print(f"\n⚠️ Found {len(mismatches)} mismatches!")
    print("\nThis explains why 'dog' is being predicted as 'rain'!")
    
    # Find what dog should be
    dog_index_in_app = APP_LABELS.index('dog')
    dog_index_in_training = CORRECT_LABELS.index('dog')
    
    print(f"\n🐕 DOG analysis:")
    print(f"   - In APP: index {dog_index_in_app}")
    print(f"   - In TRAINING: index {dog_index_in_training}")
    print(f"   - Model predicts index {dog_index_in_training}, APP maps to '{APP_LABELS[dog_index_in_training]}'")
