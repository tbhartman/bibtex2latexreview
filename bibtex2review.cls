%% This is file `bibtex2review.cls`
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bibtex2review}
\LoadClass{article}

% packages
\usepackage{geometry}
\usepackage{natbib}
\usepackage{ifthen}
\usepackage{xstring}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fink}
\usepackage{color}
\usepackage{suffix}
\usepackage{multirow}
\usepackage[parfill]{parskip}

% load hyperref last
\usepackage{hyperref}
\usepackage[all]{hypcap}


\geometry{letterpaper}
\geometry{
    body={7.0in, 9.5in},
    left=0.75in,
    top=0.75in
}

% rules
\hypersetup{
    colorlinks = true,
    linkcolor = red,
    citecolor = green,
    filecolor = blue,
    urlcolor = blue,
}

\setlength{\paperheight}{11in}
\bibliographystyle{plain}
\author{T.B. Hartman}
\title{Literature Summaries}
