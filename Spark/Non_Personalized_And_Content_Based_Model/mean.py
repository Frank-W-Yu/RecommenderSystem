import numpy as np
import pandas as pd
import pyspark
import time

def map_func(line):
    items = line.split(',')
    return [(int(items[1]), float(items[2]))]
#    ret = []
#    ret.append(('userId', items[0]))
#   ret.append(('movieId', items[1]))
#    ret.append(('rating', items[2]))
#    return ret
def map_cal_mean(item):
    cnt = 0
    total_rating = 0
    for rating in item[1]:
        cnt += 1
        total_rating += rating
    if cnt == 0:
        mean_rating = 0
    else:
        mean_rating = total_rating / cnt
    return (item[0], mean_rating)

def map_val_cal_mean(item):
    cnt = 0
    total_rating = 0
    for rating in item:
        cnt += 1
        total_rating += rating
    if cnt == 0:
        mean_rating = 0
    else:
        mean_rating = total_rating / cnt
    return mean_rating

def simple_mean(file_name):
    sc = pyspark.SparkContext('local', 'text')
    textFile = sc.textFile('file:///home/rma_lab/frank/Recommender/RecommenderSystem/Spark/Non_Personalized_And_Content_Based_Model/data/ratings.csv')
    header = textFile.first()
    dataset = textFile.filter(lambda row: row != header)
    # mean_ratings = dataset.flatMap(map_func).groupByKey().map(map_cal_mean)
    mean_ratings = dataset.flatMap(map_func).groupByKey().mapValues(map_val_cal_mean).sortBy(lambda x: x[1], ascending=False)
    return mean_ratings

def damped_mean(file_name, damp_factor):
    sc = pyspark.SparkContext('local', 'text')
    textFile = sc.textFile('file:///home/rma_lab/frank/Recommender/RecommenderSystem/Spark/Non_Personalized_And_Content_Based_Model/data/ratings.csv')
    header = textFile.first()
    dataset = textFile.filter(lambda row: row != header)
    global_mean = dataset.flatMap(lambda line: line[2])
    # mean_ratings = dataset.flatMap(map_func).groupByKey().map(map_cal_mean)
    mean_ratings = dataset.flatMap(map_func).groupByKey().mapValues(map_val_cal_mean).sortBy(lambda x: x[1], ascending=False)
    return mean_ratings

    
    
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
    return movie_rating.take(5)

if __name__ == '__main__':
    start_time = time.time()
    file_name = r'data/ratings.csv'
    mean_ratings = simple_mean(file_name) 
    print(recommendItems(10, mean_ratings))
    print("------{} seconds------".format(round(time.time() - start_time),2))

