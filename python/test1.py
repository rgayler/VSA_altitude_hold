#!/usr/bin/env python3

import vsa


# make an encoder specification with realistic vector dimension
ss = vsa.mk_scalar_encoder_spline_spec(1000, (-1, 1, 2, 4))

'''
# get the vectors corresponding to the knots
v1 <- ss$knots_vsa[[1]]
v2 <- ss$knots_vsa[[2]]
v3 <- ss$knots_vsa[[3]]
v4 <- ss$knots_vsa[[4]]

# make a sequence of scalar values that (more than) span the knot range
d <- tibble::tibble(
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
