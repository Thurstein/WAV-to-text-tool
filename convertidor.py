import os, shutil
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from PySide6.QtCore import QThread, Signal

class AudioThread(QThread):
    signal = Signal(str)

    def __init__(self):
        super().__init__()

    def process_audio(self, file_name):
        os.makedirs("chunked", exist_ok=True)
        with open("the_audio.txt", "w+") as txtf:
            myaudio = AudioSegment.from_wav(file_name)
            CHUNK_LENGTH_MS = 60 * 1000
            chunks = make_chunks(myaudio, CHUNK_LENGTH_MS)
            chunk_names = [f'./chunked/{file_name.replace(":", "").replace("/", "")}_{i}.wav' for i in range(len(chunks))]
            num_chunk = 0
            for chunkname, chunk in zip(chunk_names, chunks):
                print('I am exporting', chunkname)
                chunk.export(chunkname, format='wav')
                file = chunkname
                r = sr.Recognizer()
                with sr.AudioFile(file) as source:
                    audio_listened = r.listen(source)
                try:
                    LANGUAGE = 'es-ES'
                    rec = r.recognize_google(audio_listened, language=LANGUAGE)
                    txtf.write(f'Minuto {num_chunk}. \n {rec}. \n')
                    self.signal.emit(f'Minuto {num_chunk}. \n {rec}. \n')
                    print("writing text")

                except sr.UnknownValueError:
                    txtf.write(f'Minuto {num_chunk}. \n (No se reconoce el audio en este tramo). \n')
                    print("I dont recognize your audio")
                except sr.RequestError as e:
                    print("could not get the result. Check your internet")
                num_chunk += 1
            print("finished")
            shutil.rmtree("chunked")