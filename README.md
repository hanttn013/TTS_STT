# 🇻🇳 Vietnamese STT & TTS (Full Offline)

Đây là hệ thống Speech-to-Text và Text-to-Speech chạy **hoàn toàn Offline** trên máy tính của bạn, đảm bảo tính riêng tư và tốc độ xử lý nhanh.

## 🚀 Tính năng
- **Speech-to-Text (STT)**: Sử dụng `Faster-Whisper` (mô hình Whisper được tối ưu hóa) để nhận diện giọng nói tiếng Việt cực nhanh và chính xác.
- **Text-to-Speech (TTS)**: Sử dụng `VieNeu-TTS` mô hình Turbo dành riêng cho tiếng Việt, giọng đọc tự nhiên, xử lý cực nhanh trên CPU.
- **Offline 100%**: Sau khi tải model lần đầu tiên, không cần kết nối Internet để chạy.

## 🛠️ Cài đặt

1. **Cài đặt Python**: Yêu cầu Python 3.8 - 3.11.
2. **Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Cài đặt ffmpeg** (Bắt buộc để xử lý audio):
   - **Windows**: Tải tại [ffmpeg.org](https://ffmpeg.org/download.html) và thêm vào PATH.
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## 💻 Cách sử dụng

### 1. Chạy demo với giao diện (Streamlit)
```bash
streamlit run stream.py
```

### 2. Tích hợp vào code của bạn
Bạn có thể dễ dàng sử dụng lại các class trong hệ thống:

```python
from stt import STT
from tts import TextToSpeech

# Khởi tạo (Model sẽ tự tải về trong lần đầu tiên)
stt = STT(model_size="small")
tts = TextToSpeech()

# STT: Chuyển file audio sang văn bản
text = stt.transcribe_file("audio_cua_ban.wav")
print(f"Nhận diện: {text}")

# TTS: Chuyển văn bản sang giọng nói
output_wav = tts.synthesize("Xin chào bạn nhé!")
print(f"File audio đã lưu tại: {output_wav}")
```

## 📂 Cấu trúc thư mục
- `stt.py`: Class xử lý nhận diện giọng nói.
- `tts.py`: Class xử lý tổng hợp tiếng nói.
- `stream.py`: Ứng dụng giao diện Streamlit.
- `requirements.txt`: Danh sách các thư viện cần thiết.

## ⚠️ Lưu ý về Model
- Lần đầu chạy, hệ thống sẽ tự động tải model từ HuggingFace (khoảng vài trăm MB). 
- Các lần chạy sau sẽ lấy model từ cache nên không cần Internet.
- Nếu muốn chạy trên GPU, hãy cài đặt thêm `onnxruntime-gpu`.
