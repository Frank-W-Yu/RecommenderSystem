import numpy as np
import pandas as pd

def load_data(file_name):
    data_set = pd.read_csv(file_name)
    return data_set

def simple_mean(file_name):
    data_set = load_data(file_name)
    means = data_set.groupby('movieId').mean()
    return means['rating'].to_dict()

def damped_mean(file_name, damp_factor):
    data_set = load_data(file_name)
    global_mean = data_set['rating'].mean()
    groupby_item = data_set.groupby('movieId')
    item_sum_rating = groupby_item.sum()['rating']
    item_count_rating = groupby_item.count()['userId']
    movie_rating = {}
    for movieId, rating in item_sum_rating.items():
        movie_rating[movieId] = (rating + damp_factor * global_mean) / (item_count_rating[movieId] + damp_factor)
    return movie_rating 

def recommendItems(numOfRec, movie_rating):
    results = []
    for k, v in movie_rating.items():
        results.append((k, v))
    results.sort(key = lambda x : -x[1])
    return results[:numOfRec]

if __name__ == '__main__':
    file_name = r'data/ratings.csv'
    movie_rating = damped_mean(file_name, 5)
#    movie_rating = simple_mean(file_name)
#    print(recommendItems(10, movie_rating))
#    movie_rating = simple_mean(file_name)
    results = recommendItems(10, movie_rating)
#    for k, v in results:
#        print('simple mean: ', k, ':', v)
#    damped_rating = damped_mean(file_name, 5)
#    results_damped = recommendItems(10, damped_rating)
    for k, v in results:
        print('damped mean: ', k, ':', v)
    
