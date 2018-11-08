mkdir /dev/shm/ImageMagickTMP

for i in $(ls origImages)
    do
    mkdir $i
    convert perPhrase/00$i.bmp -scale 800% -transparent $(cat perPhrase/fillColor.txt) /dev/shm/ImageMagickTMP/currentTitle.png
    for j in $(ls origImages/$i)
        do
            composite logo.png -gravity NorthWest -geometry +50+50 origImages/$i/$j /dev/shm/ImageMagickTMP/currentImg.png
            composite /dev/shm/ImageMagickTMP/currentTitle.png -gravity South -geometry +0+100 /dev/shm/ImageMagickTMP/currentImg.png $i/$j
        done

    done
