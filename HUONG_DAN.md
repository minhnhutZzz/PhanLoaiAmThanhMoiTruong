# 🎧 S-Hear Intelligent Dashboard - Hướng Dẫn Sử Dụng

## ✅ Hoàn Thành!

Ứng dụng **S-Hear Intelligent Dashboard** đã được xây dựng thành công với đầy đủ các tính năng:

### 🌟 Các Tính Năng Chính

#### 1. **📁 File Analysis (Phân Tích File)**
- Upload file âm thanh (.wav, .mp3, .ogg, .flac)
- Hiển thị Mel-Spectrogram đầy màu sắc
- Dự đoán loại âm thanh với độ tự tin (Confidence Score)
- Hiển thị Top-5 predictions với biểu đồ thanh ngang
- Icon đại diện cho mỗi loại âm thanh

#### 2. **🎙️ Live Monitor (Giám Sát Trực Tiếp)**
- Bắt âm thanh từ microphone real-time
- Hiển thị waveform động (sóng âm chạy liên tục)
- Dự đoán âm thanh mỗi 2 giây
- Cập nhật kết quả tự động trên giao diện

#### 3. **🔔 Smart Notification System**
- Thông báo Snackbar khi phát hiện âm thanh
- **Visual Alert**: Nháy đèn màn hình đỏ khi phát hiện âm thanh nguy hiểm (siren, alarm, glass breaking, etc.)
- Có thể bật/tắt thông báo trong Settings

#### 4. **📜 Sound History Log**
- Lưu lại tất cả âm thanh đã nhận diện
- Hiển thị: Thời gian, Loại âm thanh, Độ tự tin, Nguồn (File/Live)
- Có thể xóa lịch sử
- Color-coded confidence scores (xanh lá: cao, vàng: trung bình, đỏ: thấp)

#### 5. **⚙️ Settings (Cài Đặt)**
- **Confidence Threshold**: Chỉ hiển thị dự đoán trên ngưỡng tự tin nhất định (0-100%)
- **Enable Notifications**: Bật/tắt thông báo
- **Visual Alerts**: Bật/tắt hiệu ứng nháy màn hình cho âm thanh nguy hiểm
- Hiển thị thông tin model

#### 6. **📊 Dashboard**
- Thống kê tổng quan: Tổng số detections, Âm thanh phổ biến nhất, Độ tự tin trung bình
- Quick Actions để chuyển nhanh sang các chức năng
- Hiển thị trạng thái model (Loaded/Mock Mode)

### 🎨 Giao Diện

- **Dark Mode** với màu chủ đạo **Electric Blue (#00D9FF)** và **Slate Grey**
- Sidebar điều hướng với icons đẹp mắt
- Status bar hiển thị: Mic status, CPU usage, Model version
- Animations mượt mà, responsive

### 🤖 AI Model

- **Model**: ConvNeXt-Tiny
- **Dataset**: ESC-50 (50 loại âm thanh môi trường)
- **Input**: Mel-Spectrogram 128x431 (grayscale)
- **Output**: 50 classes với confidence scores

### 📝 Danh Sách 50 Loại Âm Thanh

**Động vật (Animals)**:
- dog, cat, pig, cow, frog, rooster, hen, insects, sheep, crow

**Tự nhiên (Natural)**:
- rain, sea_waves, crackling_fire, crickets, chirping_birds, water_drops, wind, pouring_water, toilet_flush, thunderstorm

**Con người (Human)**:
- crying_baby, sneezing, clapping, breathing, coughing, footsteps, laughing, brushing_teeth, snoring, drinking_sipping

**Nội thất/Gia đình (Interior/Domestic)**:
- door_wood_knock, mouse_click, keyboard_typing, door_wood_creaks, can_opening, washing_machine, vacuum_cleaner, clock_alarm, clock_tick, glass_breaking

**Ngoại thất/Đô thị (Exterior/Urban)**:
- helicopter, chainsaw, siren, car_horn, engine, train, church_bells, airplane, fireworks, hand_saw

### 🚨 Alert Sounds (Âm Thanh Cảnh Báo)

Các âm thanh sau sẽ kích hoạt visual alert (nháy màn hình đỏ):
- siren
- car_horn
- glass_breaking
- clock_alarm
- crying_baby
- fireworks

---

## 🚀 Cách Chạy Ứng Dụng

### Lần Đầu Tiên

1. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

2. **Chuyển đổi model** (nếu có file .pth):
```bash
$env:PYTHONIOENCODING="utf-8"; python convert_model.py
```

3. **Chạy ứng dụng**:
```bash
python main.py
```

### Lần Sau

Chỉ cần chạy:
```bash
python main.py
```

---

## 📖 Hướng Dẫn Sử Dụng Chi Tiết

### 1. File Analysis

1. Click vào tab **"File Analysis"** trên sidebar
2. Click nút **"📁 Select Audio File"**
3. Chọn file âm thanh (.wav hoặc .mp3)
4. Click **"🔍 Analyze"**
5. Xem kết quả:
   - Mel-Spectrogram hiển thị ở giữa
   - Kết quả chính với icon và confidence score
   - Top-5 predictions với biểu đồ

### 2. Live Monitor

1. Click vào tab **"Live Monitor"**
2. Click **"🎙️ Start Monitoring"**
3. Cho phép quyền truy cập microphone (nếu được hỏi)
4. Nói hoặc phát âm thanh gần microphone
5. Xem:
   - Waveform cập nhật real-time
   - Kết quả dự đoán xuất hiện khi có âm thanh
   - Thông báo Snackbar
6. Click **"⏹️ Stop"** để dừng

### 3. History

1. Click vào tab **"History"**
2. Xem danh sách tất cả âm thanh đã nhận diện
3. Click **🔄 Refresh** để cập nhật
4. Click **🗑️ Clear** để xóa lịch sử

### 4. Settings

1. Click vào tab **"Settings"**
2. Điều chỉnh:
   - **Confidence Threshold**: Kéo slider để thay đổi ngưỡng
   - **Notifications**: Bật/tắt thông báo
   - **Visual Alerts**: Bật/tắt hiệu ứng nháy màn hình
3. Xem thông tin model ở dưới

---

## 🎯 Tips & Tricks

### Để Có Kết Quả Tốt Nhất:

1. **File Analysis**:
   - Sử dụng file âm thanh rõ ràng, không nhiễu
   - File nên có độ dài 1-5 giây
   - Format .wav cho chất lượng tốt nhất

2. **Live Monitor**:
   - Đảm bảo microphone hoạt động tốt
   - Môi trường yên tĩnh cho kết quả chính xác hơn
   - Nói/phát âm thanh rõ ràng
   - Điều chỉnh Confidence Threshold nếu có quá nhiều false positives

3. **Performance**:
   - Đóng các ứng dụng khác để tăng hiệu suất
   - Live Monitor sử dụng nhiều CPU - bình thường
   - Nếu lag, tăng interval trong code (hiện tại là 2 giây)

---

## ⚠️ Troubleshooting

### Microphone Không Hoạt Động
- Kiểm tra quyền microphone trong Windows Settings
- Đảm bảo không có app nào khác đang sử dụng mic
- Restart ứng dụng

### Model Không Load
- Kiểm tra file `models/model.onnx` có tồn tại không
- Chạy lại `convert_model.py` nếu cần
- Ứng dụng sẽ tự động chuyển sang Mock Mode nếu không tìm thấy model

### Ứng dụng Chạy Chậm
- Đóng Live Monitor khi không sử dụng
- Giảm số lượng history entries
- Kiểm tra CPU usage

---

## 🔧 Cấu Trúc Dự Án

```
app/
├── models/
│   ├── best_convnext_tiny.pth    # PyTorch model (original)
│   └── model.onnx                # ONNX model (converted)
├── src/
│   ├── ai/
│   │   ├── model_handler.py      # ONNX inference
│   │   └── audio_processor.py    # Audio processing
│   ├── ui/
│   │   ├── layout.py             # Main layout
│   │   ├── dashboard.py          # Dashboard view
│   │   ├── file_analysis.py      # File analysis view
│   │   ├── live_monitor.py       # Live monitor view
│   │   ├── history.py            # History view
│   │   └── settings.py           # Settings view
│   └── utils/
│       └── state.py              # App state management
├── main.py                       # Entry point
├── convert_model.py              # PyTorch to ONNX converter
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## 📚 Dependencies

- **flet**: UI framework
- **onnxruntime**: Model inference
- **librosa**: Audio processing
- **sounddevice**: Real-time audio capture
- **numpy, matplotlib, pandas**: Data processing & visualization
- **torch, torchvision**: Model conversion (chỉ cần khi convert)
- **onnx, onnxscript**: ONNX support

---

## 🎓 Kỹ Thuật Sử Dụng

### 1. **Multi-threading**
- Live Monitor chạy trong thread riêng để không block UI
- Audio callback xử lý trong background

### 2. **State Management**
- Singleton pattern cho global state
- Thread-safe với locks

### 3. **Audio Processing**
- Mel-Spectrogram: 128 mel bands, 431 time frames
- Sample rate: 22050 Hz
- Window: 2048, Hop: 512

### 4. **Model Inference**
- Input shape: (1, 1, 128, 431)
- Output: (1, 50) - softmax probabilities
- Threshold filtering cho notifications

---

## 🎉 Kết Luận

Ứng dụng **S-Hear Intelligent Dashboard** đã được xây dựng hoàn chỉnh với:

✅ Giao diện hiện đại, đẹp mắt (Dark Mode + Electric Blue)
✅ 5 chức năng chính đầy đủ
✅ AI model ConvNeXt-Tiny với 50 classes
✅ Real-time monitoring với threading
✅ Smart notifications + Visual alerts
✅ History logging
✅ Settings tùy chỉnh
✅ Clean code architecture

**Chúc bạn sử dụng vui vẻ! 🎧🔊**
