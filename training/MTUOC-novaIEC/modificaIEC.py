#    modificaIEC.py   
#    Copyright (C) 2020  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import codecs
import sys
from MTUOC_tokenizer_cat import tokenize
from MTUOC_tokenizer_cat import detokenize
import unicodedata


fcanvis=codecs.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "canvisDIECnova.txt"),"r",encoding="utf-8")

canvis={}
for linia in fcanvis:
    linia=linia.rstrip()
    if not linia.startswith("#"):
        camps=linia.split("\t")
        canvis[camps[0]]=camps[1]

entrada=codecs.open(sys.argv[1],"r",encoding="utf-8")
sortida=codecs.open(sys.argv[2],"w",encoding="utf-8")

claus=set(canvis.keys())
for linia in entrada:
    cat=linia.rstrip(os.linesep)
    leading_spaces=len(cat)-len(cat.lstrip())
    trailing_spaces=len(cat)-len(cat.rstrip())
    cat=cat.strip()
    cat=cat.replace("’","'") #normalitzacio apòstrof
    cat=cat.replace("l.l","l·l") #normalitzacio l geminada
    cat=cat.replace("L.L","L·L") #normalitzacio l geminada
    cat=unicodedata.normalize('NFC',cat)                    
    cattok=tokenize(cat)
    tokens=set(cattok.split(" "))
    cattok=" "+cattok+" "
    commonclaus=tokens.intersection(claus)
    if len(commonclaus)>0:
        cattok2=cattok
        for cc in commonclaus:
            cattok2=cattok2.replace(" "+cc+" "," "+canvis[cc]+" ")
            cattok2=cattok2.replace(" "+cc.upper()+" "," "+canvis[cc].upper()+" ")
            cattok2=cattok2.replace(" "+cc.capitalize()+" "," "+canvis[cc].capitalize()+" ")
        cat2=detokenize(cattok2).strip()
    else:
        cat2=cat
    cat2=" "*leading_spaces+cat2+" "*trailing_spaces
    sortida.write(cat2+"\n")
    
