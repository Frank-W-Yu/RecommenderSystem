import pandas as pd
import os
from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import als, item_knn as knn
from lenskit.metrics import topn as tnmetrics

data = pd.read_csv(r'data\u.data', sep='\t',
                   names=['user', 'item', 'rating', 'timestamp'], skiprows=1)
algo_ii = knn.ItemItem(20)
algo_als = als.BiasedMF(50)

def eval(aname, algo, train, test):
    fittable = util.clone(algo)
    algo.fit(train)
    users = test.user.unique()
    # the recommend function can merge rating values
    recs = batch.recommend(algo, users, 100,
            topn.UnratedCandidates(train), test)
    # add the algorithm
    recs['Algorithm'] = aname
    return recs

all_recs = []
test_data = []
for train, test in xf.partition_users(data[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)):
    test_data.append(test)
    all_recs.append(eval('ItemItem', algo_ii, train, test))
    all_recs.append(eval('ALS', algo_als, train, test))