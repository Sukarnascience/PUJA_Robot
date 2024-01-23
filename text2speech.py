from gtts import gTTS
import pygame

def text_to_speech(text, language='en'):

    print(f"Input is : {text}")

    tts = gTTS(text=text, lang=language)
    audio_path = 'output.mp3'
    tts.save(audio_path)

    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio_path)
    sound.play()
    pygame.time.wait((int(sound.get_length()) * 1000)+580)