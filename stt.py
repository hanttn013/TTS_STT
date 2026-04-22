import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
from faster_whisper import WhisperModel


class STT:
    def __init__(self, model_size="small", compute_type="int8"):
        self.model = WhisperModel(model_size, compute_type=compute_type)
        self.sample_rate = 16000

    # ===== RECORD =====
    def record(self, duration=5):
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1
        )
        sd.wait()
        return audio.flatten()

    # ===== PREPROCESS =====
    def preprocess_audio(self, audio):
        max_val = np.max(np.abs(audio)) + 1e-6
        audio = audio / max_val
        audio = np.clip(audio, -1, 1)
        return audio

    # ===== SAVE TEMP FILE =====
    def save_temp(self, audio):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_int16 = (audio * 32767).astype("int16")
        wav.write(tmp.name, self.sample_rate, audio_int16)
        return tmp.name

    # ===== TRANSCRIBE FROM FILE =====
    def transcribe_file(self, audio_path):
        segments, _ = self.model.transcribe(
            audio_path,
            language="vi",
            task="transcribe",
            beam_size=5,
            vad_filter=True,
            temperature=0.0,
            condition_on_previous_text=False
        )
        return " ".join([seg.text.strip() for seg in segments])

    # ===== TRANSCRIBE FROM ARRAY (CHO STREAM) =====
    def transcribe_array(self, audio):
        audio = self.preprocess_audio(audio)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_int16 = (audio * 32767).astype("int16")
        wav.write(tmp.name, self.sample_rate, audio_int16)

        text = self.transcribe_file(tmp.name)

        os.remove(tmp.name)
        return text

    # ===== TRANSCRIBE FROM STREAMLIT UPLOADED FILE =====
    def transcribe_uploaded_file(self, uploaded_file):
        """Xử lý file từ st.audio_input hoặc st.file_uploader"""
        if uploaded_file is None:
            return ""
            
        # Lưu vào file tạm vì whisper model ổn định hơn với file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
            
        try:
            text = self.transcribe_file(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
        return text

    # ===== FULL PIPELINE (MIC → TEXT) =====
    def speech_to_text(self, duration=5):
        print("🎤 Recording...")
        audio = self.record(duration)

        print("🔊 Max volume:", np.max(audio))

        audio = self.preprocess_audio(audio)

        print("💾 Saving...")
        path = self.save_temp(audio)

        print("🧠 Transcribing...")
        text = self.transcribe_file(path)

        print("📝 Done:", text)

        os.remove(path)
        return text