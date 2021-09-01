#!/usr/bin/env python3
'''
Replicates third pair of figures from
  https://rgayler.github.io/VSA_altitude_hold/encoder_spline.html
'''

import vsa
import numpy as np

ss = vsa.mk_scalar_encoder_spline_spec(10000, np.arange(100))

print(ss)

'''
# encode and decode random values over the first knot interval
runif(n = 1e3, min = -0.1, max = 1.1) %>% 
  tibble::tibble(x_in = .) %>% 
  dplyr::rowwise() %>% 
  dplyr::mutate(
    x_out = x_in %>% 
      vsa_encode_scalar_spline(ss) %>% 
      vsa_decode_scalar_spline(ss, zero_thresh = 8)
  ) %>% 
  dplyr::ungroup() %>% 
  ggplot() +
  geom_vline(xintercept = 0:1, alpha = 0.3) +
  geom_abline(slope = 1, intercept = 0, colour = "red", alpha = 0.5) +
  geom_point(aes(x = x_in, y = x_out), size = 0.1, alpha = 0.5) +
  ggtitle("zero_thresh = 8")
  '''
