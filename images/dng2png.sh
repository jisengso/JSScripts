# dng2png
# By Jiseng So
# Converts all dng files in the current directory to png and transfers all possible EXIF tags.

DEPENDS="basename dcraw pnmtopng"
DOCONVERSION="YES"
for dependency in $DEPENDS
do
    if [ `which $dependency` ]; then
        echo "$dependency exists."
    else
        echo "Cannot find $dependency."
        DOCONVERSION=""
    fi
done

if [ `which exiftool` ]; then
    echo "exiftool exists."
else
    echo "Cannot find exiftool. It is optional, but EXIF tags will not be transferred."
fi

if [ $DOCONVERSION ]; then
    for dngfile in `ls *.dng`
    do 
        echo "Processing $dngfile"
        OUTFILE=`basename $dngfile .dng`.png
        dcraw -c -w $dngfile | pnmtopng > $OUTFILE
        exiftool -overwrite_original_in_place -ee -U -F -tagsFromFile $dngfile $OUTFILE 
    done
    mkdir -p dngFiles
    mv *.dng dngFiles
fi
