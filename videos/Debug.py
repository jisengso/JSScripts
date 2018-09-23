#!/usr/bin/python

# The debug module, so that I can turn debugging on or off from a centralized spot.

Debug = False

def Debug(text):
  if Debug:
    print(text, file=sys.stderr)