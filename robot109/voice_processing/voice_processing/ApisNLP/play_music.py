import pygame

def play_mp3(file_name):
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/NLP/voice_file/"+file_name+".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print("play over...")
    return


if __name__ == "__main__":
    pass
