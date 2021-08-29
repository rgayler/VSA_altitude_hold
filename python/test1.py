#!/usr/bin/env python3

import vsa

import numpy as np
import matplotlib.pyplot as plt

# make an encoder specification with realistic vector dimension
ss = vsa.mk_scalar_encoder_spline_spec(1000, (-1, 1, 2, 4))

# get the vectors corresponding to the knots
vecs = ss['knots_vsa']
v1 = vecs[0]
v2 = vecs[1]
v3 = vecs[2]
v4 = vecs[3]

# make a sequence of scalar values that (more than) span the knot range
x = np.arange(-1.5, 4.5, .05)

# get the cosine between the encoded x and each of the knot vectors
cos_1 = [vsa.cos_sim(vsa.encode_scalar_spline(xval, ss), v1) for xval in x]
cos_2 = [vsa.cos_sim(vsa.encode_scalar_spline(xval, ss), v2) for xval in x]
cos_3 = [vsa.cos_sim(vsa.encode_scalar_spline(xval, ss), v3) for xval in x]
cos_4 = [vsa.cos_sim(vsa.encode_scalar_spline(xval, ss), v4) for xval in x]

# plot the cosines
plt.plot(cos_1, '.')
plt.plot(cos_2, '.')
plt.plot(cos_3, '.')
plt.plot(cos_4, '.')
plt.xlabel('x')
plt.ylabel('cos')
plt.legend(['knot1', 'knot2', 'knot3', 'knot4'])
plt.show()
