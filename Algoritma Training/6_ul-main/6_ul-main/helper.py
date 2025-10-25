import warnings
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from pylab import rcParams
from sklearn.decomposition import PCA
from numpy.linalg import eig
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import importlib

plt.style.use('seaborn-v0_8-whitegrid')
warnings.filterwarnings('ignore')

def biplot_pca (data):
    """
    Function to perform plots with first 2 PC from PCA on selected data.
    Data needs to be scales for the better result.
    
    data = selected dataframe
    """
    
    pca = PCA()
    pca.fit(data.values)
    eig_vec_pc1 = pca.components_[0]
    eig_vec_pc2 = pca.components_[1]
    value_pc1 = pca.transform(data)[:,0]
    value_pc2 = pca.transform(data)[:,1]
    for i in range(len(eig_vec_pc1)):
    # arrows project features (ie columns from csv) as vectors onto PC axes
        plt.arrow(0, 0, eig_vec_pc1[i]*max(value_pc1), eig_vec_pc2[i]*max(value_pc2),
                  color='yellow', width=0.0005, head_width=0.0025)
        plt.text(eig_vec_pc1[i]*max(value_pc1)*1.2, eig_vec_pc2[i]*max(value_pc2)*1.2,
                 list(data.columns.values)[i], color='magenta')

    for i in range(len(value_pc1)):
    # circles project documents (ie rows from csv) as points onto PC axes
        plt.scatter(value_pc1[i], value_pc2[i], c='grey')
        plt.text(value_pc1[i]*1.2, value_pc2[i]*1.2, list(data.index)[i], color='brown')
    plt.title('Biplot PCA', fontsize=20)
    plt.xlabel('PC1', fontsize=14)
    plt.ylabel('PC2', fontsize=14)
    
    return plt.show()

def plot_silscore(data, kmax=10):
    """
    Function for plotting silhouette score result.
    Perform better with scaled data.
    
    data = dataframe selected;
    kmax = int, default=10;
    """
    np.random.seed(2102)
    sil = []
    # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
    for k in range(2,kmax+1):
        kmeansx = KMeans(n_clusters = k).fit(data)
        labels = kmeansx.labels_
        sil.append(silhouette_score(data, labels, metric = 'euclidean', random_state=0))
    
    plt.plot(list(range(2,kmax+1)), sil)
    plt.title('Silhouette Score', fontsize=20)
    plt.xlabel("Number of cluster (K)", fontsize=14)
    plt.ylabel("Silhouette Score", fontsize=14)
    
    return plt.show()

def plot_elbow_kmeans(data, kmax=10):
    """
    Function for visualizing elbow plot for K-Means.
    
    data = dataframe selected;
    kmax = int, default=10;
    """
    np.random.seed(121)
    wss = []
    # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
    for k in range(2,kmax+1):
        kmeansx = KMeans(n_clusters = k).fit(data)
        wss_iter = kmeansx.inertia_
        wss.append(wss_iter)
    
    plt.plot(list(range(2,kmax+1)), wss, marker='o')
    plt.title('Elbow Method for K-Means', fontsize=20)
    plt.xlabel("Number of cluster (K)", fontsize=14)
    plt.ylabel("Total Within Sum of Square", fontsize=14)
    
    return plt.show()

def plot_elbow_kmedoids(data, kmax=10):
    """
    Function for visualizing elbow plot for K-Medoids.
    K-Medoids  tries to minimize the sum of distances between each point and the medoid of its cluster.
    
    data = Gower matrix (output from go.gower_matrix());
    kmax = int, default=10;
    """
    np.random.seed(121)
    sum_of_distances = []
    # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
    for k in range(2,kmax+1):
        kmedx = KMedoids(n_clusters = k,
                         metric = 'precomputed',
                         method = 'pam').fit(data)
        sod_iter = kmedx.inertia_
        sum_of_distances.append(sod_iter)
    
    plt.plot(list(range(2,kmax+1)), sum_of_distances, marker='o')
    plt.title('Elbow Method with for K-Medoids', fontsize=20)
    plt.xlabel("Number of cluster (K)", fontsize=14)
    plt.ylabel("Total Sum of Distances", fontsize=14)
    
    return plt.show()

def biplot_kmeans(data, k, feature_name=False):
    """
    Function to perform biplots for kmeans;
    
    data = selected dataframe, pandas.dataframe or numpy.ndarray;
    K = number of cluster, int;
    feature_name = option to show feature names and its arrow, bool, default=False;
    """
    
    x = np.arange(k)
    ys = [i+x+(i*x)**2 for i in range(k)]
    colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
    rainbow = [colors.rgb2hex(i) for i in colors_array]
    
    pca = PCA()
    try:
        pca.fit(data.values)
    except:
        pca.fit(data)
    eig_vec_pc1 = pca.components_[0]
    eig_vec_pc2 = pca.components_[1]
    transformed_data = pca.transform(data)
    value_pc1 = transformed_data[:,0]
    value_pc2 = transformed_data[:,1]
    kmeansx = KMeans(n_clusters = k).fit(transformed_data)
    label = list(kmeansx.labels_)
    u_labels = np.unique(label)
    if feature_name:        
        for i in range(len(eig_vec_pc1)):
        # arrows project features (ie columns from csv) as vectors onto PC axes
            plt.arrow(0, 0, eig_vec_pc1[i]*max(value_pc1), eig_vec_pc2[i]*max(value_pc2),
                      color='yellow', width=0.0005, head_width=0.0025)
            plt.text(eig_vec_pc1[i]*max(value_pc1)*1.2, eig_vec_pc2[i]*max(value_pc2)*1.2,
                     list(data.columns.values)[i], color='magenta')

    #for i in range(len(value_pc1)):
    # circles project documents (ie rows from csv) as points onto PC axes
        #plt.scatter(value_pc1[i], value_pc2[i], c=rainbow[label[i]], label=label[i])
        #plt.text(value_pc1[i]*1.2, value_pc2[i]*1.2, list(data.index)[i], color='brown')
    for i in u_labels:
       plt.scatter(transformed_data[label == i , 0] , transformed_data[label == i , 1] , c = rainbow[i], label=i)
  
    plt.title(f'Biplot KMeans, number of cluster = {k}', fontsize=20)
    plt.xlabel('PC1', fontsize=14)
    plt.ylabel('PC2', fontsize=14)
    plt.legend()
    return plt.show()

def BCSS(X, kmeans):
    _, label_counts = np.unique(kmeans.labels_, return_counts = True)
    diff_cluster_sq = np.linalg.norm(kmeans.cluster_centers_ - np.mean(X, axis = 0), axis = 1)**2
    return sum(label_counts * diff_cluster_sq)

def plot_depth_readings_cluster(wellname, dataframe, curves_to_plot, depth_curve, log_curves=[], facies_curves=[]):
    df = dataframe.copy()
    
    # count the number of tracks we need
    num_tracks = len(curves_to_plot)
    
    facies_color = ['#F4D03F', '#F5B041','#DC7633','#6E2C00', '#1B4F72','#2E86C1', '#AED6F1', '#A569BD', '#196F3D', 'red','black', 'blue']
            
    # setup the figure and axes
    fig, ax = plt.subplots(nrows=1, ncols=num_tracks, figsize=(num_tracks*2, 10))
    
    # create a super title for the entire plot
    fig.suptitle(wellname, fontsize=20, y=1.05)
    
    # loop through each curve in curves_to_plot and create a track with that data
    for i, curve in enumerate(curves_to_plot):
        # mapping lithology classes to numbers
        if curve in facies_curves:
            if curve == 'LITHOLOGY_CLASS':
                lithology_numbers = {'Sandstone' : 1,
                 'Sandstone/Shale': 2,
                 'Shale': 3,
                 'Marl': 4,
                 'Dolomite': 5,
                 'Limestone': 6,
                 'Chalk': 7,
                 'Halite': 8,
                 'Anhydrite': 9,
                 'Tuff': 10,
                 'Coal': 11,
                 'Basement': 12}
                
                df[curve] = df[curve].map(lithology_numbers)
            
            cmap_facies = colors.ListedColormap(facies_color[0:df[curve].max()], 'indexed')
            
            cluster=np.repeat(np.expand_dims(df[curve].values,1), 100, 1)
            im=ax[i].imshow(cluster, 
                            interpolation='none', 
                            cmap=cmap_facies, 
                            aspect='auto',
                            vmin=df[curve].min(),
                            vmax=df[curve].max(), 
                            extent=[0,20, depth_curve.max(), depth_curve.min()])
        
        else:
            ax[i].plot(dataframe[curve], depth_curve)

        
        # setup a few plot cosmetics
        ax[i].set_title(curve, fontsize=14, fontweight='bold')
        ax[i].grid(which='major', color='lightgrey', linestyle='-')
        
        # we want to pass in the deepest depth first, so we are displaying the data 
        # from shallow to deep
        ax[i].set_ylim(depth_curve.max(), depth_curve.min())
 
        # only set the y-label for the first track. Hide it for the rest
        if i == 0:
            ax[i].set_ylabel('DEPTH (m)', fontsize=18, fontweight='bold')
        else:
            plt.setp(ax[i].get_yticklabels(), visible = False)
        
        # check to see if we have any logarithmic scaled curves
        if curve in log_curves:
            ax[i].set_xscale('log')
            ax[i].grid(which='minor', color='lightgrey', linestyle='-')
        
    
    plt.tight_layout()
    plt.show()
    
    return cmap_facies