import tensorflow as tf
import numpy as np

def parse_data(line):
    columns = tf.decode_csv(line, record_defaults=[[0.0], [0.0], [0.0], [0.0]])
    return tf.stack(columns)

def load_data(file_name, header_lines):
    data_set = tf.data.TextLineDataset(file_name).skip(header_lines)
    data_set = data_set.map(parse_data)
    return data_set

def simple_mean(file_name):
    ld = load_data(file_name, 1)
    ld_next = ld.make_one_shot_iterator().get_next()
    movie_rating = {}
    users = {}
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        try:
            i = j = 1
            while True:
                if i == 10000:
                    print(j)
                    j += 1
                    i = 0
                i += 1
                data_line = sess.run(ld_next)
                userId = int(data_line[0])
                movieId = int(data_line[1])
                rating = data_line[2]
                if movieId not in movie_rating:
                    movie_rating[movieId] = rating
                    users[movieId] = 1
                else:
               
                    movie_rating[movieId] = movie_rating[movieId] + rating
                    users[movieId] = users[movieId] + 1
        except tf.errors.OutOfRangeError:
            print('Done')
        for movie_id, rating in movie_rating.items():
            movie_rating[movie_id] = rating / users[movie_id]
    return movie_rating

def dampled_mean(file_name):
    ld = load_data(file_name, 1)
    ld_next = ld.make_one_shot_iterator().get_next()
    itemSumRating = {}
    itemCountRating = {}
    movie_rating = {}
    users = {}
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        try:
            i = j = 1
            while True:
                if i == 10000:
                    print(j)
                    j += 1
                    i = 0
                i += 1
                data_line = sess.run(ld_next)
                userId = int(data_line[0])
                movieId = int(data_line[1])
                rating = data_line[2]
                if movieId not in movie_rating:
                    movie_rating[movieId] = rating
                    users[movieId] = 1
                else:
               
                    movie_rating[movieId] = movie_rating[movieId] + rating
                    users[movieId] = users[movieId] + 1
        except tf.errors.OutOfRangeError:
            print('Done')
        for movie_id, rating in movie_rating.items():
            movie_rating[movie_id] = rating / users[movie_id]
    return movie_rating

def recommendItems(numOfRec, movie_rating):
    results = []
    for k, v in movie_rating.items():
        results.append((k, v))
    results.sort(key = lambda x : -x[1])
    return results[:numOfRec]

if __name__ == '__main__':
    movie_rating = simple_mean(r'data/ratings.csv')
    results = recommendItems(10, movie_rating)
    for k, v in results:
        print(k, ':', v)
