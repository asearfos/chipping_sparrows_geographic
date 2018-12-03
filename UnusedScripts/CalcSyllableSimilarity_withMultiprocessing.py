import os
import glob
import time
import numpy as np
import csv
import pickle
from scipy import signal
import utils as utils
import gc
import time
import itertools
from multiprocessing import Pool, sharedctypes



"""
Define functions
"""

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

def calc_2Dcrosscorr(indices):
    col, row = indices
    print('here')
    print(type(shared_array))
    syllable_correlation = np.ctypeslib.as_array(shared_array)
    print('here2')

    if col >= row:
        max_overlap = max(self_correlation[j], self_correlation[k])
        scale_factor = 100. / max_overlap

        # 2D cross-correlation
        max_cross_corr = np.max(signal.correlate2d(sylls[col].astype(int), sylls[row].astype(int)))
        syll_corr = scale_factor * max_cross_corr

        # fill both upper and lower diagonal of symmetric matrix
        syllable_correlation[col, row] = syll_corr
        syllable_correlation[row, col] = syll_corr

# # shared_array = None
# def _init(share):
#     print('initializing')
#     global shared_array
#     shared_array = share
#     print('done initializing'

# shared_array = None
#
# def _init(share):
#     global shared_array
#     shared_array = share

if __name__ == '__main__':
    """
    1. load data
    2. get center onset/offset and associated syllable
    3. clear onsets, offsets, and full sexonogram
    4. save the syllables with their names
    """

    print('start program')
    start_time = time.time()

    directory = "C:/Users/abiga/Box Sync/Abigail_Nicole/ChippiesProject/FinalDataCompilation"

    names = []
    sylls = []
    syll_durs = []
    # list_names = (glob.glob(directory + '/*/*/*/*.gzip') + glob.glob(directory + '/*/**/*.gzip'))
    # list_names = list_names[1:200]
    list_names = glob.glob(directory + '/*/**/*.gzip')
    list_names = list_names[0:2]

    for f in list_names:
        names.append(os.path.basename(f).split('_', 1)[-1])
        onset_list, offset_list, song, _, _ = load_bout_data(f)
        mid = int((len(onset_list) - 1) / 2)
        mid_onset = onset_list[mid]  # this rounds down since not float
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

    names_sylls = zip(names, sylls)
    print('number of name sylls pairs: ', len(list(zip(names, sylls))))
    # f = open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables'
    #          '/AllSylls_Sylls_2Dcorr_smallTest.pkl', 'wb')
    # pickle.dump(names_sylls, f)
    # f.close()

    print('saved sylls and names')
    end_time = time.time()
    print(end_time - start_time)

    """
    start correlation portion of the code
    """
    self_correlation = calc_max_correlation(sylls)
    # make array that will be shared by the multiprocessing to put results of each pool back into
    result = np.ctypeslib.as_ctypes(np.zeros((n_sylls, n_sylls)))
    share = sharedctypes.RawArray(result._type_, result)
    matrix_idxs = [(j, k) for j, k in itertools.product(range(0, n_sylls), range(0, n_sylls))]

    p = Pool(processes=2, initializer=_init(share))
    res = p.map(calc_2Dcrosscorr, matrix_idxs)
    result = np.ctypeslib.as_array(shared_array)

    syll_corr_matrix = np.matrix(result)
    print(syll_corr_matrix)
    # with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables'
    #           '/AllSylls_SimMatrix_2Dcorr_smallTest.txt', 'wb') as f:
    #     for line in syll_corr_matrix:
    #         np.savetxt(f, line, fmt='%.2f')
