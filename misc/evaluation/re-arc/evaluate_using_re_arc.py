import time
import tqdm
import os
import json

from random import seed as set_seed

import dsl
from dsl import *

import utils
from utils import *

import generators
import verifiers
import sys



def get_verifiers() -> dict:
    """
    returns mapper from task identifiers (keys) to example verifier functions
    """
    prefix = 'verify_'
    return {
        strip_prefix(n, prefix): getattr(verifiers, n) for n in dir(verifiers) if n.startswith(prefix)
    }


def evaluate_verifiers(indir="arc_original/training") -> None:
    """
    runs the verifiers on a suite of ARC example pairs
    """
    verifiers = get_verifiers()
    dataset = dict()
    for key in verifiers.keys():
        filename = indir + f'/{key}.json'
        if not os.path.exists(filename): continue
        with open(filename, 'r') as fp:
            task = json.load(fp)
        if type(task) is list:
            dataset[key] = {'train': task}
        else:
            dataset[key] = format_task(task)
    if 'arc_original' in indir: fix_bugs(dataset)
    failed_on = set()
    for key, verifier in verifiers.items():
        print('Testing task ' + key + ' ... ', end='')
        if key not in dataset.keys():
            print('[missing]')
            failed_on.add(key)
            continue
        task = dataset[key]
        examples = task['train']
        if 'test' in task.keys(): examples = task['train'] + task['test']
        bad = 0
        good_examples = []
        for example in examples:
            example_input = tuple(tuple(row) for row in example['input'])
            try:
                verified = [list(row) for row in verifier(example_input)]
            except:
                verified = [[]]
                failed_on.add(key)
            exampled = [list(row) for row in example['output']]
            if verified == exampled:
                good_examples.append(example)
            try: assert verified == exampled
            except:
                failed_on.add(key)
                bad += 1
        print("pass" if not bad else "FAIL")
    n = len(verifiers)
    k = len(failed_on)
    print(f'Examples pass for {n-k}/{n} tasks (' + str(100*(n-k)/n) + '%)')
    # print(f'verification fails (on one example) for tasks {failed_on}')


if __name__ == "__main__":
    evaluate_verifiers(sys.argv[1])
