#!/usr/bin/env python3
'''
Replicates third pair of figures from
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def plotvert(x):
    plt.plot([x, x], [-0.1, +1.1], color=(.5, .5, .5), linewidth=1)


ss = vsa.mk_scalar_encoder_spline_spec(10000, np.arange(100))

x_in = [x for x in np.linspace(-0.1, +1.1, 1000)]

for zero_thresh in 8, 6, 5:

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
    plt.title('zero_thresh = %d' % zero_thresh)
    plt.show()
