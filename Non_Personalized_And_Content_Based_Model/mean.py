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
    # file_name = r'/home/rma_lab/frank/Recommender/RecommenderSystem/Non_Personalized_And_Content_Based_Model/data/ratings.csv'
    ld = load_data(file_name, 1)
    ld_next = ld.make_one_shot_iterator().get_next()
    # movie_rating = tf.contrib.lookup.MutableHashTable(key_dtype=tf.float32, value_dtype=tf.float32, default_value=-1)
    movie_rating = {}
    users = {}
    #means = tf.contrib.lookup.HashTable(key_dtype=tf.int32, value_dtype=tf.int32, default_value=-1)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        try:
            # for i in range(10):
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
        movie_ids = tf.convert_to_tensor(list(movie_rating.keys()))
        ratings = tf.convert_to_tensor(list(movie_rating.values()))
        table = tf.contrib.lookup.HashTable(tf.contrib.lookup.KeyValueTensorInitializer(movie_ids, ratings), -1)
        table.init.run()
        print('table size')
        print(table.size().eval())
        out = table.export()
        print(out.eval())
    return out

if __name__ == '__main__':
    simple_mean('data/ratings.csv')
