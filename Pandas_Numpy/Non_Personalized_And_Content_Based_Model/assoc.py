import numpy as np
import pandas as pd

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
        for y_id, y_users in item_users.items():
            xy = 0.0
            for x_user in x_users:
                if x_user in y_users:
                    xy += 1.0
            item_scores[y_id] = xy / len(x_users)
        assoc_matrix[x_id] = item_scores
    return assoc_matrix

def assoc_recommender(assoc_matrix):
    results = {}



if __name__ == '__main__':
    file_name = r'data/ratings.csv'
    assoc_matrix = basic_association(file_name)
    print(len(assoc_matrix))

