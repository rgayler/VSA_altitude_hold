#!/usr/bin/env python3
#
# These are all the functions used across multiple notebooks.
# Functions used in a single notebook are defined in that notebook.
# These functions are `sourced` into each notebook in the setup chunk.
#
# Each function is labelled with a  '## ---- some_function_name' section header
# to identify the function for displaying the code in the notebook.
# See https://bookdown.org/yihui/rmarkdown-cookbook/read-chunk.html

import numpy as np
import matplotlib.pyplot as plt

## ---- vsa_mk_sample_spec --------------------------------------------------------

# function to make a sampling specification for adding VSA vectors

def vsa_mk_sample_spec(
  vsa_dim, # integer - dimensionality of VSA vectors
  sample_wt, # numeric vector - VSA vector sampling weights
  seed = None # integer - seed for random number generator
): # value # one VSA vector, the weighted sum (sampled) of the argument vectors

  # if seed is set the sampling specification vector is fixed
  # otherwise it is randomised
  np.random.seed(seed)
  
  return np.random.choice(len(sample_wt), size=vsa_dim, replace=True, p=sample_wt)

## ---- vsa_mag --------------------------------------------------------------------

# function to calculate the magnitude of a VSA vector
# Allow for the possibility that the vector might not be bipolar

def vsa_mag (
  v1 # numeric - VSA vector (not necessarily bipolar)
  ): # value # numeric - magnitude of the VSA vector

  # No numerical analysis considerations 
  return np.sqrt(np.sum(v1*v1))


## ---- vsa_mk_atom_bipolar ---------------------------------------------------------

# function to make an atomic VSA vector

def vsa_mk_atom_bipolar(
  vsa_dim, # integer - dimensionality of VSA vector
  seed = None # integer - seed for random number generator
  ): # value # one randomly selected VSA vector of dimension vsa_dim
  
  # if seed is set the the vector is fixed
  # otherwise it is randomised
  np.random.seed(seed)
  
  # Construct a random bipolar vector
  return 2 * (np.random.random(vsa_dim) > 0.5) - 1

## ---- vsa_multiply ----------------------------------------------------------------

# function to multiply an arbitrary number of VSA vectors

def vsa_multiply(vectors
     # >= 2 VSA vectors of identical dimension as arguments to multiply
  ): # value # one VSA vector, the weighted sum (sampled) of the argument vectors


    result = np.ones(len(vectors[0]))

    for v in vectors:
        result *= v

    return result

## ---- vsa_mk_scalar_encoder_spline_spec --------------------------------------------

# function to make the specification for a piecewise linear spline encoder

def vsa_mk_scalar_encoder_spline_spec(
  vsa_dim, # integer - dimensionality of VSA vectors
  knots, # numeric vector - scalar knot locations (in increasing order)
  seed = None # integer - seed for random number generator
  ): # value # data structure representing linear spline encoder specification

  # set the seed
  np.random.seed(seed)
  
  # generate VSA atoms corresponding to each of the knots
  return { 
          'knots_scalar' : knots,
          'knots_vsa' : [vsa_mk_atom_bipolar(vsa_dim) for _ in knots]
          }

## ---- vsa_dotprod -------------------------------------------------------------------

# function to calculate the dot product  of two VSA vectors
# Allow for the possibility that the vectors might not be bipolar

def vsa_dotprod(
  v1, v2 # numeric - VSA vectors of identical dimension (not necessarily bipolar)
  ): # value # numeric - cosine similarity of the VSA vectors

  # No numerical analysis considerations 
  return np.sum(v1*v2)

## ---- vsa_decode_scalar_spline -------------------------------------------------------

# function to encode a scalar numeric value to a VSA vector
# This function uses a linear interpolation spline
# to interpolate between a sequence of VSA vectors corresponding to the spline knots

def vsa_decode_scalar_spline (
  v, # numeric - VSA vector (not necessarily bipolar)
  spline_spec, # data frame - spline spec created by vsa_mk_scalar_encoder_spline_spec()
  zero_thresh = 4 # numeric[1] - zero threshold (in standard deviations)
  ): # numeric[1] - scalar value decoded from v

  # get the dot product of the encoded scalar with each of the knot vectors
  dotprods = np.array(list(map(lambda w : vsa_dotprod(v,w), spline_spec['knots_vsa'])))

  # set dot products below the zero threshold to 0.5
  zero_thresh = zero_thresh * np.sqrt(len(v) * 0.5)
  dotprods[dotprods<zero_thresh] = 0

  # normalise the dot products
  dotprods = dotprods / np.sum(dotprods)

  # return the weighted sum of the knot scalars
  return np.sum(dotprods * spline_spec['knots_scalar'])

## ---- vsa_add -------------------------------------------------------------------------

# function to add (weighted sum) an arbitrary number of VSA vectors given as arguments
# Weighted add is implemented as weighted sampling from the source vectors
# If sample_spec is given it specifies which argument vector is the source for
# each element of the output vector If sample_wt is given the sample
# specification is generated randomly If neither sample_spec or sample_wt is
# given then sample_wt is constructed with equal weight for each argument
# vector

def vsa_add(
  vectors,
  sample_spec=None, # integer vector - source (argument VSA vector) for each element of result
  sample_wt=None    # numeric vector - argument vector sampling weights
  ): # value # one VSA vector, the weighted sum (sampled) of the argument vectors

  vsa_dim = len(vectors[0])

  return 0
  
  '''
  if sample_spec is None:

    # sample spec not supplied - make a new random one
    # create a sampling weight vector if not supplied
    if sample_wt is None:
      sample_wt = rep(1, length.out = args_n) # equal weighting for all source VSA vectors
    
    # For each element of the result work out which source VSA vector to sample
    # sample_spec <- sample.int(n = args_n, size = vsa_dim,
    #                           replace = TRUE, prob = sample_wt)
    sample_spec = vsa_mk_sample_spec(vsa_dim, sample_wt)

  ### Set up the selection matrix ###
  # Each row corresponds to an element of the output vector
  # Each row specifies the (row,col) cell to select from the VSA source vectors
  sel <- as.matrix(data.frame(row = 1L:vsa_dim, col = sample_spec),
                   ncol = 2, byrow = FALSE)
  
  ### Construct the result vector
  as.data.frame(args_list)[sel]

'''

## ---- tests -----------------------------------------------------

def vsa_print(x):
    for v in x:
        print('%+0.f' % v, end=' ')
    print()

def main():

    DIM = 20
    COUNT = 5

    vecs = [vsa_mk_atom_bipolar(DIM, 0) for _ in range(COUNT)]

    for vec in vecs:
        vsa_print(vec)
 
    sample_spec = vsa_mk_sample_spec(DIM, (0.1, 0.5, 0.4))

if __name__ == '__main__':
    main()
