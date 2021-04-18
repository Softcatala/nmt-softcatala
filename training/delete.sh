#!/bin/bash
echo Deletes unnecessary files before training
sudo rm -r -f /var/cache/apt/archives/
sudo rm -r -f /usr/local/cuda-11.0
sudo rm -f -r /home/ubuntu/anaconda3/envs/ # 40Gb of python envs
