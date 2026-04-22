import streamlit as st
from stt import STT
from tts import TextToSpeech

# ===== Cấu hình trang =====
st.set_page_config(page_title="STT & TTS Vietnamese", layout="centered", page_icon="🎤")

# ===== Khởi tạo Models =====
@st.cache_resource
def load_models():
    return STT(model_size="small"), TextToSpeech()

stt_model, tts_model = load_models()

# ===== Giao diện chính =====
st.title("🎤 STT & 🔊 TTS Vietnamese")
st.markdown("---")

# ===== PHẦN 1: SPEECH TO TEXT (STT) =====
st.header("1. 🎤 Chuyển giọng nói thành văn bản")

# Sử dụng widget audio_input chính chủ của Streamlit
audio_file = st.audio_input("Nhấn vào micro để ghi âm giọng nói của bạn")

if audio_file:
    with st.spinner("🧠 Đang chuyển đổi giọng nói..."):
        # Xử lý file audio đã ghi
        transcribed_text = stt_model.transcribe_uploaded_file(audio_file)
        
        if transcribed_text:
            st.success("✅ Đã nhận diện thành công!")
            st.write("**Kết quả:**")
            st.info(transcribed_text)
            
            # Gợi ý: Có thể dùng kết quả này để đưa vào phần TTS bên dưới
            if st.button("📋 Copy kết quả vào phần TTS"):
                st.session_state.tts_input = transcribed_text
        else:
            st.warning("Không nhận diện được nội dung, hãy thử lại nhé!")

st.markdown("---")

# ===== PHẦN 2: TEXT TO SPEECH (TTS) =====
st.header("2. 🔊 Chuyển văn bản thành giọng nói")

# Khởi tạo state cho input text nếu chưa có
if "tts_input" not in st.session_state:
    st.session_state.tts_input = ""

input_text = st.text_area("Nhập nội dung văn bản cần chuyển đổi:", 
                          value=st.session_state.tts_input,
                          placeholder="Ví dụ: Chào bạn, tôi là trợ lý AI.")

if st.button("🔈 Tạo và Phát âm thanh"):
    if input_text.strip():
        with st.spinner("🔊 Đang tổng hợp giọng nói..."):
            try:
                # Tổng hợp âm thanh
                output_path = tts_model.synthesize(input_text)
                # Phát âm thanh trong browser
                st.audio(output_path, format="audio/wav", autoplay=True)
                st.success("Đã tạo xong âm thanh!")
            except Exception as e:
                st.error(f"Lỗi khi tạo âm thanh: {e}")
    else:
        st.warning("Vui lòng nhập văn bản trước khi nhấn nút!")

# Footer
st.markdown("---")
st.caption("Ứng dụng sử dụng Faster-Whisper cho STT và VieNeu cho TTS.")