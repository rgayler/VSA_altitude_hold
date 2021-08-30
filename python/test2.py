#!/usr/bin/env python3
'''
Replicates second two figures from
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa

import matplotlib.pyplot as plt

DIMS = 10000
N = 1000  # number of pairs to create
BINS = 30

# make an encoder specification with realistic vector dimension
ss = vsa.mk_scalar_encoder_spline_spec(DIMS, (0, 1))

for x in 0.5, 0.05:

    # generate n pairs of encodings of the same scalar (x) and make a
    # one-column data frame with the cos similarity of each vector pair
    cos = [vsa.cos_sim(vsa.encode_scalar_spline(x, ss),
                       vsa.encode_scalar_spline(x, ss)) for _ in range(N)]

    plt.hist(cos, bins=BINS)
    plt.xlabel('cos')
    plt.ylabel('count')
    plt.title('x = %2.2f' % x)
    plt.show()
