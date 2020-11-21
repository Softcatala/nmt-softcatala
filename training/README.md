# Required hardware

We use an AWS EC2 <em>p3.2xlarge</em> instance with a Tesla
V100-SXM2-16GB. We use the following Linux image:

Deep Learning AMI (Ubuntu 18.04) Version 36.0 - ami-096a6497745975f89


# Installing the software

## Check Cuda version

Tensorflow requires specific versions of CUDA drives. Check that the CUDA
drives are properly supported by you Tensorflow version.

execute ```./install-cuda.sh``` if it is necessary.

Reboot 

## Install OpenNMT and necessary dependencies

Run ```./install.sh ```

# Training

- Run ```./get.sh```. Get the corpus
- Run ```./voc.sh```. Create vocabulary and train the tokenizer
- Run ```./train.sh```. Train the model
- Run ```./export.sh```. To export the models

# Learning on training models

[Here](./TRAINING.md) you have our learnings training models.
