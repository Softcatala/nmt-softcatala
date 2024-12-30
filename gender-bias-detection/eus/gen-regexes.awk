BEGIN{
FS="\t"
# badaiteke akatsak oraindik egotea
# paradigma errekursiboak eta ez-errekurtsiboak behar ditugu elipsia prozesatzeko
# momentuz paradigma bizidunak eta bizigabekoak nahastuta (overgeneration)
# errekurtsibitaterik ez (baina bi mailetako errepikapenak bai)
# maila gehiago lortzeko, bariableak iteratiboki egunera zitekeen → beste bertsio batean probatuko dut
# parentesiak erabili bada ez bada ere → gero kenduko ditut behar ez diren lekuetatik
# "aren" gabeko "-gan-" singularrean falta da
#
# errekurtsibitaterik gabeko paradigmak ("_")

KIN_="(ki(n|ko))" 
A_="(a(t|ko|n(tz|zko)|ino(ko)?)?)"
IK_="(i(k|ko))"
GA_="(ga(t" IK_ "|n(" A_ "|d" IK_ ")?))"  
N_="(n(tza(t|ko)|"	 GA_ ")?)"
NKIN_ = "(" N_ "|" KIN_ ")"
TA_="(ta(n|ko|r" A_ "|t" IK_ "))"
SINGA_="(a("GA_ "|k|r(i|e" NKIN_ ")|z(ko)?)?)"
PLUE_="(e(z(ko)?|" TA_ "|" NKIN_ "))"
	
# hitzen paradigmak
KONTS_=   "((" SINGA_ "|" PLUE_               "|ez(ko)?|e(an|ko|r"  A_ ")|ik|tzat))?" # zuhaitz, zurgin
BOK_=     "((" SINGA_ "|" PLUE_ "|re(" NKIN_ ")|z(ko)?|an|ko|r"     A_ "|rik|tzat))?" # etxe, nagusi
OTAR_= "((r(" SINGA_  "|" PLUE_               "|ez(ko)?|e(an|ko|r" A_ ")|ik)|tzat))?"  # otar, herritar
NESK_ =  "(" SINGA_  "|" PLUE_               "|ez(ko)?|a(n|ko|r" A_  "|rik|tzat))" # kutxatil/a nesk/a


# lehen mailako errekurtsibitatea
#

KO = "(ko" BOK_ "?)" # ko-ren bidezko errekurtsioa

KIN="(ki(n|" KO "))"
A= "(a(t|" KO "|n(tz|z" KO ")|ino(" KO ")?)?)"
IK="(i(k|" KO "))"
GA="(ga(t" IK "|n(" A "|d" IK ")?))"

N="(n(tza(t|" KO ")|" GA "|" KONTS_ ")?)" # n-en bidezko errekurtsioa 

NKIN = "(" N "|" KIN ")"
TA="(ta(n|ko|r" A "|t" IK "))"

# -ko eta -n elipsiaren bidezko errekurtsioa
# sakontasuna berdina??    

SINGA ="(a("GA "|k|r(i|e" NKIN ")|z(" KO ")?)?)"
PLUE="(e(k|i|z(" KO ")?|" TA "|" NKIN "))"


# hitzen paradigmak
KONTS=   "((" SINGA "|" PLUE              "|ez(" KO ")?|e(an|" KO "|r"  A ")|ik|tzat|i))?" # zuhaitz, zurgin
BOK=     "((" SINGA "|" PLUE "|re(" NKIN ")|z(" KO ")?|an|" KO "|r"     A "|rik|tzat|k|ri))?" # etxe, nagusi
NESK=  "(" SINGA  "|" PLUE              "|ez(" KO ")?|a(n|" KO "|r"  A  "|rik|tzat))" # kutxatil/a nesk/a
OTAR= "((r(" SINGA  "|" PLUE              "|ez(" KO ")?|e(an|" KO "|r"  A ")|ik)|tzat|rek|ri))?"  # otar, herritar

printf("KONTS\t%s\n",KONTS)
printf("BOK\t%s\n", BOK)
printf("NESK\t%s\n", NESK)
printf("OTAR\t%s\n", OTAR)
}
