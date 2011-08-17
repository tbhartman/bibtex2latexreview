#!/usr/bin/python

# Copyright 2011 Tim Hartman <tbhartman@gmail.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

version='0.0.1'

import argparse
import numpy as np
import re
from collections import *
import datetime
import sys
import tempfile

# argument parsing definitions

parser = argparse.ArgumentParser(prog='abaqus2dyna',
                                 description='Translate Abaqus to LS-DYNA')
parser.add_argument('input',
                    metavar='INPUT',
                    help='Abaqus keyword file (limit one)',
                    nargs=1,
                    type=argparse.FileType('r'))
parser.add_argument('-o, --output',
                    dest='output',
                    metavar='OUTPUT',
                    help='LS-DYNA keyword file output location',
                    type=argparse.FileType('w'))
parser.add_argument('-v, --version',
                    action='version',
                    version='%(prog)s ' + version)
#args = parser.parse_args()

bib = open('reviews.bib','r')

try:
    bib_lines = bib.readlines()
except UnicodeDecodeError:
    print('Oops, I don\'t do Unicode characters\n')
    exit(1)

madebyjabref = False

regex_comment = re.compile('^ *%')
for i in range(len(bib_lines)-1,-1,-1):
    if regex_comment.search(bib_lines[i]):
        if re.search('This file was created with JabRef',bib_lines[i]):
            madebyjabref = True
        bib_lines.pop(i)

bib_lines = str.join('',bib_lines)
bib_split = bib_lines.split('@')

types = Counter()
entry = {}
regex = {}
regex['type'] = re.compile('^[a-zA-Z]*{')
regex['key'] = re.compile('^{[a-zA-Z0-9\-_+=()\[\] ]*,')
regex['entry_name'] = re.compile('^[a-zA-Z]* = {')
for i in bib_split:
    i.strip()
    search_for_type = regex['type'].search(i)
    if not search_for_type:
        continue
    current_type = search_for_type.group(0)[:-1]
    if re.match('comment',current_type,flags=re.IGNORECASE):
        continue
    types[current_type] += 1
    i = i[len(current_type):]
    key = regex['key'].search(i)
    if not key:
        import pdb; pdb.set_trace()
        raise Exception('Couldn\'t find BiBTeX key')

    i = i[len(key.group(0)):-1]
    # next four lines to get rid of last two }'s
    i = i.strip()
    i = i[:-1]
    i = i.strip()
    i = i[:-1]
    key = key.group(0)[1:-1]
    entry[key] = {}
    entry[key]['type'] = current_type
    isplit = i.split('},\n')
    for j in isplit:
        j = j.strip()
        field = regex['entry_name'].search(j)
        if not field:
            import pdb; pdb.set_trace()
            raise Exception('Cannot find field/value pair')
        j = j[len(field.group(0)):]
        field = field.group(0)[:-4].lower()
        value = j
        entry[key][field] = value
        #import pdb; pdb.set_trace()

output = open('reviews.tex','w+')
output.write('% LaTeX document generated from BibTeX reviews\n')
output.write('% ' + datetime.datetime.utcnow().strftime("%y-%m-%d %H:%M:%S UTC") + '\n')
output.write('\\documentclass{bibtex2review}\n')
output.write('\\begin{document}\n\maketitle\n\\tableofcontents\n\\clearpage\n\n')

def eolsub(match):
    match = match.group(0)
    match = re.sub('\n',' ',match)
    return match

for key in entry:
    ref = entry[key]
    if 'review' in ref and ref['review'] is not None:
        output.write('% review for {:s}\n'.format(key))
        output.write('\\subsection{{{0:s}}}\n\\LARGE\n{1:s}\n\\cite{{{0:s}}}\n\\normalsize\n'.format(key,ref['title']))
        # prepare review section
        review = ref['review']
        if madebyjabref:
            # strip tabs
            review = re.sub('\t','',review)
            # strip unintended eols
            review = re.sub('.\n.',eolsub,review)
            # condense good eols
            review = re.sub('\n\n','\n',review)
        #import pdb; pdb.set_trace()

        output.write('\n\n{{\\large\n{:s}\n}}\n\\clearpage\n\n'.format(review))

output.write('%bibliography\n\\bibliography{\\finkbase}\n\\end{document}')

output.close()
