# Introduction

This directory holds diferent corpus that have not been used during training and we use
to evaluate the performance of the English - Catalan models against others systems.

We use the current corpus that we benchmark:
* Sleepyhollow - 342 words
* Tatoeba - 2000 words
* Fedalist - 5681 words
* Softcatalà user's corpus - 492 words

We basically translated these corpus with different engines to be able compare our
performance against others.

Run ```python evaluate.py```

# Benchmark

<pre>


anguage pair: English > Catalan
-- Sleepyhollow
Apertium		0.08	3.51
Yandex			0.10	3.90
Google			0.17	5.01
nmt-softcatala		0.16	4.87
-- Tatoeba
Apertium		0.19	5.24
Yandex			0.28	6.30
Google			0.36	7.60
nmt-softcatala		0.38	7.94
-- SC Users
Apertium		0.23	6.55
Google			0.51	9.56
nmt-softcatala		0.53	9.77
-- Fedalist
Yandex			0.19	5.87
Google			0.28	7.60
nmt-softcatala		0.28	7.63
Translation engine	BLEU	NIST
Language pair: German > Catalan
-- Tatoeba
Yandex			0.24	5.24
Google			0.34	6.72
nmt-softcatala		0.32	6.53
-- Ubuntu
Yandex			0.10	4.59
Google			0.22	6.52
nmt-softcatala		0.18	5.63
Translation engine	BLEU	NIST
Language pair: Catalan > German
-- Ubuntu
Google			0.14	5.03
nmt-softcatala		0.13	5.08
</pre>

