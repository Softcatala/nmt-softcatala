# Description

This directory contains the Dockerfile to compile Tensorflow 2.10 with AVX2, AVX512F and FMA extensions

Our server in production has 2 CPUs Intel Xeon: Gold 6130 2.1G 16C/32T

The gain of the compiled version with the specific CPU support is about +5% compared to the standard version
