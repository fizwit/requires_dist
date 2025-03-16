#!/usr/bin/env python3
"""
requires.py
This script will evaluate the requires_dist from the metadata of a PyPi package.
The requires_dist is a list of requires based on pep508 grammer. The
requires_dist is evaluated based on the environment variables provided in the
script. The `packaing` module allows the environment to be modified, deminstrate
the use of modifing the `env` during evaluation of `requires` from the metadata.

The environment variables are set in the `env` dictionary.

The requires_dist is evaluated and printed to the console.
"""

import sys
import requests
from packaging.requirements import Requirement


__version__ = '1.0.0'
__date__ = 'March, 16 2025'
__maintainer__ = 'John Dey jfdey@fredhutch.org'

env = {'python_version': '3.10', 'platform_python_implementation': 'CPython',}


def get_pypi_meta_data(name):
    """ requires_dist is a list of requires based on pep508
    Evalute the requires_dist and return a list of evaluated requires
    """
    url = f"https://pypi.org/pypi/{name}/json"
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        sys.exit(1)
    return data


def display_meta_data(pypi_meta_data):
    fields = ['name', 'version', 'classifiers', 'requires_dist']
    for val in fields:
        print(f"{val.capitalize():>30} : {pypi_meta_data['info'][val]}")


def process_requires_dist(project_name, pypi_meta_data):
    """ process the requires_dist from the metadata
        follow the requires_dist and evaluate the requires recursively
    """
    global top_level
    if 'requires_dist' not in pypi_meta_data['info'] or pypi_meta_data['info']['requires_dist'] is None:
        return
    for req in pypi_meta_data ['info']['requires_dist']:
        require = Requirement(req)
        if require.marker:
            evaluated = require.marker.evaluate(env)
            if evaluated:
                data = get_pypi_meta_data(require.name)
                # print(f"  {require.name} : {data['info']['version']} {data['info']['requires_dist']}")
                process_requires_dist(require.name, data)
                print(f"  {require.name:>30} : Add from {project_name}")
            elif project_name == top_level:
                print(f"  {require.name:>30} : {evaluated} from {project_name}")
        else:
            print(f"  {require.name:>30} : Add")


global top_level
if __name__ == "__main__":
    test_packages = ['anyio']
    
    if len(sys.argv) > 1:
        test_packages = sys.argv[1:]
    for name in test_packages:
        top_level = name
        pypi_meta_data = get_pypi_meta_data(name)
        display_meta_data(pypi_meta_data)
        process_requires_dist(name, pypi_meta_data)
