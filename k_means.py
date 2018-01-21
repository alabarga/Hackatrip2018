import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

# Import and select the data
df_all = pd.read_csv('car_processed.csv')
df_cat = pd.read_csv('car_cats.csv')
MONTH = 201507
df_all = df_all[df_all.mes == MONTH]
df = pd.merge(df_all, df_cat, left_on = 'zipcode', right_on = 'zipcode')
df = df.fillna(df.mean())  
cats = ['es_hotelservices', 'es_travel', 'es_barsandrestaurants', 'es_transportation']
for cat in cats:
    name = 'ratio_' + str(cat)
    name_gross = 'num_gross_' + str(cat)
    df[name] = df[str(name_gross)] / df['num_gross']
X = dataset.drop(['mes', 'zipcode'], axis=1)
# Normalize
sc = StandardScaler()
X = sc.fit_transform(X)

# Elbow method to select K
Ks = [i+2 for i in range(9)]
distortion = []
for k in Ks:
    KM = KMeans(n_clusters=k).fit(X)
    score = sum(np.min(cdist(X, KM.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0]
    print('The scoring for K=%.0f is %.2f' % (k, score))
    distortion.append(score)
plt.plot(Ks, distortion)
plt.show()
plt.close()

K = 5
clustering = KMeans(n_clusters=K, max_iter=10)
clustering.fit(X)
centroids = clustering.cluster_centers_
centroids = sc.inverse_transform(centroids)