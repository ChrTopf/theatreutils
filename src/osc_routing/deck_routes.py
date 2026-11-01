# First OSC address segment that tells the relay which deck a message is for,
# e.g. "/x32/-action/gosnippet 5" is forwarded to the X32 as "/-action/gosnippet 5".
X32_ROUTE = "x32"
MAGICQ_ROUTE = "mq"

# Sent by the Script Viewer straight to LiSP (not via the relay) to start the cue with the given user number (from 1).
LISP_CUE_ADDRESS = "/lisp/cue"
