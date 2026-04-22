from vieneu import Vieneu
import sounddevice as sd
import scipy.io.wavfile as wav

class TextToSpeech:
    def __init__(self, voice_id=None):
        self.tts = Vieneu()

        # load voice nếu có
        if voice_id is not None:
            self.voice = self.tts.get_preset_voice(voice_id)
        else:
            self.voice = None

    def synthesize(self, text, output_file="output.wav"):
        # generate audio
        if self.voice:
            audio = self.tts.infer(text=text, voice=self.voice)
        else:
            audio = self.tts.infer(text=text)

        # save file
        self.tts.save(audio, output_file)
        return output_file

    def play(self, file_path):
        sr, data = wav.read(file_path)
        sd.play(data, sr)
        sd.wait()

    def text_to_speech(self, text):
        file_path = self.synthesize(text)
        self.play(file_path)