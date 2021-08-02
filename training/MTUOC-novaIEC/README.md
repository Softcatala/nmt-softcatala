MTUOC-novaIEC
=============

## Introduction

A simple script and data file to chang Catalan texts from old ortography to new othograpy. All changes have been taken from [ORTOGRAFIA Modificacions entrades DIEC2](https://www.iec.cat/llengua/documents/ORTOGRAFIA-Modificacions%20entrades%20DIEC2.pdf). Please, keep in mind that only orthographic changes have been implemented.

The script can be useful to convert Catalan corpora to the new orthographic norms.

The three files:

- modificaIEC.py
- MTUOC_tokenizer_cat.py
- canvisDIECnova.txt

should be in the same directory.

## Usage

To convert the file exemples-antiga.txt to exemples-nova.txt:

```
python3 modificaIEC.py exemples-antiga.txt exemples-nova.txt
```

## License

This program is under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
