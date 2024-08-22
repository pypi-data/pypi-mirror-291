import pygame
from __init__ import load_wav, set_wav_pos, __clean_tmp

pygame.mixer.pre_init(44100, 32, 2, 4096)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.034)
load_wav(r"D:\coding\Python_Programs\NoBrowserYT\temp\tempaudio0.wav")
pygame.mixer.music.play()
set_wav_pos(50)

i : int = 0
while pygame.mixer.music.get_busy():
    i += 1
    pygame.time.Clock().tick(60)

    if i == 100:
        set_wav_pos(10_000)
    elif i == 500:
        break

__clean_tmp()