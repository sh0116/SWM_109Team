import pygame

def play_mp3(file_name):
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/robot109/voice_processing/voice_file/"+file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print("play over...")
    return


if __name__ == "__main__":
    play_mp3("송가인-가인이어라.mp3")
