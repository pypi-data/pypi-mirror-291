---
This is a module to make setting the position of a wav file in pygame.mixer.music possible

---

# Functions
## load_wav
*Loads wav file into pygame mixer*

`def load_wav(filename : str, namehint : str | None = "") -> None:...`

**Example**
```
import wavsetpos as wsp
import pygame

# use in place of pygame.mixer.music.load()
wsp.load_wav(...)
...
pygame.mixer.music.play()
```

## set_wav_pos
*Sets position of wav file playing in pygame mixer*

`def set_wav_pos(pos : int, dir : str | None = None) -> None:...`

**Example**
```
import wavsetpos as wsp
import pygame

# use in place of pygame.mixer.music.load()
wsp.load_wav(...)
...
pygame.mixer.music.play()

# in seconds
wsp.set_wav_pos(50)
```
