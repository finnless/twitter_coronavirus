#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
ks = []
vs = []
for k,v in items:
    print(k,':',v)
    ks.append(k)
    vs.append(v)
    

print("ks=", ks)
print("vs=", vs)


# Sort ks and vs in descending order based on the values in vs
sorted_kv = sorted(zip(ks, vs), key=lambda x: x[1], reverse=True)
sorted_ks, sorted_vs = zip(*sorted_kv)

print("sorted_ks=", sorted_ks)
print("sorted_vs=", sorted_vs)
fig, ax = plt.subplots(figsize =(16, 9))
ax.bar(sorted_ks, sorted_vs)

'''
fig, ax = plt.subplots(figsize =(16, 9))
ax.bar(ks, vs)
'''


import requests
import time
import math

timestamp = str(math.floor(time.time()))[-5:]

filename = f'{args.input_path}_{args.key[1:]}_{timestamp}.png'

print("filename=", filename)

plt.savefig(filename)

url = f'https://transfer.archivete.am/{filename}'


with open(filename, 'rb') as file_data:
    response = requests.put(url, data=file_data)

print(response.status_code)
print(response.text)


'''
with open(filename, 'rb') as f:
    r = requests.put(url, files={filename: f})

print(r.text)
'''
