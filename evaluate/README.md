# Introduction

This directory hols diferent corpus that have not been used during training and we use 
to evaluate the performance of the English - Catalan models against others systems.

We use the current corpus that we benchmark:
* Sleepyhollow - 342 words
* Tatoeba - 2000 words
* Fedalist -5681 words
* Softcatalà user's corpus - 492 words

We basically translated these corpus with different engines to be able compare our
performance against others.

Run  ```python evaluate.py```

# Benchmark

<pre>
Transalion engine	BLEU	NIST
-- Sleepyhollow
Apertium		0.08	3.51
Yandex			0.10	3.90
Google			0.17	5.01
nmt-softcatala		0.16	4.90
-- Tatoeba
Apertium		0.19	5.24
Yandex			0.28	6.30
Google			0.36	7.60
nmt-softcatala		0.37	7.87
-- SC Users
Apertium		0.23	6.55
Google			0.51	9.56
nmt-softcatala		0.73	11.79
-- Fedalist
Yandex			0.19	5.87
Google			0.28	7.60
nmt-softcatala		0.28	7.65
</pre>

