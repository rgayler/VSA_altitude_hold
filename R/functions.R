

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
          role == "input"     ~ "yellow",
          role == "output"    ~ "orange",
          role == "internal"  ~ "LightBlue",
          role == "function"  ~ "DeepSkyBlue",
          role == "post"      ~ "white",
          TRUE                ~ "red" # ERROR
        ),
        shape = if_else(role == "post", "plaintext", "circle"),
        peripheries = if_else(vsa == "TRUE", 3, 1)
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
        color = linecolor,
        arrowsize = 1,
        # set edge aesthetic attributes based on imported edge properties
        penwidth = if_else(vsa == "TRUE", 5, 1)
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
