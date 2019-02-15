import numpy as np
import pandas as pd
import time
import cython

%%cython

def load_data(file_name):
    data_set = pd.read_csv(file_name)
    return data_set

def basic_association(file_name):
    data_set = load_data(file_name)
    item_users = {}
    all_users = data_set['userId'].unique()
    grouped_rating = data_set.groupby('movieId')
    for movieId, item in grouped_rating:
        users = item['userId']
        item_users[movieId] = users
    assoc_matrix = {}
    for x_id, x_users in item_users.items():
        item_scores = {}
        x_users = x_users.tolist()
        for y_id, y_users in item_users.items():
            xy = 0.0
            y_users = y_users.tolist()
            for x_user in x_users:
                if x_user in y_users:
                    xy += 1.0
            item_scores[y_id] = xy / len(x_users)
        assoc_matrix[x_id] = item_scores
    print(len(assoc_matrix))
    print(assoc_matrix[1125])
    return assoc_matrix

def assoc_recommender(num_of_Rec, ref_item, assoc_matrix):
    results = []
    for k, v in assoc_matrix[ref_item].items():
        results.append((k, v))
    results.sort(key = lambda x : -x[1])
    return results[:num_of_Rec]

if __name__ == '__main__':
    start_time = time.time()
    file_name = r'data/ratings.csv'
    assoc_matrix = basic_association(file_name)
    results = assoc_recommender(10, 260, assoc_matrix)
    for k, v in results:
        print('Association rating: ', k, ':', v)
    print('Run time: ', time.time() - start_time)
