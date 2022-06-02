# README

## Scripts by Jiseng So

This is a collection of scripts by Jiseng So to help with various things. Mostly, they make the computer perform repetitive tasks so that a person does not have to. They tend to be much more accurate and up to thousands of times faster.

<table>
<tr><th>File</th><th>Description</th><th>Dependencies</th><th>Usage</th></tr>
<tr><td>Debug.py</td><td>Displays debug messages. Provides a single point to toggle debug messaging.</td><td></td><td>Import in Python.</td></tr>
<tr><th>audio</th><th colspan=3>Scripts for mostly audio stuff.</th></tr>
<tr><td>audio/unVgz.py</td><td>Takes a directory, finds all files ending with .vgz, converts them to .vgm. If no directory is provided, assumes current directory.</td><td>Depends on gunzip</td><td>unVgz.py {vgzDirectory}</td></tr>
<tr><th>dfhack</th><th colspan=3>Scripts for dfhack to interact with Dwarf Fortress.</th></tr>
<tr><td>dfhack/impregnate.lua</td><td>Impregnates viviparous creatures. Not useful with oviparous or sterile creatures.<br />Based on catsplosion.</td><td>Dwarf Fortress and dfhack</td><td>
<pre>impregnate           If the cursor points at a creature, impregnate it.
impregnate -query    Displays would-be-affected creatures without action.
impregnate -all      Affects all creatures in local site.
impregnate -species  Affects all individuals of the same species as the selected creature.
</pre>
</td></tr>
<tr><th>dos</th><th colspan=3>Utilities which interact with DOS-era files.</th></tr>
<tr><td>dos/adplayDump.py</td><td>Given a list of files, dump all music to disk, including subsongs.</td><td>Linux, adplay, sox</td><td>adplayDump.py -d {outDir} {*inputFiles}</td></tr>
<tr><td>dos/extractPak.py</td><td>Extracts Westwood .PAK files.</td><td>None</td><td>extractPak.py {PAKfile}</td></tr>
<tr><th>ElseHeartBreak</th><th colspan=3>Things for the video game Else: Heart.Break()</th></tr>
<tr><td>ElseHeartBreak/GetElseHeartBreakCode.py</td><td>Extracts code segments which contain the string "ExportMark" from saved games.</td><td>None</td><td>GetElseHeartBreakCode.py {EHBSavedGame}</td></tr>
<tr><th>images</th><th colspan=3>Manipulates images somehow.</th></tr>
<tr><td>images/capImage.py</td><td>Saves screenshots of the main display approximately once per second into a directory. Might not work with all applications, especially in fullscreen mode.</td><td>Windows, Pillow</td><td>capImage.py {basename}</td></tr>
<tr><td>images/CompressImages.py</td><td>Parallelizes recompression using pngout, running up to 7 instances in parallel. Adjust the self.compressProcessesMax to change number of instances.</td><td>pngout</td><td>CompressImages.py {DirectoryWithPngs}</td></tr>
<tr><td>images/dng2png.sh</td><td>Converts .dng files to .png in the current directory. Resulting pngs do not become much smaller with pngout.</td><td>basename, dcraw, pnmtopng, exiftool</td><td>dng2png.sh (no arguments)</td></tr>
<tr><td>images/LinScreenshotter.py</td><td>Takes screenshots and saves as pngs at approximately one per second. Uses the argument to match a window name substring. May exhibit inconsistent behavior if multiple windows contain the substring.</td><td>Linux, xwininfo, imagemagick</td><td>LinScreenshotter.py {WindowNameSubstring}</td></tr>
<tr><td>images/lossyReencoding.py</td><td>Reencodes an image until it reaches a number of encodings or reaches a loop, as determined by file hashes. Demonstrates generational loss through repeated transcoding.</td><td>imagemagick</td><td>lossyReencoding.py {imageFile}</td></tr>
<tr><th>network</th><th colspan=3>Utilities which help perform computer networking operations.</th></tr>
<tr><td>network/ipSwitcher.py</td><td>Randomly changes the IP address of the computer.</td><td>ifconfig, route</td><td>ipSwitcher.py (No arguments)</td></tr>
<tr><td>network/vpnRandomizer.py</td><td>Randomizes VPN configuration file selection.</td><td>None</td><td>vpnRandomizer.py (No arguments)</td></tr>
<tr><th>videos</th><th colspan=3>Scripts which help with making and processing videos.</th></tr>
<tr><td>videos/audioDedup.py</td><td>Works with ffmpeg to create synchronized audio to deduplicated video frames. Video should be lossless so that duplicate frames are easily discernable. Run only one instance at a time.</td><td>Linux, ffmpeg, mkvmerge, mpv.</td><td>audioDedup.py {videoFile}</td></tr>
<tr><td>videos/audioExtract.py</td><td>Extracts audio component of video files in the directory where it is invoked.</td><td>mkvmerge</td><td>audioExtract.py .</td></tr>
<tr><td>videos/bmpHandler.py</td><td>Library to handle 24-bit, uncompressed BMP image files. Saves and loads.</td><td>None</td><td>Import in Python</td></tr>
<tr><td>videos/cheeseImgDater.py</td><td>Incomplete image timestamper.</td><td></td><td></td></tr>
<tr><td>videos/cheeseSummary.py</td><td>Summarizes data from my cheese-related statistics.</td><td></td><td></td></tr>
<tr><td>videos/composite.sh</td><td>Meant to paste backgrounds and images together for soundtrack videos. Requires much manual adjustment. Run in a location containing subdirectory "origImages".</td><td>imagemagick</td><td>composite.sh</td></tr>
<tr><td>videos/CompressVideos.py</td><td>Compresses directory of videos losslessly with VP9 and FLAC. Meant to be used on already-lossless video encoded with OBS or a camera, which prioritize encoding speed over space efficiency.</td><td>ffmpeg, mkvinfo</td><td>CompressVideos.py {directoryOfVideos}</td></tr>
<tr><td>videos/Joiner.py</td><td>Concatenates all .wav files in current directory in alphabetical order. Fails if formats are different. Run in a directory with .wav files. sox is better at this in modern times.</td><td>None</td><td>Joiner.py (No arguments)</td></tr>
<tr><td>videos/mp3Extract.py</td><td>Extracts mp3s from archives without compression or encryption.</td><td>None</td><td>mp3Extract.py (Add information to script)</td></tr>
<tr><td>videos/pdfToPng.py</td><td>Converts a PDF to a series of paired images. Intended to convert books to video.</td><td>Imagemagick, pdfinfo</td><td>pdfToPng.py {PDF_to_convert}</td></tr>
<tr><td>videos/randImgMapper.py</td><td>Creates a bash script to create symlinks to images in a directory randomly.</td><td>None</td><td>randImageMapper.py (Add information to script)</td></tr>
<tr><td>videos/SilenceInserter.py</td><td>Creates a bash script to create symlinks to segments of silence. Examines current directory to determine how many. Relies on specific naming scheme.</td><td>None</td><td>SilenceInserter.py (Add information to script)</td></tr>
<tr><td>videos/stringMaker.py</td><td>Uses a BMP file representing a bitmapped font and an index to convert phrases into images with that font.</td><td>None</td><td>stringMaker.py (Add information to script)</td></tr>
<tr><td>videos/stringWordsToImages.py</td><td>Uses Imagemagick to convert a sequence of words into images.</td><td>Imagemagick</td><td>stringWordsToImages.py (Add information to script)</td></tr>
<tr><td>videos/TargetsAdvanced.py</td><td>Creates a bash script to create symlinks for each frame, now with different types of sequences. Intended to be used with MEncoder.</td><td>None</td><td>TargetsAdvanced.py (Add information to script)</td></tr>
<tr><td>videos/Targets.py</td><td>Creates a bash script to create symlinks for each frame named in a specific manner. Intended to be used with MEncoder.</td><td>None</td><td>Targets.py (Add information to script)</td></tr>
<tr><td>videos/timeIndexToList.py</td><td>Converts a time index into a Python list of frame numbers per item.</td><td>None</td><td>timeIndexToList.py (Add time index to script)</td></tr>
<tr><td>videos/WavIndexer.py</td><td>Produces an index of all WAV files in current directory, assuming that they have been concatinated in alphabetical order.</td><td>None</td><td>WavIndexer.py (No arguments)</td></tr>
<tr><th>wiki</th><th colspan=3>Utilities related to Mediawiki content</th></tr>
<tr><td>wiki/WikiCalendar.py</td><td>Creates a wikitext calendar.</td><td>holidays Python package</td><td>WikiCalendar.py {year} {numericalMonth}</td></tr>
<td></td>
</table>


<style>
td { vertical-align: top; }
</style>