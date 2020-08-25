import pygame

def play_mp3():
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/my_dir/NLP/voice_file/TTS.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print("play over...")
    return


if __name__ == "__main__":
    play_mp3()
