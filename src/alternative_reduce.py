#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--keys',nargs='+',required=True)
args = parser.parse_args()

# imports
import os
import json
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import requests
import time
import math

# load each of the input paths
totals = {key: [] for key in args.keys}
for path in args.input_paths:
    date = path.split('geoTwitter')[1][:8]
    with open(path) as f:
        tmp = json.load(f)
        for k in tmp:
            if k in args.keys:
                cnt = 0
                for v in tmp[k]:
                    cnt += tmp[k][v]
                totals[k].append((date, cnt))



# Plot

for k in totals:
    print("k=", k)
    items = totals[k]
    ds = []
    vs = []
    for d,v in items:
        print(d,':',v)
        ds.append(d)
        vs.append(v)

    plt.plot(ds, vs, label = k)

plt.locator_params(axis='x', nbins=4)
plt.legend()

# Set the title and labels with font properties
plt.title(f"Use of {str(args.keys)[1:-1]} in 2020")
plt.xlabel('Date')
plt.ylabel('Tweets')

# Customize xticks and yticks
plt.xticks(fontsize=12)


timestamp = str(math.floor(time.time()))[-5:]

filename = f'plot_{timestamp}.png'

plt.savefig(filename)


# Upload Plot
url = f'https://transfer.archivete.am/{filename}'

with open(filename, 'rb') as file_data:
    response = requests.put(url, data=file_data)

print(response.text)
