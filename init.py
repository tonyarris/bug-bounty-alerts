#!/usr/bin/python3

# a script to set up the comparison files on first run
import requests
import json
import time
from random import randint
import os, glob, sys

# get target names
def get_targets(filename):
    names = []
    with open(filename, mode='r', encoding='utf-8') as targets_file:
        for a_target in targets_file:
            names.append(a_target.split()[0])
    return names

if __name__ == "__main__":

    # get cwd
    cwd = os.getcwd()

    # remove any existing responses
    if len(os.listdir(cwd + '/responses/')) != 0:
        files = glob.glob(cwd + '/responses/*')
        
        # remove temp files
        for file in files:
            os.remove(file)

    # get request headers
    with open('./requests/headers.json') as f:
        headers = json.load(f)

    # get request body
    with open('./requests/body') as f:
        body = json.load(f)
    
    names = get_targets('targets.txt')

    i = 0
    # loop over targets and get scope
    for name in names:
        # place target in body
        body['variables']['handle'] = names[i]

        # create/open file
        filename = './responses/{0}'.format(names[i])
        f = open(filename, 'a')

        # make request and process relevant parts of response
        r = requests.post('https://hackerone.com/graphql', headers=headers, json=body)
        r = r.json()
        try:
            scope = r['data']['team']['in_scope_assets']['edges']
            for node in scope:
                f.write(node['node']['asset_identifier'])
                f.write('\n')
                f.write(node['node']['instruction'])
            i += 1
            f.close
        except:
            print("Unexpected error:", sys.exc_info()[0])
        time.sleep(randint(1,2))
       