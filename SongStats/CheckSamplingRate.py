"""
Note you have to switch interpreters to use this script. Need the one used for Chipper, with python3:
SongAnlaysisGUI_Env_3.6
"""

import numpy as np
# import bottleneck as bn
import glob
import os
import soundfile as sf
import shutil
#import matplotlib.pyplot as plt

# directory = 'C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/FinalDataCompilation/'
# directory = "G:\Ivybouts"
directory = "C:/Users/abiga\Box Sync\Creanza " \
            "Lab\Abigail_Nyssa\BSCI_1512L_compiledFiles\shanbhmv_parsed_bouts_6_compiled"

for dirpath, dirnames, filenames in os.walk(directory):
    new_path = dirpath + '_non44100Hz'
    for filename in [f for f in filenames if f.endswith(".wav")]:
        song1, sampling_rate = sf.read(os.path.join(dirpath, filename), always_2d=True)
        if sampling_rate != 44100:
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            # os.rename(os.path.join(dirpath, filename), os.path.join(new_location, filename))
            shutil.move(os.path.join(dirpath, filename), os.path.join(new_path, filename))
            print(filename, sampling_rate)