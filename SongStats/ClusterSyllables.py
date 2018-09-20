import os
import glob
import time
from sklearn.cluster import AffinityPropagation
import numpy as np
import pandas as pd
from skimage.measure import label, regionprops
import csv
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
from matplotlib.backends.backend_pdf import PdfPages
# import matplotlib.pyplot as plt
# import seaborn as sns; sns.set()
import matplotlib
import utils as utils
import time
start_time = time.time()
import gc
import pickle
from scipy.cluster import hierarchy
from scipy.spatial import distance
from sklearn.cluster import KMeans
import math
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale



syllable_correlation = np.loadtxt("C:/Users/abiga\Box "
                                  "Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\ClusterSyllables/1Dcorr"
                                  "\AllSylls_SimMatrix_1Dcorr_desktop.txt", delimiter=' ')

# with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/AllSylls_Names'
#           '.txt') as f:
#     names = f.read().splitlines()
#
# with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/AllSylls_Sylls'
#           '.txt') as f:
#     sylls_list = f.read().split(',')

with open("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData\ClusterSyllables/1Dcorr"
          "\AllSylls_Sylls_1Dcorr_desktop.pkl", 'rb') as f:
    names_sylls = pickle.load(f)

names = zip(*names_sylls)[0]
sylls = zip(*names_sylls)[1]
print(names)
print(syllable_correlation.shape)
quit()


#threshold the matrix
# syllable_correlation[syllable_correlation < 40] = 0

"""
KMeans
"""
# # all should have same height, just different widths
# max_width = 0
# max_syll= None
# for i in range(len(sylls)):
#     if sylls[i].shape[1] > max_width:
#         max_width = sylls[i].shape[1]
#         max_syll = i
#
# sylls_padded = []
# for i in range(len(sylls)):
#     if sylls[i].shape[1] < max_width:
#         add_left = int(math.ceil((max_width-sylls[i].shape[1])/2.0))
#         add_right = int(math.floor((max_width-sylls[i].shape[1])/2.0))
#         sylls_padded.append(np.pad(sylls[i], ((0, 0), (add_left, add_right)), 'constant'))
#
# data = scale(np.asarray(sylls_padded).reshape(-1, len(sylls_padded)))
# pca = PCA(n_components=30).fit(data)
#
# km = KMeans(init=pca.components_, n_clusters=30, n_init=1, n_jobs=1)
# km.fit(data)
#
# # km = KMeans(n_jobs=1, n_clusters=30, n_init=20)
# # km.fit(np.asarray(sylls_padded).reshape(-1, len(sylls_padded)))
#
#
# labels = km.labels_
# labeled_names = [[y, x] for y, x in sorted(zip(labels, names))]
# print(labeled_names)
#
#
# n, m = 4, 10
#
# # Don't forget to indent after the with statement
# matplotlib.rcParams.update({'font.size': 6})
# with PdfPages('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables'
#               '/TestingKmeans.pdf') as pdf:
#     f, axarr = plt.subplots(n, m)
#     arr_ij = [(x, y) for x, y in np.ndindex(axarr.shape)]
#     subplots = [axarr[index] for index in arr_ij]
#     splot_index = 0
#     # Iterate through each sample in the data
#     for sample in range(len(sylls_padded)):
#
#         subplots[splot_index].imshow(sylls_padded[sample])
#         subplots[splot_index].set_title(str(labels[sample]))
#         subplots[splot_index].xaxis.set_visible(False)
#         subplots[splot_index].spines['top'].set_linewidth(0.3)
#         subplots[splot_index].spines['right'].set_linewidth(0.3)
#         subplots[splot_index].spines['bottom'].set_linewidth(0.3)
#         subplots[splot_index].spines['left'].set_linewidth(0.3)
#
#         # Keep subplotting through the samples in the data and increment
#         # a counter each time. The page will be full once the count is equal
#         # to the product of the user-set dimensions (i.e. n * m)
#         splot_index += 1
#
#         # We can basically repeat the same exact code block used for the
#         # first layout initialization, but with the addition of 4 new lines:
#         # 2 for saving the just-finished page to the pdf, 1 for the
#         # page's execution time, & 1 more to reset the subplot index
#         if splot_index == n*m:
#             pdf.savefig()
#             plt.close(f)
#
#             f, axarr = plt.subplots(n, m)
#             arr_ij = [(x, y) for x, y in np.ndindex(axarr.shape)]
#             subplots = [axarr[index] for index in arr_ij]
#             splot_index = 0
#
#
#     # Done!
#     # But don't forget the last page
#     pdf.savefig()
#     plt.close(f)
#
# with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/1Dcorr'
#           '/AllSylls_1Dcorr_clusterResults_noThresh_pref52.csv', 'w') as out:
#     csv_out = csv.writer(out)
#     csv_out.writerow(['label', 'song'])
#     for row in names:
#         csv_out.writerow(row)
#
# quit()
#

"""
run affinity propogation
"""

af = AffinityPropagation(affinity='precomputed', verbose=True, preference=0)
af.fit(syllable_correlation)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
# print af.labels_, af.cluster_centers_indices_

# see what the clusters look like
n_clusters_ = len(cluster_centers_indices)
n_labels = len(labels)
syll_corr_index = range(0, len(syllable_correlation))

# print(names)
# print(labels)
print('Number of Labels: %d' % n_labels)
print('Estimated number of clusters: %d' % n_clusters_)
labeled_names = [[y, x] for y, x in sorted(zip(labels, names))]
print(labeled_names)

# labels_sorted = sorted(labels)
# # labels_sorted_index = [int(j) for j in sorted(range(len(labels)), key=labels.__getitem__)]
# labels_sorted_index = [int(j) for j in sorted(range(len(labels)), key=labels.__getitem__)]
# sylls_sorted = [sylls[x] for x in labels_sorted_index]
# syll_corr_index_sorted = [syll_corr_index[x] for x in labels_sorted_index]
# names_sorted = [names[x] for x in labels_sorted_index]
# print(names_sorted)
# print(labeled_names == names_sorted)

labels_sorted, names_sorted, syll_corr_index_sorted, sylls_sorted = zip(*sorted(zip(labels, names, syll_corr_index,
                                                                                    sylls)))



# plotting
# fig1, ax1 = plt.subplots(4, 12)
# fig1.subplots_adjust(hspace=0.025, wspace=0.05)
# for i in range(1, 48):
#     plt.subplot(4, 12, i)
#     plt.imshow(sylls_sorted[i-1], cmap='jet')
#     plt.gca().set_title(labels_sorted[i-1])
# plt.show()
# plt.savefig("C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/"
#             + 'Testing' + '.png', type='png')

# fig2, ax2 = plt.subplots(4, 12)
# fig2.subplots_adjust(hspace=0.025, wspace=0.05)
# for i in range(1, 49):
#     plt.subplot(4, 12, i)
#     plt.imshow(sylls_sorted[i+48])
#     plt.gca().set_title(labels_sorted[i+48])
# plt.show()

# # find maximum length syllable and pad all others to be the same size
# max_syll_len = max(np.size(s, 1) for s in sylls_sorted)
# print(max_syll_len)
# pad_sylls_sorted = [np.pad(i, (max_syll_len-np.size(i, 1), 0), 'constant', constant_values=(0, 0)) for i in
#                     sylls_sorted]

# Create pdf with syllables
# Dimensions for any n-rows x m-cols array of subplots / pg.
n, m = 4, 10

# Don't forget to indent after the with statement
matplotlib.rcParams.update({'font.size': 6})
with PdfPages('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/1Dcorr'
              '/AllSylls_1Dcorr_clusterResults_noThresh_pref0.pdf') as pdf:

    # # Let's time the execution required to create and save
    # # each full page of subplots to the pdf
    # start_time = timeit.default_timer()

    # Before beginning the iteration through all the data,
    # initialize the layout for the plots and create a
    # representation of the subplots that can be easily
    # iterated over for knowing when to create the next page
    # (and also for custom settings like partial axes labels)
    f, axarr = plt.subplots(n, m)
    # f.subplots_adjust(hspace=0.025, wspace=0.05)
    arr_ij = [(x, y) for x, y in np.ndindex(axarr.shape)]
    subplots = [axarr[index] for index in arr_ij]
    # To conserve needed plotting real estate,
    # only label the bottom row and leftmost subplots
    # as determined automatically using n and m
    splot_index = 0
    # for s, splot in enumerate(subplots):
    #     splot.set_ylim(0,.15)
    #     splot.set_xlim(0,50)
    #     last_row = ( n*m-s < m+1 )
    #     first_in_row = ( s % m == 0 )
    #     if last_row:
    #         splot.set_xlabel("X-axis label")
    #     if first_in_row:
    #         splot.set_ylabel("Y-axis label")

    # Iterate through each sample in the data
    for sample in range(len(sylls_sorted)):

        # As a stand-in for real data, let's just make numpy take 100 random draws
        # from a poisson distribution centered around say ~25 and then display
        # the outcome as a histogram
        # scaled_y = np.random.randint(20, 30)
        # random_data = np.random.poisson(scaled_y, 100)
        # subplots[splot_index].hist(random_data, bins=12, normed=True,
        #                            fc=(0,0,0,0), lw=0.75, ec='b')
        subplots[splot_index].imshow(sylls_sorted[sample])
        subplots[splot_index].set_title(str(labels_sorted[sample]) + ', ' + str(syll_corr_index_sorted[sample]))
        subplots[splot_index].xaxis.set_visible(False)
        subplots[splot_index].spines['top'].set_linewidth(0.3)
        subplots[splot_index].spines['right'].set_linewidth(0.3)
        subplots[splot_index].spines['bottom'].set_linewidth(0.3)
        subplots[splot_index].spines['left'].set_linewidth(0.3)

        # Keep subplotting through the samples in the data and increment
        # a counter each time. The page will be full once the count is equal
        # to the product of the user-set dimensions (i.e. n * m)
        splot_index += 1

        # We can basically repeat the same exact code block used for the
        # first layout initialization, but with the addition of 4 new lines:
        # 2 for saving the just-finished page to the pdf, 1 for the
        # page's execution time, & 1 more to reset the subplot index
        if splot_index == n*m:
            pdf.savefig()
            plt.close(f)
            # print(timeit.default_timer()-start_time)
            # start_time = timeit.default_timer()
            f, axarr = plt.subplots(n, m)
            # f.subplots_adjust(hspace=0.025, wspace=0.05)
            arr_ij = [(x, y) for x, y in np.ndindex(axarr.shape)]
            subplots = [axarr[index] for index in arr_ij]
            splot_index = 0
            # for s,splot in enumerate(subplots):
            #     splot.set_ylim(0,.15)
            #     splot.set_xlim(0,50)
            #     last_row = ( (n*m)-s < m+1 )
            #     first_in_row = ( s % m == 0 )
            #     if last_row:
            #         splot.set_xlabel("X-axis label")
            #     if first_in_row:
            #         splot.set_ylabel("Y-axis label")

    # Done!
    # But don't forget the last page
    pdf.savefig()
    plt.close(f)

with open('C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\StatsOfFinalData/ClusterSyllables/1Dcorr'
          '/AllSylls_1Dcorr_clusterResults_noThresh_pref0.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['label', 'song'])
    for row in labeled_names:
        csv_out.writerow(row)

print "My program took", time.time() - start_time, "to run"





# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

# #############################################################################
# # Plot result
# import matplotlib.pyplot as plt
# from itertools import cycle
#
# plt.close('all')
# plt.figure(1)
# plt.clf()
#
# colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
# for k, col in zip(range(n_clusters_), colors):
#     class_members = labels == k
#     cluster_center = X[cluster_centers_indices[k]]
#     plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
#     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=14)
#     for x in X[class_members]:
#         plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)
#
# plt.title('Estimated number of clusters: %d' % n_clusters_)
# plt.show()



"""
hierarchical clustering
"""
# # fig = plt.figure()
# # plt.imshow(syllable_correlation, interpolation='nearest', cmap='jet')
# # plt.show()
#
# dissimilarity = distance.squareform(100-syllable_correlation)
# threshold = 50
# linkage = hierarchy.linkage(dissimilarity, method='ward', metric='correlation')
# clusters = hierarchy.fcluster(linkage, threshold, criterion='maxclust')
# print(len(clusters))
# print(clusters.max())
# hierarchy.dendrogram(linkage, color_threshold=45)
# plt.show()
#
# # Plotting
# fig, ax = plt.subplots()
# ax.plot(range(1, len(linkage)+1), linkage[::-1, 2])
# knee = np.diff(linkage[::-1, 2], 2)
# num_clust = knee.argmax() + 2
# print(num_clust)
# # ax.plot(range(2, len(linkage)), knee)
#
# plt.show()
#

