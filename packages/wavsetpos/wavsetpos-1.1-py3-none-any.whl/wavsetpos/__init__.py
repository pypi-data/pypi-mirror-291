from pydub import AudioSegment
from typing import Any
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from os import remove
from pygame.mixer_music import load, play, stop, unload

loaded_file : str | None = None
tmp_file : str

def __init_tmp() -> None:
    global tmp_file
    temp : _TemporaryFileWrapper = NamedTemporaryFile(delete=False)
    tmp_file = temp.name
    temp.close()
__init_tmp()

def load_wav(filename : str, namehint : str | None = "") -> None:
    global loaded_file 
    load(filename, namehint)
    loaded_file = filename

def set_wav_pos(pos : int, dir : str | None = None) -> None:
    """
    pos is in ms
    """
    global loaded_file, tmp_file
    if loaded_file is None and dir is None:
        raise Exception("No files are loaded/no dir in args.")
    
    audio : Any = AudioSegment.from_wav(loaded_file if loaded_file is not None else dir)
    trimmed : Any = audio[pos * 1000:]

    stop()
    unload()
    trimmed.export(tmp_file, format="wav")


    load(tmp_file)
    play()

    del audio, trimmed

def __clean_tmp(new_tmp : bool = True) -> None:
    """
    Removes all tmp files.
    (unloads mixer.music)
    """
    global tmp_file
    stop()
    unload()
    try:
        remove(tmp_file)
    except FileNotFoundError: ...
    if new_tmp:
        __init_tmp()

import atexit
# clean tmp on exit
atexit.register(__clean_tmp, (False))