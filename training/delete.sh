#!/bin/bash
echo Deletes unnecessary files before training
sudo rm -r -f /var/cache/apt/archives/
sudo rm -r -f /usr/local/cuda-11.0
