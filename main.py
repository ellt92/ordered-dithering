import numpy as np
from matplotlib.pyplot import imread
from matplotlib.pyplot import imsave
import matplotlib.pyplot as plt
import math
from skimage.color import rgb2gray
import sys
import argparse
import os

def reverse_int(x):
    result = 0
    pos_x = abs(x)
    while pos_x:
        result = result * 10 + pos_x % 10
        pos_x /= 10
    return result if x >= 0 else (-1) * result

def part1by1(n):
    n&= 0x0000ffff
    n = (n | (n << 8)) & 0x00FF00FF
    n = (n | (n << 4)) & 0x0F0F0F0F
    n = (n | (n << 2)) & 0x33333333
    n = (n | (n << 1)) & 0x55555555
    return n

def interleave2(x, y):
        return part1by1(x) | (part1by1(y) << 1)

PATH = os.getcwd()
parser=argparse.ArgumentParser()

parser.add_argument('--image', help='name of the image file including extension (required)')
parser.add_argument('--size', help='size of the Bayer matrix (optional, default=4)')
parser.add_argument('--range', help='range of dithering spread (optional, default=8)')
parser.add_argument('--offset', help='brightness offset, multiple of range (optional, default=0)')

args=parser.parse_args()

filename = args.image
if filename is None:
    print("no image provided, exiting...")
    exit()
n = int(args.size or 4)
r = int(args.range or 8)
offset = (1 / r) * int(args.offset or 0)

image = imread("{}/{}".format(
    PATH, filename
))
image = rgb2gray(image)
output = np.zeros(image.shape)


M = np.zeros([n*2,n*2])

for i in range(0, n*2):
    for j in range(0, n*2):
        temp = interleave2(i ^ j, i)
        b = '{:0{width}b}'.format(temp, width=int(math.log2((n*2)**2)))
        M[i][j] = int(b[::-1], 2) / ((n * 2) ** 2) - 0.5

for i in range(0, image.shape[0]):
    for j in range(0, image.shape[1]):
        image_val = image[i][j]
        matrix_val = M[i % (n*2)][j % (n*2)]
        curr_range = 1 / r
        temp = image_val + (curr_range * matrix_val)
        output[i][j] = (round(temp * (1 / curr_range)) / (1 / curr_range)) - offset

if not os.path.exists('bin'):
    os.makedirs('bin')
imsave("{}/bin/dither_n-{}_r-{}_o-{}_{}".format(
    PATH,
    n,
    r,
    offset,
    filename
), np.clip(output, 0, 1), cmap='gray')
