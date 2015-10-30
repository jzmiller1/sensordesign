from collections import namedtuple
from math import floor
from sensing import sense
import sqlite3
from dbtools import DBContext



Bucket = namedtuple('Bucket', ['number', 'start_lambda', 'stop_lambda'])
Data_bucket = namedtuple('Data_bucket', ['number', 'start_lambda', 'stop_lambda', 'data'])

#This is a single bucket that covers the entire spectrum. It's needed because the sense function requires a bucket/band
spectral_bucket = ('-9', 100, 3000)


def bucket(lambda_min, lambda_max, width):
    buckets = []
    bucket_num = 1
    total_buckets = int(floor(((lambda_max - lambda_min)/width)))
    while bucket_num <= total_buckets:
        if bucket_num == 1:
            buckets.append(Bucket(bucket_num, lambda_min, (lambda_min+width)))
        else:
            buckets.append(Bucket(bucket_num, (lambda_min+(width*(bucket_num-1))), lambda_min+(width*bucket_num)))
        bucket_num += 1
    return buckets




# value_at_index = dic.values()[index]
#
def histogram(buckets, material, to_dict=False):
    data_buckets = []
    for bucket in buckets:
        reflectance_val = sense(bucket, material)
        data = Data_bucket(bucket.number, bucket.start_lambda, bucket.stop_lambda, reflectance_val)
        data_buckets.append(data)
    return data_buckets



def WaveHedges(h1, h2):
    sum = 0
    if len(h1) == len(h2):
        for i in range(len(h1)):
            if max(h1[i].data, h2[i].data) == 0:
                sum += 1
            else:
                sum += min(h1[i].data, h2[i].data)/float(max(h1[i].data, h2[i].data))
        return sum / (len(h1))
    else:
        return "the histograms need to be of equal length "


def get_top_n_spectra(material, n):
    #This is a single bucket that covers the entire spectrum. It's needed because the sense function requires a bucket/band
    spectral_bucket = bucket(100, 3000, 25)

    with DBContext('data.db') as db:
        db.execute("SELECT DISTINCT material FROM main WHERE material NOT LIKE ?;", (material,))
        comparison_materials = db.fetchall()

    histogram_list = []
    material_hist = histogram(spectral_bucket, material)

    for comp_material in comparison_materials:
        histogram_list.append([comp_material[0], histogram(spectral_bucket, comp_material[0])])

    for h in histogram_list:
        h.append(WaveHedges(material_hist, h[1]))

    return sorted(histogram_list, reverse=True, key=lambda x: x[2])[0:n]


def run():

    data = get_top_n_spectra('Aspen', 3)
    for item in data:
        print(item[0], item[2])