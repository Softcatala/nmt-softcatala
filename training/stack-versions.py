#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import tensorflow as tf
import opennmt
import pkg_resources

ctranslate_version = pkg_resources.get_distribution('ctranslate2').version
print(f"TF version {tf.__version__}, OpenNMT version {opennmt.__version__}, CTranslate2 version {ctranslate_version}")
