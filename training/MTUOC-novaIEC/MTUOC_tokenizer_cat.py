#    MTUOC_tokenizer_cat
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

import pyonmttok
import sys
import html
import re
import re

subs=["d'￭","￭'en","￭'hi","￭'ho","￭'l","l'￭","￭'ls","￭'m","m'￭","￭'n","n'￭","￭'ns","￭'s","s'￭","￭'t","t'￭","￭-el","￭-els","￭-em","￭-en","￭-ens","￭-hi","￭-ho","￭-l","￭-la","￭-les","￭-li","￭-lo","￭-los","￭-m","￭-me","￭-n","￭-ne","￭-nos","￭-s","￭-se","￭-te","￭-t","￭-us","￭-vos"]
sorted_subs = sorted(subs, key=len, reverse=True)
subs=sorted_subs

expgeminada=re.compile(r'[\w]+·[\w]+')

def protect_tags(segment):
    protectedsegment=re.sub(r'(<[^>]+>)', r'｟\1｠',segment)
    return(protectedsegment)    

def protect(segment):
    segment=protect_tags(segment)
    match=expgeminada.findall(segment)
    for m in match:
        replace="｟"+m+"｠"
        segment=segment.replace(m,replace)
    segmentList=segment.split(" ")
    segment2List=segment.split(" ")
    for i in range(0,len(segment2List)):
        for sub in subs:
            sub=sub.replace("￭","")
            replace="｟"+sub+"｠"
            replaceUC="｟"+sub.upper()+"｠"
            replaceCAP="｟"+sub.capitalize()+"｠"
            if segment2List[i].find(sub)>-1:
                segment2List[i]=segment2List[i].replace(sub,"")
                segmentList[i]=segmentList[i].replace(sub,replace)
            if segment2List[i].find(sub.upper())>-1:
                segment2List[i]=segment2List[i].replace(sub.upper(),"")
                segmentList[i]=segmentList[i].replace(sub.upper(),replaceUC)
            if segment2List[i].find(sub.upper())>-1:
                segment2List[i]=segment2List[i].replace(sub.upper(),"")
                segmentList[i]=segmentList[i].replace(sub.upper(),replaceUC)
            if segment2List[i].find(sub.capitalize())>-1:
                segment2List[i]=segment2List[i].replace(sub.capitalize(),"")
                segmentList[i]=segmentList[i].replace(sub.capitalize(),replaceCAP)
    segment=" ".join(segmentList)
    return(segment)
    
def unprotect(segment):
    segment=segment.replace("｟","")
    segment=segment.replace("｠","")
    return(segment)

def tokenize(segment):
    tokenizer = pyonmttok.Tokenizer("aggressive", segment_numbers=False, joiner_annotate=False)
    segment=protect(segment)
    tokens, features = tokenizer.tokenize(segment)
    tokenized=" ".join(tokens)       
    unprotected=unprotect(tokenized).replace("％0020"," ")
    return(unprotected) 

def tokenize_m(segment):
    tokenizer = pyonmttok.Tokenizer("aggressive", segment_numbers=False, joiner_annotate=True)
    segment=protect(segment)
    tokens, features = tokenizer.tokenize(segment)
    tokenized=" ".join(tokens)       
    unprotected=unprotect(tokenized).replace("％0020"," ")
    return(unprotected) 
    
def tokenize_mn(segment):
    tokenizer = pyonmttok.Tokenizer("aggressive", segment_numbers=True, joiner_annotate=True)
    segment=protect(segment)
    tokens, features = tokenizer.tokenize(segment)
    tokenized=" ".join(tokens)       
    unprotected=unprotect(tokenized)
    return(unprotected) 
    
def detokenize(segment):
    for sub in subs:
        sub1=sub.replace("￭"," ")
        sub2=sub.replace("￭","")
        segment=segment.replace(sub1,sub2)
        sub1=sub.upper().replace("￭"," ")
        sub2=sub.upper().replace("￭","")
        segment=segment.replace(sub1,sub2)
    segment=segment.replace(" .",".")
    segment=segment.replace(" ,",",")
    segment=segment.replace(" :",":")
    segment=segment.replace(" ;",";")
    segment=segment.replace(" :",":")
    segment=segment.replace(" )",")")
    segment=segment.replace("( ","(")
    segment=segment.replace(" ]","]")
    segment=segment.replace("[ ","[")
    segment=segment.replace(" }","}")
    segment=segment.replace("{ ","{")
    segment=segment.replace(" !","!")
    segment=segment.replace("¡ ","¡")
    segment=segment.replace(" ?","?")
    segment=segment.replace("¿ ","¿")
    segment=segment.replace(" »","»")
    segment=segment.replace("« ","«")
    segment=segment.replace("‘ ","‘")
    segment=segment.replace(" ’","’")
    segment=segment.replace("“ ","“")
    segment=segment.replace(" ”","”")
    detok=segment
    return(detok)

def detokenize_m(segment):
    tokenizer = pyonmttok.Tokenizer("aggressive", segment_numbers=False, joiner_annotate=False)
    segment=tokenizer.detokenize(segment.split(" "))
    for sub in subs:
        sub1=sub.replace("￭"," ")
        sub2=sub.replace("￭","")
        segment=segment.replace(sub1,sub2)
    detok=segment
    return(detok)
    
def detokenize_mn(segment):
    tokenizer = pyonmttok.Tokenizer("aggressive", segment_numbers=True, joiner_annotate=False)
    segment=tokenizer.detokenize(segment.split(" "))
    detok=segment
    return(detok)
        

if __name__ == "__main__":
    if len(sys.argv)>1:
        action=sys.argv[1]
    else:
        action="tokenize"
    for line in sys.stdin:
        line=line.strip()
        #normalization of apostrophe
        line=line.replace("’","'")
        line=html.unescape(line)
        if action=="tokenize":
            outsegment=tokenize(line)
        elif action=="tokenize_m":
            outsegment=tokenize_m(line)
        elif action=="tokenize_mn":
            outsegment=tokenize_mn(line)
        elif action=="detokenize":
            outsegment=detokenize(line)
        elif action=="detokenize_m":
            outsegment=detokenize_m(line)
        elif action=="detokenize_mn":
            outsegment=detokenize_mn(line)
        print(outsegment)
        

