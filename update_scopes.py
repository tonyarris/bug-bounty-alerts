#!/usr/bin/python3

# a script to update bug bounty programs in targets.txt

import requests, json, time, os, glob, sys
from random import randint

# load existing targets
def get_targets(filename):
    names = []
    with open(filename, mode='r', encoding='utf-8') as targets_file:
        for a_target in targets_file:
            names.append(a_target.split()[0])
    return names

# get live targets

# diff

# update targets.txt if necessary