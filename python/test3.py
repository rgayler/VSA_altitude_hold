#!/usr/bin/env python3
'''
Replicates section 3.1 of
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa

def test(expected, encoded):

    obtained = vsa.decode_scalar_spline(vsa.encode_scalar_spline(encoded, ss), ss)

    print('Expect: %f; got %f' % (expected, obtained))

# Make an encoder specification with realistic vector dimension
ss = vsa.mk_scalar_encoder_spline_spec(10000, (-1, 1, 2, 4))

# Check that encoded values are decoded correctly across the range of the knots.
for expected, encoded in ((-1, -1.5), (-1, -1), (0, 0), (1, 1), (1.5, 1.5)):
    test(expected, encoded)

print()

# Check the random variation of intermediate values
for _ in range(5):
    test(0, 0)
