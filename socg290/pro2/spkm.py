#!/usr/bin/env python

"""
@package css
@file css/spkm.py
@author Edward Hunter
@brief Spherical k-means core algorithm and support routines.
"""

# Copyright and licence.
"""
Copyright (C) 2014 Edward Hunter
edward.a.hunter@gmail.com
840 24th Street
San Diego, CA 92102

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from common import *

cats = {
  'all' : None,
  '4' : [
    'comp.graphics',
    'rec.autos',
    'sci.space',
    'talk.religion.misc'
    ]
}

def count_cluster_sizes(no_clusters, no_docs, r):
    cluster_sizes = [0 for x in range(no_clusters)]
    for j in range(no_clusters):
        for i in range(no_docs):
            if r[i] == j:
                cluster_sizes[j] += 1
    return cluster_sizes


def initialize_clusters(x, cluster_ids, doc_ids):

    no_docs = len(doc_ids)
    no_clusters = len(cluster_ids)

    # Initialize shuffled docs ids.
    shuffled_docs = np.array(doc_ids)
    np.random.shuffle(shuffled_docs)

    # Initialize new assigments.
    r_new = np.zeros(no_docs, np.int32)

    # Initialize the centroids.
    mu = np.copy(x)[shuffled_docs[:no_clusters],:]

    return shuffled_docs, r_new, mu


def spkmeans(x, no_clusters, verbose=False, **kwargs):

    if not isinstance(x, np.ndarray):
        x = x.toarray()

    # Get doc and cluster ids.
    no_docs = x.shape[0]
    cluster_ids = range(no_clusters)
    doc_ids = range(no_docs)

    on_empty = kwargs.get('on_empty','restart')

    # Initialize the clusters
    shuffled_docs, r_new, mu = initialize_clusters(x, cluster_ids, doc_ids)

    # Initialize count and similary array.
    count = 0
    similarity = []

    # Spherical k means loop.
    while True:

        # Iteration start time.
        startime = time.time()

        # Update assignments.
        # Copy the old assignments.
        r = np.copy(r_new)

        # Compute the new assignments.
        products = np.dot(x,mu.T)
        r_new = np.argmax(products,axis=1)

        # Collect and sort the new scores.
        scores = np.array([products[i, r_new[i]] for i in doc_ids])
        scores_idx = np.argsort(scores)

        # Fix empty clusters here.
        empty = [i for i in cluster_ids if i not in r_new]
        if empty:
            print 'Iteration %i: empty clusters: %s' % (count, str(empty))
            if on_empty == 'restart':
                print 'Reinitializing algorithm.'
                shuffled_docs, r_new, mu = initialize_clusters(x, cluster_ids,
                                                               doc_ids)
                continue

            else:
                print 'Reassinging remote data to empty clusters.'
                for i,j in enumerate(empty):
                    r_new[scores_idx[-(i+1)]] = j
                empty = [i for i in cluster_ids if i not in r_new]
                if verbose:
                    print 'Adjusted empty clusers: ' + str(empty)

        newsim = 0
        for i in range(no_docs):
            newsim += products[i,r_new[i]]
        similarity.append(newsim)

        # Exit if assigments do not change.
        if np.all(r == r_new):
            sizes = count_cluster_sizes(no_clusters, no_docs, r)
            return mu, r, similarity, sizes

        # Update centroids.
        mu = np.zeros_like(mu)
        for i in range(no_docs):
            mu[r_new[i],:] += x[i,:]
        for j in range(no_clusters):
            mu_norm = np.linalg.norm(mu[j,:])
            if mu_norm == 0.0:
                print 'WARNING: Cluster %i empty!' % j

            else:
                mu[j,:] = mu[j,:]/mu_norm

        delta = time.time() - startime
        if verbose:
            print 'Iteration %i: %.2f seconds.' % (count, delta)
        count += 1

def tfidf_features(categories):
    """
    Get TF-IDF features for documents
    """
    
    print 'Fetching training data...'
    data = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'),
    categories=categories)
    
    labels = data.target
    n_class = numpy.unique(labels).shape[0]
    
    print 'Number of classes: %i' % n_class
    
    t0 = time.time()
    
    print 'Vectorizing training data...'
    vectorizer = TfidfVectorizer(sublinear_tf=True, norm='l2', max_df=0.5, stop_words='english')
    vectors = vectorizer.fit_transform(data.data)
    
    print 'done in %fs' % (time.time() - t0)
    print 'Number of training samples: %i' % vectors.shape[0]
    print 'Dimension of text vectors: %s' % vectors.shape[1]
    print 'Feature density: %f' % density(vectors)
    
    print 'Saving objects...'
    pickle.dump(vectorizer, open('vectorizer', 'w'))
    
    return vectors,labels, n_class

def report(labels, km_labels, mu, no_clusters, n_class):
    #Reporting
    print 'Loading objects...'
    vectorizer = pickle.load(open('vectorizer'))
    
    print '\n################### Reporting #######################\n'
    
    print 'Top terms per cluster'
    order_centroids = mu.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(no_clusters):
        print 'Cluster %d:' % i,
        for ind in order_centroids[i, :10]:
            print ' %s' % terms[ind],
        print ''
        
    print '\n'    
    print 'Homogeneity: %0.3f' % metrics.homogeneity_score(labels, km_labels)
    print 'Completeness: %0.3f' % metrics.completeness_score(labels, km_labels)
    print 'V-measure: %0.3f' % metrics.v_measure_score(labels, km_labels)
    print 'Adjusted Rand-Index: %.3f' % metrics.adjusted_rand_score(labels, km_labels)
    print 'Silhouette Coefficient: %0.3f' % metrics.silhouette_score(x, km_labels)
    
    print '\n'
    for cluster in range(no_clusters):
        print 'Cluster: %i' % cluster,
        count=dict()
        for i in range(len(km_labels)):
            if(km_labels[i]==cluster):
                if(count.has_key(labels[i])):
                    count[labels[i]]+=1
                else:
                    count[labels[i]]=1
        print count
          
if __name__== '__main__':
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cluster', action='store_true', 
                       help='Create clusters using spherical k-means clustering.')
    group.add_argument('--data', action='store_true',
                       help='Ensure the 20newsgroup data is downloaded to the local cache.')
    parser.add_argument('-c', '--categories', default='all')
    parser.add_argument('-k', '--clusters', default=0)
    args = parser.parse_args()
  
    if args.data:
        fetch_20newsgroups()

    if args.cluster:
        x, labels, n_class = tfidf_features(cats[args.categories])
        
        no_clusters = args.clusters
        if(no_clusters == 0):
            no_clusters = n_class
            
        mu, r, similarity, sizes = spkmeans(x, no_clusters)
        report(labels, r, mu, no_clusters, n_class)
        