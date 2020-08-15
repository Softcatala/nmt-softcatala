
# Idees en marxa

- [ ] Entendre quines frases són les més comunes en la traducció i servir-les des d'una memòria de traducció (Jordi Mas)
- [ ] Avaluació del sistema actual amb humans respecte a Apertium (Jordi Mas)

# Idees sense desenvolupar

- [ ] El traductor no processa bé els textos només en majúscules
- [ ] Provar el model TransformerRelative en comptes de Transformer (+1 punt de BLEU)
- [ ] Usar els scripts de valencianització per a valencianitzar els corpus català i poder oferir un model anglès -> valencià
- [ ] Millorar la puntuació. Sovint no utilitza bé les comes.

# Tasques senzilles

**Afegir-hi corpus nous lliures per millorar l'abast del sistema**

Els sistemes neurals depenen molt de corpus bilingues alineats per aprendre és, és a dir, de textos en anglès amb la seva correspondència en anglès. Aquí tenim els corpus lliures que hem recopilat i/o creat: https://github.com/Softcatala/en-ca-corpus

Què cal fer? Continuar creant corpus de diferents àmbits. Quines característiques han de tenir:

* Han de ser textos amb llicències lliures
* Han de tenir la millor qualitat possible tant en anglès com en català
* Han d'estar alineats, és a dir, que cada frase en català és pugui relacionar amb la frase en anglès

Si no sé com començar, què m'aconsellaríeu? 
* Mirar els llibres disponibles a https://www.gutenberg.org/ en anglès i català de bona qualitat
* Fer servir una eina d'alineació per alinear els textos
* Revisar després la qualitat


Per ajudar en qualsevol d'aquestes tasques contacteu uniu-vos a canal de Telegram https://t.me/Softcatala_TecnoLlengua o escriviu a  Jordi Mas: jmas@softcatala.org 


# Tasques complexes

Estem parlant d'una complexitat similar a un projecte de doctorat en tecnologies de la llengua

**Millorar la qualitat de la traducció**

Objectiu: millorar la qualitat del model neural actual

Utilitzant el model neural actual fer una avaluació per a entendre les àrees a millorar amb l'objectiu incrementar la qualitat de les traduccions. Implementar les millores obtenint un increment de qualitat en avaluació humana i avaluació automàtica (p. ex. BLEU)


**Reducció del Biaix de gènere**

Objectiu: reduir el biaix de gènere en les traduccions

Crear un corpus d'avaluació del biaix de gènere, i crear una solució basada en xarxes neurals que ajudi a reduir el baix de gènere oferint
traduccions en dos gèneres quan sigui possible.

