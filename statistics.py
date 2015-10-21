from collections import namedtuple
from math import floor
from sensing import sense
from materials import two_materials


Bucket = namedtuple('Bucket', ['number', 'start_lambda', 'stop_lambda'])
Data_bucket = namedtuple('Data_bucket', ['number', 'start_lambda', 'stop_lambda', 'data'])

def bucket(lambda_min, lambda_max, width):
    buckets = []
    bucket_num = 1
    total_buckets = int(floor(((lambda_max - lambda_min)/width)))
    while bucket_num < total_buckets:
        if bucket_num == 1:
            buckets.append(Bucket(bucket_num, lambda_min, (lambda_min+width)))
        else:
            buckets.append(Bucket(bucket_num, (lambda_min+(width*bucket_num)), lambda_min+(width*(bucket_num+1))))
        bucket_num += 1
    return buckets



# value_at_index = dic.values()[index]
#
def histogram(buckets, material=two_materials['Aspen'], to_dict=False):
    data_buckets = []
    for bucket in buckets:
        reflectance_val = sense(bucket, material)
        data = Data_bucket(bucket.number, bucket.start_lambda, bucket.stop_lambda, reflectance_val)
        data_buckets.append(data)
    return data_buckets



