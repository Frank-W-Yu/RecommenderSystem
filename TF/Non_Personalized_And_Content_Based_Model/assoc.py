import tensorflow as tf


def parse_data(line):
    columns = tf.decode_csv(line, record_defaults=[[0.0], [0.0], [0.0], [0.0]])
    return tf.stack(columns)

def load_data(file_name, header_lines):
    data_set = tf.data.TextLineDataset(file_name).skip(header_lines)
    data_set = data_set.map(parse_data)
    return data_set

def associationItemBasedItemRecommender(numOfRec, movie_rating):
    pass

def basicAssociation(file_name):
    ld = load_data(file_name, 1)
    ld_next = ld.make_one_shot_iterator().get_next()
    item_users = {}
    all_users = {}

