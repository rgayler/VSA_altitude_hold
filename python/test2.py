#!/usr/bin/env python3
'''
Replicates second two figures from
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa

import numpy as np
import matplotlib.pyplot as plt

dims = 10

# make an encoder specification with realistic vector dimension
ss = vsa.mk_scalar_encoder_spline_spec(dims, (0, 1))

# generate n pairs of encodings of the same scalar (x)
x = 0.5   # scalar to encode (in the range 0 .. 1)
n = 10  # number of pairs to create

cos = [vsa.cos_sim(vsa.encode_scalar_spline(x, ss),
                   vsa.encode_scalar_spline(x, ss)) for _ in range(n)]

print(cos)

'''
# make a one-column data frame with the cos similarity of each vector pair
d = tibble::tibble(
  cos = purrr::map_dbl(1:n, ~
  )
)

geom_histogram(aes(x = cos))
'''
