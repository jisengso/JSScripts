#!/usr/bin/python3
# Extracts audio from all mkv or mp4 files in present directory, placing it in mka files with the same name.

import os

for eachFileName in os.listdir():

    if eachFileName.endswith((".mkv", ".mp4")):
        command = f"mkvmerge --no-video \"{eachFileName}\" -o \"{eachFileName[:-4]}.mka\""
        print(command)