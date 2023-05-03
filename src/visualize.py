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
import matplotlib.font_manager as fm

import requests
import time
import math


# Download Fonts
# Check if the file exists in the current path
file_name = "NotoSansCJKtc-Regular.otf"
file_exists = os.path.exists(file_name)

# If the file does not exist, download it using requests
if not file_exists:
    url = "https://github.com/openmaptiles/fonts/raw/master/noto-sans/NotoSansCJKtc-Regular.otf"
    response = requests.get(url)

    # Save the file to the current path
    with open(file_name, "wb") as file:
        file.write(response.content)
        print(f"{file_name} downloaded successfully.")
else:
    print(f"{file_name} already exists in the current path.")

# Apply fonts
fprop = fm.FontProperties(fname='NotoSansCJKtc-Regular.otf')


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
    

ks = ks[::-1][-10:]
vs = vs[::-1][-10:]



# Plot

plt.bar(range(len(ks)), vs)
plt.xticks(range(len(ks)), ks)

# Set the title and labels with font properties
plt.title(f"Use of {args.key} in 2020 by {args.input_path.split('.')[-1]}", fontproperties=fprop)
plt.xlabel('Key')
plt.ylabel('Tweets')

# Customize xticks and yticks
plt.xticks(fontsize=12)


timestamp = str(math.floor(time.time()))[-5:]

filename = f'{args.input_path}_{args.key[1:]}_{timestamp}.png'

plt.savefig(filename)


# Upload Plot
url = f'https://transfer.archivete.am/{filename}'

with open(filename, 'rb') as file_data:
    response = requests.put(url, data=file_data)

print(response.text)
