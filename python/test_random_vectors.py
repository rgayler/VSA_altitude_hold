#!/usr/bin/env python3
'''
Try to decode a random vector (i.e. not a valid encoding of a scalar).

Replicates results from 3.3 Random vectors section of
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa
import numpy as np


def test(ss, zero_thresh):
    v = vsa.mk_atom_bipolar(10000)
    print(vsa.decode_scalar_spline(v, ss, zero_thresh))


ss = vsa.mk_scalar_encoder_spline_spec(10000, np.linspace(0, 2, 100))

# Setting a high zero threshold means that with high probability we will end up
# dividing by zero in the decoder.

test(ss, 4)
test(ss, 4)
test(ss, 4)
test(ss, 4)
test(ss, 4)

print()

# Setting a zero threshold means that approximately half the dot products will
# be set to zero.
test(ss, 0)
test(ss, 0)
test(ss, 0)
test(ss, 0)
test(ss, 0)

print()

# The probability of dividing by zero is nonzero.
# The “decoded” values lie in the range of the knots.
# Disabling the zero threshold results in a very small probability of dividing
# by zero. The weighted sum no longer makes sense because the weights can be
# negative. Consequently, the returned value can lie outside the range of the
# knots.
test(ss, -np.inf)
test(ss, -np.inf)
test(ss, -np.inf)
test(ss, -np.inf)
test(ss, -np.inf)
