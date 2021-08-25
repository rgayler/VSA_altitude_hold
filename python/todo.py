# make a DiagrammeR graph of a data flow diagram from an external spreadsheet
mk_dfd_graph <- function(
  f # character[1] - path to spreadsheet file (xlsx) containing sheets: nodes, edges
  # Look at one of the files to see the required format
) # value # DiagrammeR graph
{
  # use the same colour for the edges and borders of nodes
  linecolor <- "gray"
  
  # function to create a node data frame
  mk_nodes <- function(
    d # data frame - node definitions read from a spreadsheet
  ) # value - data frame - DiagrammeR node data frame
  {
    do.call( # call create_node_df() with arguments supplied as a list
      # this allows for arbitrary columns in the input data frame
      DiagrammeR::create_node_df,
      c(
        list(n = nrow(d), type = NULL, label = d$label),
        as.list(subset(d, select = -label))
      )
    ) %>% 
      dplyr::mutate( # add some node aesthetic attributes
        # set constant node aesthetic attributes
        color = linecolor,
        fontcolor = "black",
        # set node aesthetic attributes based on imported node properties
        fillcolor = case_when(
          role == "parameter" ~ "white",
          role == "input"     ~ "yellow1",
          role == "output"    ~ "yellow2",
          role == "function"  ~ "cyan",
          role == "reference" ~ "magenta",
          role == "post"      ~ "white",
          role == "internal"  ~ "green",
          TRUE                ~ "red" # ERROR
        ),
        shape = if_else(role == "post", "plaintext", "circle", missing = "circle"),
        peripheries = if_else(vsa == "TRUE", 3, 1, missing = 1)
      )
  }
  
  # create node data frame from spreadsheet 
  d_ndf <- readxl::read_xlsx(f, sheet = "nodes") %>% 
    mk_nodes()
  
  # DiagrammeR needs integer node IDs but the spreadsheet uses character node IDs
  # Create a lookup table to translate node IDs from character strings to integers
  d_translate <- d_ndf %>% 
    dplyr::select(node, id)
  
  # function to create an edge data frame
  mk_edges <- function(
    d # data frame - edge definitions read from spreadsheet
  ) # value - data frame - Diagrammer edge data frame
  {
    do.call( # call create_edge_df() with arguments supplied as a list
      # this allows for arbitrary columns in the input data frame
      DiagrammeR::create_edge_df,
      c(
        list(from = d$id_from, to = d$id_to, rel = NULL),
        as.list(subset(d, select = -c(from, to)))
      )
    ) %>% 
      # set edge aesthetic attributes from imported properties
      dplyr::mutate( # add some edge aesthetic attributes
        # set constant node aesthetic attributes
        arrowsize = 2,
        fontsize = 24,
        # set edge aesthetic attributes based on imported edge properties
        penwidth = if_else(vsa == "TRUE", 5, 1),
        dir = if_else(label == "=", "none", "forward", missing = "forward"),
        color = if_else(label == "=", "magenta", linecolor, missing = linecolor)
      )
  }
  
  # create edge data frame from spreadsheet 
  d_edf <- readxl::read_xlsx(f, sheet = "edges") %>%
    # translate character node IDs to integer node IDs
    dplyr::left_join(d_translate, by = c("from" = "node")) %>%
    dplyr::rename(id_from = id) %>%
    dplyr::left_join(d_translate, by = c("to" = "node")) %>%
    dplyr::rename(id_to = id) %>%
    mk_edges()
  
  # create graph
  DiagrammeR::create_graph(d_ndf, d_edf)
}

## ---- run_simulation

# Function to run an arbitrary simulation
run_simulation <- function(
  input_df, # dataframe[n_steps, n_input_vars] - values of all input variables at all times
  init_state, # dataframe[1, n_state_vars] - initial values of state variables used by f_update()
  f_update # function(prev_state, input) - state update function, args are 1-row dataframes
) # value - dataframe[n_steps, n_input_vars + n_state_vars + 1]
  # One row per time step
  # One column for each input variable, state variable, and time (t)
{
  # Apply the state update to the input values
  state_df <- input_df %>% 
    base::split(seq(nrow(.))) %>% # split input into a list of 1-row data frames
    purrr::accumulate( # accumulate list of simulated states
      f_update,
      .init = init_state
    ) %>% 
    purrr::discard(.p = seq_along(.) == 1) %>% # discard first element (initial state)
    dplyr::bind_rows() %>%  # convert list of time step states to a data frame
    dplyr::bind_cols(input_df, .) %>% # add input variables
    dplyr::mutate(t = 1:nrow(input_df), .before = everything()) # add time variable
}

# The input variables data frame is split into a list of one-row data frames
# because accumulate() requires it. The input variables could have been created
# in that format, but that's a much less convenient for general manipulation
# and the list of rows format is only required for accumulate().
# That's why the reformatting occurs on the fly in run_simulation().

# The time and input variables are added to the data frame for convenience.

## ---- vsa_cos_sim

# function to calculate the cosine similarity  of two VSA vectors
# Allow for the possibility that the vectors might not be bipolar

vsa_cos_sim <- function(
  v1, v2 # numeric - VSA vectors of identical dimension (not necessarily bipolar)
) # value # numeric - cosine similarity of the VSA vectors
{
  ### Set up the arguments ###
  # The OCD error checking is probably more useful as documentation
  
  if(missing(v1) || missing(v2)) 
    stop("two VSA vector arguments must be specified")
  
  if(!is.vector(v1, mode = "numeric"))
    stop("v1 must be an numeric vector")
  
  if(!is.vector(v2, mode = "numeric"))
    stop("v2 must be an numeric vector")
  
  vsa_dim <- length(v1)
  
  if(length(v2) != vsa_dim)
    stop("v1 and v2 must be the same length")
  
  vsa_dotprod(v1, v2) / (vsa_mag(v1) * vsa_mag(v2))
}

## ---- vsa_negate

# Function to calculate the negation of a VSA vector
# (Reverse the direction of the vector)
# Allow for the possibility that the vector might not be bipolar

vsa_negate <- function(
  v1 # numeric - VSA vector (not necessarily bipolar)
) # value # negation of input VSA vector
{
  ### Set up the arguments ###
  # The OCD error checking is probably more useful as documentation
  
  if(missing(v1)) 
    stop("VSA vector argument (v1) must be specified")
  
  if(!is.vector(v1, mode = "numeric"))
    stop("v1 must be an numeric vector")
  
  -v1
}

## ---- vsa_mk_perm

# function to make a permutation

vsa_mk_perm <- function(
  vsa_dim, # integer - dimensionality of VSA vector
  seed = NULL # integer - seed for random number generator
) # value # one randomly generated permutation specification
  # this is an integer vector of length vsa_dim
{  
  ### Set up the arguments ###
  # The OCD error checking is probably more useful as documentation
  if(missing(vsa_dim))
    stop("vsa_dim must be specified")
  
  if(!(is.vector(vsa_dim, mode = "integer") && length(vsa_dim) == 1))
    stop("vsa_dim must be an integer")
  
  if(vsa_dim < 1)
    stop("vsa_dim must be (much) greater than zero")
  
  # check that the specified seed is an integer
  if(!is.null(seed) &&!(is.vector(seed, mode = "integer") && length(seed) == 1))
    stop("seed must be an integer")
  
  # if seed is set the the vector is fixed
  # otherwise it is randomised
  set.seed(seed)
  
  # Construct a random permutation of 1:vsa_dim
  sample.int(vsa_dim)
}

## ---- vsa_mk_inv_perm

# function to make a permutation

vsa_mk_inv_perm <- function(
  perm # integer vector - specification of a permutation
) # value # integer vector [length(perm)] - specification of inverse permutation
{  
  ### Set up the arguments ###
  # The OCD error checking is probably more useful as documentation
  if(missing(perm))
    stop("perm must be specified")
  
  if(!is.vector(perm, mode = "integer"))
    stop("perm must be an integer vector")
  
  if(!all(sort(perm) == 1:length(perm)))
    stop("perm must be a permutation of 1:length(perm)")
  
  # Invert the permutation
  Matrix::invPerm(perm)
}

## ---- vsa_permute

# function to apply the specified permutation to the VSA vector

vsa_permute <- function(
  v1, # numeric - VSA vector (not necessarily bipolar)
  perm # integer vector - specification of a permutation
) # value # permutation of input VSA vector
{  
  ### Set up the arguments ###
  # The OCD error checking is probably more useful as documentation
  
  if(missing(v1)) 
    stop("VSA vector argument (v1) must be specified")
  
  if(!is.vector(v1, mode = "numeric"))
    stop("v1 must be an numeric vector")
  
  if(missing(perm))
    stop("perm must be specified")
  
  if(!is.vector(perm, mode = "integer"))
    stop("perm must be an integer vector")
  
  if(!all(sort(perm) == 1:length(perm)))
    stop("perm must be a permutation of 1:length(perm)")
  
  # apply the permutation
  v1[perm]
}

 
  ### Set up the selection matrix ###
  # Each row corresponds to an element of the output vector
  # Each row specifies the (row,col) cell to select from the VSA source vectors
  sel <- as.matrix(data.frame(row = 1L:vsa_dim, col = sample_spec),
                   ncol = 2, byrow = FALSE)
  
  ### Construct the result vector
  as.data.frame(args_list)[sel]
}

## ---- vsa_encode_scalar_spline

# function to encode a scalar numeric value to a VSA vector
# This function uses a linear interpolation spline
# to interpolate between a sequence of VSA vectors corresponding to the spline knots

vsa_encode_scalar_spline <- function(
  x, # numeric[1] - scalar value to be encoded
  spline_spec # data frame - spline spec created by vsa_mk_scalar_encoder_spline_spec()
  ): # numeric # one VSA vector, the encoding of the scalar value

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

