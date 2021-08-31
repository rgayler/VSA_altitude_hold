#!/usr/bin/env python3
'''
Replicates section 3.1 of
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa

def report(expected, actual):
    print('Expect: %f; got %f' % (expected, actual))

# make an encoder specification with realistic vector dimension
ss = vsa.mk_scalar_encoder_spline_spec(10000, (-1, 1, 2, 4))

for expected, encoded in ((-1, -1.5), (-1, -1), (0, 0), (1, 1), (1.5, 1.5)):

    obtained = vsa.decode_scalar_spline(vsa.encode_scalar_spline(encoded, ss), ss)

    print('Expect: %f; got %f' % (expected, obtained))


# The decoded values at the knots are exactly correct.
# The decoded values between the knots are approximately correct.
# Check the random variation of intermediate values.
