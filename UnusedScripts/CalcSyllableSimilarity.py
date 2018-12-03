import os
import glob
import time
import numpy as np
import csv
import pickle
from scipy import signal

import utils as utils

import time
start_time = time.time()
import gc

def load_bout_data(f_name):
    """
    Load sonogram and syllable marks (onsets and offsets).
    """
    try:
        song_data = utils.load_gz_p(f_name)
    except:
        song_data = utils.load_old(f_name)
    onsets = np.asarray(song_data[1]['Onsets'], dtype='int32')
    offsets = np.asarray(song_data[1]['Offsets'], dtype='int32')
    threshold_sonogram = np.asarray(song_data[2]['Sonogram'], dtype='bool')
    ms_per_pixel = np.asarray(song_data[3]['timeAxisConversion'])
    hz_per_pixel = np.asarray(song_data[3]['freqAxisConversion'])
    return onsets, offsets, threshold_sonogram, ms_per_pixel, hz_per_pixel


def calc_max_correlation(syll_sonograms):
    sonogram_self_correlation = np.zeros(len(syll_sonograms))

    for i in range(len(syll_sonograms)):
        sonogram_self_correlation[i] = (syll_sonograms[i] * syll_sonograms[i]).sum()

    return sonogram_self_correlation


def calc_corr(syll_1, syll_2, shift_factor, min_length, max_overlap):
    syllable_correlation = np.zeros(shift_factor + 1)
    scale_factor = 100. / max_overlap
    # flatten matrix to speed up computations
    for m in range(shift_factor + 1):
        start = 0 + m
        # flatten matrix to speed up computations
        syll_2_new = syll_2[:, start:start + min_length]
        syllable_correlation[m] = (syll_1*syll_2_new).sum()
    return max(scale_factor * syllable_correlation)


# 1.load data
# 2. get center onset/offset and associated syllable
# 3. clear onsets, offsets, and full sonogram

directory = "C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/FinalDataCompilation"

names = []
sylls = []
syll_durs = []
list_names = (glob.glob(directory + '/*/*/*/*.gzip') + glob.glob(directory + '/*/**/*.gzip'))
# list_names = list_names[1:200]
# list_names = glob.glob(directory + '/*/**/*.gzip')
# list_names = list_names[0:2]

for f in list_names:
    names.append(os.path.basename(f).split('_', 1)[-1])
    onset_list, offset_list, song, _, _ = load_bout_data(f)
    mid = int((len(onset_list) - 1)/2)
    mid_onset = onset_list[mid] #this rounds down since not float
    mid_offset = offset_list[mid]
    sylls.append(song[:, mid_onset:mid_offset])
    syll_durs.append(mid_offset - mid_onset)
    del song, mid, mid_onset, mid_offset, onset_list, offset_list
gc.collect()
print('loaded everything')
# get pairwise similarity matrix of all representative syllables
print('number of files: ', len(names))
n_sylls = len(sylls)
print('number of sylls: ', n_sylls)
self_correlation = calc_max_correlation(sylls)
syllable_correlation = np.zeros((n_sylls, n_sylls))

# with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/AllSylls_Names'
#           '.txt', 'wb') as f:
#     for item in names:
#         f.write("%s\n" % item)
#
# with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/Testing_Sylls'
#           '.txt', 'a') as f:
#     for i in range(len(sylls)):
#         np.savetxt(f, sylls[i], delimiter=', ', newline='\n', fmt='%s')
#     # csvwriter = csv.writer(f)
#     # csvwriter.writerows(sylls)

names_sylls = zip(names, sylls)
print('number of name sylls pairs: ', len(list(zip(names, sylls))))
f = open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables'
         '/1Dcorr/AllSylls_Sylls_1Dcorr_desktop.pkl', 'wb')
pickle.dump(names_sylls, f)
f.close()

print('saved sylls and names')
end_time = time.time()
print(end_time-start_time)

new_start = time.time()
for j in range(n_sylls):
    print(j)
    print(time.time() - new_start)
    # do not want to fill the second half of the diagonal matrix
    for k in range(j, n_sylls):

        max_overlap = max(self_correlation[j], self_correlation[k])
        scale_factor = 100. / max_overlap
        #1D overlap sliding similarity
        shift_factor = abs(syll_durs[j] - syll_durs[k])
        if syll_durs[j] < syll_durs[k]:  #j is shorter
            min_length = syll_durs[j]
            syll_corr = calc_corr(sylls[j], sylls[k], shift_factor, min_length, max_overlap)

        # will be if k is shorter than j or they are equal
        else:
            min_length = syll_durs[k]
            syll_corr = calc_corr(sylls[k], sylls[j], shift_factor, min_length, max_overlap)

        #2D cross-correlation
        # print('starting corr')
        # max_cross_corr = np.max(signal.correlate2d(sylls[j].astype(int), sylls[k].astype(int)))
        # print('max chosen')
        # syll_corr = scale_factor*max_cross_corr
        # print('scale factor applied')

        # fill both upper and lower diagonal of symmetric matrix
        syllable_correlation[j, k] = syll_corr
        syllable_correlation[k, j] = syll_corr
        del max_overlap, scale_factor, syll_corr
    # sonogram_correlation_binary = np.zeros(sonogram_correlation.shape)
    # sonogram_correlation_binary[sonogram_correlation > corr_thresh] = 1
gc.collect()

syll_corr_matrix = np.matrix(syllable_correlation)
with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables'
          '/1Dcorr/AllSylls_SimMatrix_1Dcorr_desktop'
          '.txt', 'wb') as f:
    for line in syll_corr_matrix:
        np.savetxt(f, line, fmt='%.2f')
