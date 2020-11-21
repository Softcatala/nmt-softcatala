# Introduction

This document explains our experiences training models using OpenNMT.

# Models

## Neurals models are not reproducible

Every time that you train a model will have a complete different neural network. When you evaluate its quality, overall may be better
but may be specific translations that were done better in previous models. This can introduce confusion to the users because
new models will translate differently. The only thing that is sure is that the model is better globally or worse than previous models.

## Vocabulary size

We found that a vocabulary size of 50.000 words covers well our needs at least with the current corpus of 5 milions segments.

Increasing the vocabulary size did not provide any improvement in BLUE and slows down translations significantly since the
model is much bigger.

## How to improve the performance on the model

We believe that there are 3 ways:

1. Improvements on new algorims used (attention, transformers, tokenizers)
2. Configuration of the model training
3. Improvements in the corpus

Our current hypothesis is that better to focus on 3).

## When to re-train 

Basically we belive is makes sense to retrain the models on these scenario:

1. Improvements on new algorithms used (attention, transformers, tokenizers)
2. Configuration of the model training
3. Better corpus

## Evaluating quality of improvements in the corpus

The corpus is divided in training (the majority of it) to train the model and evaluation to evaluate the performance of the model.

When we make improvements in the corpus, then we made these improvements to the corpus that we use for evaluation too. As result the evaluation corpus is improved also and you cannot compare with previous trainings with old models. In trainings with better corpus, you can get the same BLEU because your evaluation is also more demanding.

To prevent this, we evaluate also the models against corpus (SleppyHollow and Tatoeba) that have not seen during training and never change. 


