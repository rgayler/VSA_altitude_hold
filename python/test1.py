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
print(x)
'''
d = tibble::tibble(
  x = seq(from = -1.5, to = 4.5, by = 0.05)
) %>% 
  dplyr::rowwise() %>% 
  dplyr::mutate(
    # encode each value of x
    v_x = vsa.encode_scalar_spline(x[[1]], ss) %>% list(),
    # get the cosine between the encoded x and each of the knot vectors
    cos_1 = vsa.cos_sim(v_x, v1),
    cos_2 = vsa.cos_sim(v_x, v2),
    cos_3 = vsa.cos_sim(v_x, v3),
    cos_4 = vsa.cos_sim(v_x, v4)
  ) %>% 
  dplyr::ungroup() %>%
  dplyr::select(-v_x) %>% 
  tidyr::pivot_longer(cos_1:cos_4, 
                      names_to = "knot", names_prefix = "cos_", 
                      values_to = "cos")

d %>% ggplot(aes(x = x)) +
  geom_hline(yintercept = c(0, 1), alpha = 0.3) +
  geom_vline(xintercept = c(-1, 1, 2, 4), alpha = 0.3) +
  geom_point(aes(y = cos, colour = knot))
'''
