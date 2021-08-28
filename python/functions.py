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
  sample_spec=None, # int vec - source (argument VSA vector) for each element of result
  sample_wt=None    # numeric vector - argument vector sampling weights
  ): # value # one VSA vector, the weighted sum (sampled) of the argument vectors

  count = len(vectors)
  vsa_dim = len(vectors[0])

  if sample_spec is None:

    # sample spec not supplied - make a new random one
    # create a sampling weight vector if not supplied
    if sample_wt is None:
      sample_wt = np.ones(count) / count # equal weighting for all source VSA vectors

    # For each element of the result work out which source VSA vector to sample
    sample_spec = vsa_mk_sample_spec(vsa_dim, sample_wt, 0)

  return np.array([vectors[k][j] for (j,k) in enumerate(sample_spec)])

## ---- vsa_permute -----------------------------------------------

# function to apply the specified permutation to the VSA vector

def vsa_permute(
  v1, # numeric - VSA vector (not necessarily bipolar)
  perm # integer vector - specification of a permutation
  ): # value # permutation of input VSA vector

  # apply the permutation
  return [v1[k] for k in perm]

## ---- vsa_mk_perm ------------------------------------------------

# function to make a permutation

def vsa_mk_perm(
  vsa_dim, # integer - dimensionality of VSA vector
  seed = None # integer - seed for random number generator
  ): # value # one randomly generated permutation specification
  # this is an integer vector of length vsa_dim

  # if seed is set the the vector is fixed
  # otherwise it is randomised
  np.random.seed(seed)
  
  # Construct a random permutation of 1:vsa_dim
  return np.random.choice(vsa_dim, vsa_dim, False)

## ---- vsa_mk_inv_perm --------------------------------------------

# function to make a permutation

def vsa_mk_inv_perm(
  perm # integer vector - specification of a permutation
  ): # value # integer vector [length(perm)] - specification of inverse permutation

  # Invert the permutation
  return np.argsort(perm)

## ---- vsa_cos_sim ------------------------------------------------

# function to calculate the cosine similarity  of two VSA vectors
# Allow for the possibility that the vectors might not be bipolar

def vsa_cos_sim(
  v1, v2 # numeric - VSA vectors of identical dimension (not necessarily bipolar)
  ): # value # numeric - cosine similarity of the VSA vectors

  
  return vsa_dotprod(v1, v2) / (vsa_mag(v1) * vsa_mag(v2))


## ---- vsa_negate -------------------------------------------------

# Function to calculate the negation of a VSA vector
# (Reverse the direction of the vector)
# Allow for the possibility that the vector might not be bipolar

def vsa_negate(
  v1 # numeric - VSA vector (not necessarily bipolar)
  ): # value # negation of input VSA vector

  
  return -v1

## ---- vsa_encode_scalar_spline -------------------------------------

# function to encode a scalar numeric value to a VSA vector This function uses
# a linear interpolation spline to interpolate between a sequence of VSA
# vectors corresponding to the spline knots

def vsa_encode_scalar_spline(
  x, # numeric[1] - scalar value to be encoded
  spline_spec # data frame - spline spec created by vsa_mk_scalar_encoder_spline_spec()
  ): # numeric # one VSA vector, the encoding of the scalar value

    '''
    # Map the scalar into a continuous index across the knots
    # Linearly interpolate the input scalar onto a scale in which knots correspond to  1:n
    i = approx(
        x = spline_spec$knots_scalar, y = seq_along(spline_spec$knots_scalar), 
        rule = 2, # clip x to fit the range of the knots
        xout = x
        )$y # get the interpolated value only

    # Get the knot indices immediately above and below the index value
    i_lo = np.floor(i)
    i_hi = np.ceil(i)

    # Return the VSA vector corresponding to the index value
    if i_lo == i_hi: # check if index is on a knot
        # Exactly on a knot so return the corresponding knot VSA vector
        return spline_spec$knots_vsa[[i]] 

    # Between two knots
    # Return the weighted sum of the corresponding knot VSA vectors
    i_offset = i - i_lo
    return vsa_add(
      spline_spec$knots_vsa[[i_lo]], spline_spec$knots_vsa[[i_hi]],
      sample_wt = c(1 - i_offset, i_offset)
    )
    '''

    return None

 
## ---- tests -----------------------------------------------------

def vsa_print(x):
    for v in x:
        print('%+0.f' % v, end=' ')
    print()

def main():


    '''
    DIM = 20
    COUNT = 5

    vecs = [vsa_mk_atom_bipolar(DIM, 0) for _ in range(COUNT)]

    print('vectors:')
    for vec in vecs:
        vsa_print(vec)
 
    print('\n')
    vsa_print(vsa_add(vecs))


    DIM = 10
    v = vsa_mk_atom_bipolar(DIM)
    p = vsa_mk_perm(DIM, 0)
    ip = vsa_mk_inv_perm(p)
    print(v)
    vi = v[p]
    print(vi)
    print(vi[ip])
    print(np.all(v == vi[ip]))

    DIM = 1000

    a = vsa_mk_atom_bipolar(DIM)
    b = vsa_mk_atom_bipolar(DIM)

    print(vsa_cos_sim(a, a))


    DIM = 10
    v = vsa_mk_atom_bipolar(DIM)
    vsa_print(v)
    vsa_print(vsa_negate(v))
    '''

    DIM = 10
    KNOTS = .1, .2, .3
    spline_spec = vsa_mk_scalar_encoder_spline_spec(DIM, KNOTS, 0)
    print(vsa_encode_scalar_spline(1.5, spline_spec))

if __name__ == '__main__':
    main()
