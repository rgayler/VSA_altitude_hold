#!/usr/bin/env python3
'''
Replicates figures from 3.2 Zero threshold section of
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def plotvert(x):
    plt.plot([x, x], [-0.1, +1.1], color=(.5, .5, .5), linewidth=1)


def test(knotmax, maxval, zero_threshes):

    ss = vsa.mk_scalar_encoder_spline_spec(10000, np.linspace(0, knotmax, 100))

    x_in = [x for x in np.linspace(-0.1, maxval, 1000)]

    for zero_thresh in zero_threshes:

        x_out = [vsa.decode_scalar_spline(
            vsa.encode_scalar_spline(x, ss), ss, zero_thresh) for x in x_in]

        r = stats.linregress(x_in, x_out)

        plt.scatter(x_in, x_out, color='k', s=0.1)
        plt.xlim([-0.1, +1.1])
        plt.plot(x_in, r.intercept + r.slope*np.array(x_in), 'r', linewidth=1)
        plotvert(0)
        plotvert(1)
        plt.xlabel('x_in')
        plt.ylabel('x_out')
        plt.title('knots = 0:%d   zero_thresh = %d' % (knotmax, zero_thresh))
        plt.show()


test(100, 1.1, (8, 6, 5))
test(2, 2.1, (4, 2, 1, 0))
