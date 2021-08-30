'''
VSA functions

Copyright (c) 2021 Ross W. Gayler and Simon D. Levy

MIT License
'''

import numpy as np

# ---- mk_sample_spec --------------------------------------------------------

# function to make a sampling specification for adding VSA vectors


def mk_sample_spec(
  dim,        # integer - dimensionality of VSA vectors
  sample_wt,  # numeric vector - VSA vector sampling weights
  seed=None # integer - seed for random number generator
):  # returns VSA vector, the weighted sum (sampled) of the argument vectors

  # if seed is set the sampling specification vector is fixed
  # otherwise it is randomised
  np.random.seed(seed)
  
  return np.random.choice(len(sample_wt), size=dim, replace=True, p=sample_wt)

# ---- mag -------------------------------------------------------------------

# function to calculate the magnitude of a VSA vector
# Allow for the possibility that the vector might not be bipolar


def mag (
  v1  # numeric - VSA vector (not necessarily bipolar)
  ):  # value # numeric - magnitude of the VSA vector

  # No numerical analysis considerations 
  return np.sqrt(np.sum(v1*v1))


# ---- mk_atom_bipolar -------------------------------------------------------

# function to make an atomic VSA vector


def mk_atom_bipolar(
  dim,         # dimensionality of VSA vector
  seed=None  # seed for random number generator
  ):           # value # one randomly selected VSA vector of dimension dim
  
  # if seed is set the the vector is fixed
  # otherwise it is randomised
  np.random.seed(seed)
  
  # Construct a random bipolar vector
  return 2 * (np.random.random(dim) > 0.5) - 1

# ---- multiply --------------------------------------------------------------

# function to multiply an arbitrary number of VSA vectors


def multiply(vectors
     # >= 2 VSA vectors of identical dimension as arguments to multiply
  ): # returns the weighted sum (sampled) of the argument vectors


    result = np.ones(len(vectors[0]))

    for v in vectors:
        result *= v

    return result

# ---- mk_scalar_encoder_spline_spec -----------------------------------------

# function to make the specification for a piecewise linear spline encoder


def mk_scalar_encoder_spline_spec(
  dim,         # dimensionality of VSA vectors
  knots,       # numeric vector - scalar knot locations (in increasing order)
  seed=None  # integer - seed for random number generator
  ):           # returns dictionary for linear spline encoder specification

  # set the seed
  np.random.seed(seed)
  
  # generate VSA atoms corresponding to each of the knots
  return { 
          'knots_scalar' : knots,
          'knots_vsa' : [mk_atom_bipolar(dim) for _ in knots]
          }

# ---- dotprod ---------------------------------------------------------------

# function to calculate the dot product  of two VSA vectors
# Allow for the possibility that the vectors might not be bipolar


def dotprod(
  v1, v2  # VSA vectors of identical dimension (not necessarily bipolar)
  ):      # returns cosine similarity of the VSA vectors

  # No numerical analysis considerations 
  return np.sum(v1*v2)

# ---- decode_scalar_spline --------------------------------------------------

# function to encode a scalar numeric value to a VSA vector
# This function uses a linear interpolation spline  to interpolate between a
# sequence of VSA vectors corresponding to the spline knots


def decode_scalar_spline (
  v,               # numeric - VSA vector (not necessarily bipolar)
  spline_spec,     # spline spec from mk_scalar_encoder_spline_spec()
  zero_thresh = 4  # zero threshold (in standard deviations)
  ):  # returns scalar value decoded from v

  # get the dot product of the encoded scalar with each of the knot vectors
  dotprods = np.array(list(map(lambda w : dotprod(v,w),
                                          spline_spec['knots_vsa'])))

  # set dot products below the zero threshold to 0.5
  zero_thresh = zero_thresh * np.sqrt(len(v) * 0.5)
  dotprods[dotprods<zero_thresh] = 0

  # normalise the dot products
  dotprods = dotprods / np.sum(dotprods)

  # return the weighted sum of the knot scalars
  return np.sum(dotprods * spline_spec['knots_scalar'])

# ---- add -------------------------------------------------------------------

# function to add (weighted sum) an arbitrary number of VSA vectors given as
# arguments Weighted add is implemented as weighted sampling from the source
# vectors. If sample_spec is given it specifies which argument vector is the
# source for each element of the output vector. If sample_wt is given the
# sample specification is generated randomly. If neither sample_spec or
# sample_wt is given then sample_wt is constructed with equal weight for each
# argument vector.


def add(
  vectors,
  sample_spec=None,  # source (argument VSA vector) for each element of result
  sample_wt=None     # numeric vector - argument vector sampling weights
  ):  # returns VSA vector, the weighted sum (sampled) of the argument vectors

    count = len(vectors)
    dim = len(vectors[0])

    if sample_spec is None:

        # sample spec not supplied - make a new random one
        # create a sampling weight vector if not supplied
        if sample_wt is None:
            # equal weighting for all source VSA vectors
            sample_wt = np.ones(count) / count

        # For each element of the result work out which source VSA vector to
        # sample
        sample_spec = mk_sample_spec(dim, sample_wt, 0)

    return np.array([vectors[k][j] for (j, k) in enumerate(sample_spec)])

# ---- permute ---------------------------------------------------------------

# function to apply the specified permutation to the VSA vector


def permute(
  v1,   # numeric - VSA vector (not necessarily bipolar)
  perm  # integer vector - specification of a permutation
  ):  # returns permutation of input VSA vector

    # apply the permutation
    return [v1[k] for k in perm]

# ---- mk_perm ---------------------------------------------------------------

# function to make a permutation


def mk_perm(
  dim,         # dimensionality of VSA vector
  seed=None  # seed for random number generator
  ):  # returns one randomly generated permutation specification
    # this is an integer vector of length dim

    # if seed is set the the vector is fixed
    # otherwise it is randomised
    np.random.seed(seed)

    # Construct a random permutation of 1:dim
    return np.random.choice(dim, dim, False)

# ---- mk_inv_perm -----------------------------------------------------------

# function to make a permutation


def mk_inv_perm(
  perm  # integer vector - specification of a permutation
  ):    # integer vector [length(perm)] - specification of inverse permutation

    # Invert the permutation
    return np.argsort(perm)

# ---- cos_sim ---------------------------------------------------------------

# function to calculate the cosine similarity  of two VSA vectors
# Allow for the possibility that the vectors might not be bipolar


def cos_sim(
  v1, v2  # VSA vectors of identical dimension (not necessarily bipolar)
  ):      # value # numeric - cosine similarity of the VSA vectors

    return dotprod(v1, v2) / (mag(v1) * mag(v2))


# ---- negate ----------------------------------------------------------------

# Function to calculate the negation of a VSA vector
# (Reverse the direction of the vector)
# Allow for the possibility that the vector might not be bipolar


def negate(
  v1  # numeric - VSA vector (not necessarily bipolar)
  ):  # value # negation of input VSA vector

    return -v1

# ---- encode_scalar_spline --------------------------------------------------

# function to encode a scalar numeric value to a VSA vector This function uses
# a linear interpolation spline to interpolate between a sequence of VSA
# vectors corresponding to the spline knots


def encode_scalar_spline(
  x,  # numeric[1] - scalar value to be encoded
  spline_spec  # data frame - spline spec from mk_scalar_encoder_spline_spec()
  ):  # numeric # one VSA vector, the encoding of the scalar value

    knots_scalar = spline_spec['knots_scalar']

    # Map the scalar into a continuous index across the knots
    # Linearly interpolate the input scalar onto a scale in which knots
    # correspond to  0:(n-1)
    i = np.interp(x, knots_scalar, range(len(knots_scalar)))

    # Get the knot indices immediately above and below the index value
    i_lo = int(np.floor(i))
    i_hi = int(np.ceil(i))

    # Return the VSA vector corresponding to the index value
    if i_lo == i_hi:  # check if index is on a knot
        # Exactly on a knot so return the corresponding knot VSA vector
        return spline_spec['knots_vsa'][int(i)]

    # Between two knots
    # Return the weighted sum of the corresponding knot VSA vectors
    i_offset = i - i_lo
    vecs = spline_spec['knots_vsa']
    return add([vecs[i_lo], vecs[i_hi]], sample_wt=(1 - i_offset, i_offset))
