#!/bin/bash

# if this script takes an argument, it is from incrond
if [ $# -gt 0 ]
then
    echo "$@"
    if [ "$1" != "hartman.bib" ]
    then
        exit 1
    fi
fi
export DISPLAY=:0.0
cd /home/tbhartman/Dropbox/VT/Research/JournalArticles/reviewsToLaTeX

cp ../hartman.bib ./reviews.bib
dos2unix ./reviews.bib

./reviews.py

if [ $? -gt 0 ]
then
    notify-send -t 4000 'BibTeX Reviews' 'Failure'
    exit 1
fi

pdflatex --interaction=nonstopmode reviews 1> /dev/null
bibtex reviews 1> /dev/null
pdflatex --interaction=nonstopmode reviews 1> /dev/null
pdflatex --interaction=nonstopmode reviews 1> /dev/null


if [ -f reviews.pdf ]
then
    cp reviews.pdf ../_hartman.bib.reviews.pdf
    
    rm reviews.aux
    rm reviews.log
    rm reviews.out
    rm reviews.toc
    rm reviews.bbl
    rm reviews.blg
    /usr/bin/notify-send -t 4000 'BibTeX Reviews' 'Updated'
else
    /usr/bin/notify-send -t 10000 'BibTeX Reviews' 'Failure'
    echo "Problem, no PDF!"
    exit 1
fi
