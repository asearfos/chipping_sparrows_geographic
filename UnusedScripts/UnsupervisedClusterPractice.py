import matplotlib.pyplot as plt
from sklearn import cluster, datasets
from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
import numpy as np

digits = datasets.load_digits()
images = digits.images
print(len(images))
print(images.shape)
# plt.imshow(images[1])
# plt.show()
X = np.reshape(images, (len(images), -1))
Y = np.reshape(images, (-1, len(images)))
print(X.shape)
print(Y.shape)
connectivity = grid_to_graph(*images[0].shape)

agglo = cluster.FeatureAgglomeration(connectivity=connectivity, n_clusters=9)
agglo.fit(X)
print(len(agglo.labels_))
# FeatureAgglomeration(affinity='euclidean', compute_full_tree='auto',...
X_reduced = agglo.transform(X)

X_approx = agglo.inverse_transform(X_reduced)
images_approx = np.reshape(X_approx, images.shape)
for i in range(images.size):
    plt.imshow(images[i])
    plt.show()