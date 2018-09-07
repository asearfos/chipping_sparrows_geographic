"""
Note you have to switch interpreters to use this script. Need the one used for Chipper, with python3:
SongAnlaysisGUI_Env_3.6
"""

import numpy as np
# import bottleneck as bn
import glob
import os
import soundfile as sf
#import matplotlib.pyplot as plt

# directory = 'C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/FinalDataCompilation/'
directory = "G:\Ivybouts"

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in [f for f in filenames if f.endswith(".wav")]:
        song1, sampling_rate = sf.read(os.path.join(dirpath, filename), always_2d=True)
        if sampling_rate != 44100:
            print(filename, sampling_rate)