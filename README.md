# 🎧 S-Hear Intelligent Dashboard

AI-Powered Environmental Sound Recognition System using ConvNeXt-Tiny and ESC-50 Dataset.

## 🌟 Features

### Core Features
- **📁 File Analysis**: Upload audio files (.wav, .mp3) and analyze them with Mel-Spectrogram visualization
- **🎙️ Live Monitor**: Real-time audio monitoring with dynamic waveform display
- **📊 Smart Dashboard**: Statistics and quick actions
- **📜 History Log**: Complete detection history with timestamps
- **⚙️ Settings**: Customizable confidence threshold and notification preferences

### Advanced Features
- **🔔 Smart Notifications**: Snackbar notifications for detections
- **🚨 Visual Alerts**: Screen flash for alert sounds (siren, alarm, etc.)
- **🎯 Confidence Filtering**: Only show predictions above custom threshold
- **🧵 Multi-threaded**: Non-blocking UI with background processing
- **🎨 Modern UI**: Dark mode with Electric Blue and Slate Grey theme

## 🛠️ Technology Stack

- **UI Framework**: Flet (Python)
- **AI Engine**: ONNX Runtime
- **Audio Processing**: Librosa, SoundDevice
- **Model**: ConvNeXt-Tiny (ESC-50 Dataset - 50 environmental sounds)
- **Visualization**: Matplotlib, Pillow

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Model Setup (Optional)

Place your trained `model.onnx` file in the `models/` directory:

```
app/
├── models/
│   └── model.onnx  # Your ConvNeXt-Tiny ONNX model
├── src/
├── main.py
└── requirements.txt
```

**Note**: If no model is found, the app will run in **Mock Mode** for testing the UI.

### 3. Run the Application

```bash
python main.py
```

## 🎯 Usage

### File Analysis
1. Click **"File Analysis"** in the sidebar
2. Click **"Select Audio File"** and choose a .wav or .mp3 file
3. Click **"Analyze"** to see the Mel-Spectrogram and prediction results

### Live Monitor
1. Click **"Live Monitor"** in the sidebar
2. Click **"Start Monitoring"** to begin real-time audio capture
3. The app will continuously analyze audio and show predictions
4. Alert sounds (siren, alarm) will trigger visual alerts if enabled

### Settings
- **Confidence Threshold**: Adjust the minimum confidence level (0-100%)
- **Enable Notifications**: Toggle snackbar notifications
- **Visual Alerts**: Toggle screen flash for alert sounds

## 🎨 UI Design

The app features a modern **Dark Mode** design with:
- **Primary Color**: Electric Blue (#00D9FF)
- **Background**: Dark Slate (#0F172A)
- **Surface**: Slate Grey (#1E293B)
- **Accent Colors**: Green (#10B981), Orange (#F59E0B), Red (#EF4444)

## 📊 ESC-50 Sound Classes

The model recognizes 50 environmental sounds across 5 categories:

1. **Animals**: dog, cat, pig, cow, frog, etc.
2. **Natural**: rain, wind, thunderstorm, sea waves, etc.
3. **Human**: crying baby, laughing, coughing, sneezing, etc.
4. **Interior/Domestic**: door knock, clock alarm, vacuum cleaner, etc.
5. **Exterior/Urban**: siren, car horn, helicopter, train, etc.

## 🔧 Project Structure

```
app/
├── src/
│   ├── ai/
│   │   ├── model_handler.py      # ONNX model inference
│   │   └── audio_processor.py    # Audio loading & preprocessing
│   ├── ui/
│   │   ├── layout.py             # Main layout & navigation
│   │   ├── dashboard.py          # Dashboard view
│   │   ├── file_analysis.py      # File analysis view
│   │   ├── live_monitor.py       # Live monitoring view
│   │   ├── history.py            # History view
│   │   └── settings.py           # Settings view
│   └── utils/
│       └── state.py              # Application state management
├── models/
│   └── model.onnx               # (Optional) Your trained model
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Performance

- **Real-time Processing**: ~2 second analysis intervals
- **Non-blocking UI**: Multi-threaded architecture
- **CPU Optimized**: ONNX Runtime with CPU execution provider
- **Memory Efficient**: Streaming audio processing

## ⚠️ Requirements

- **Python**: 3.8+
- **Microphone**: Required for Live Monitor feature
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB+ recommended
- **CPU**: Multi-core recommended for real-time processing

## 🐛 Troubleshooting

### Microphone Not Working
- Check microphone permissions in your OS settings
- Ensure no other application is using the microphone
- Try restarting the application

### Model Not Loading
- Verify `models/model.onnx` exists and is a valid ONNX file
- Check ONNX Runtime installation: `pip install onnxruntime`
- The app will automatically fall back to Mock Mode if model is missing

### Audio File Not Loading
- Ensure the file is a valid audio format (.wav, .mp3, .ogg, .flac)
- Check file is not corrupted
- Try converting to .wav format

## 📝 License

This project is for educational and demonstration purposes.

## 🙏 Credits

- **Model**: ConvNeXt-Tiny architecture
- **Dataset**: ESC-50 Environmental Sound Classification
- **UI Framework**: Flet by Google
- **Audio Processing**: Librosa, SoundDevice

---

**Built with ❤️ using Python and Flet**
